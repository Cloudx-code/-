from CN_DBpedia.CN_DBpedia import getTripleInfoFromCN_DB
from neo4jUtil import getNeo4jConn,createRelation,createMasterNode,createGeneralNode,\
    whetherNodeExist,getNeo4jNode
from neo4jUtil import createBookNode
from util.csvUtil import getCsv
# match (n) detach delete n
# 删库
# MATCH (n:`图书中文名`) RETURN count(*) 查询某一节点数量
# MATCH (n:`图书中文名`{name:'红楼梦'})-[]-()  RETURN count(*) 查询某一节点的关系数量

# 通过CN_DB扩充数据(当前这个返回方式很丑陋，需要改进)
def expandDataFromCN_DB(graphConn,node1):
    j=0
    tripleInfo = getTripleInfoFromCN_DB(node1.get("name"))
    if len(tripleInfo) > 0 and tripleInfo[0]=="http wrong":
        return node1
    for i in tripleInfo:
        relationship = i[0]
        node2Info = i[1]
        node2 = getNeo4jNode(graphConn,"CN_DB",str(node2Info))
        if whetherNodeExist(node2):
            continue
        node2 = createGeneralNode(graphConn, "CN_DB", str(node2Info))
        if createRelation(graphConn,node1,str(relationship),node2):
            j+=1
    return j
#从CSV中创建节点与关系
def createNodeAndRelationFromCsv(graphConn, titleName, csvData):
    j=0
    # # 1.书籍链接详情
    # createSlaveNode(graphCon, str(tableName[0]), str(i[0]))
    # # 2.图片链接
    # createSlaveNode(graphCon, str(tableName[1]), str(i[1]))
    # 3.图书中文名,node = Node(label,name = name,书籍链接=bookInfo,图片链接=picInfo,相关信息=relatedInfo)
    masterNode = createMasterNode(graphConn, str(titleName[2]), str(csvData[2]), str(csvData[0]), str(csvData[1]), str(csvData[7]))
    # 4.评分
    slaveNode1 = createGeneralNode(graphConn, str(titleName[4]), str(csvData[4]))
    # 5.评价数
    slaveNode2 = createGeneralNode(graphConn, str(titleName[5]), str(csvData[5]))
    # 6.概况
    slaveNode3 = createGeneralNode(graphConn, str(titleName[6]), str(csvData[6]))
    # # 7.相关信息
    # createSlaveNode(graphCon, str(tableName[7]), str(i[7]))
    # 8.图书别名
    if str(csvData[3]) != " " and str(csvData[3]) != '':
        slaveNode4 = createGeneralNode(graphConn, str(titleName[3]), str(csvData[3]))
        if createRelation(graphConn, masterNode, str(titleName[3]), slaveNode4):
            j += 1
    # 作者,若作者节点不存在，则创建节点，若存在则只创建关系
    slaveNode5 = createGeneralNode(graphConn, str(titleName[8]), str(csvData[8]))
    # 创建关系
    # 作者与书籍(单向)
    if createRelation(graphConn, masterNode, str(titleName[8]), slaveNode5):
        j += 1
    # 书籍与评分
    if createRelation(graphConn, masterNode, str(titleName[4]), slaveNode1):
        j += 1
    # 书籍与评价数
    if createRelation(graphConn, masterNode, str(titleName[5]), slaveNode2):
        j += 1
    # 书籍与概况
    if createRelation(graphConn, masterNode, str(titleName[6]), slaveNode3):
        j += 1
    # 其他字段拓展，BookType,根据书籍评分拓展受欢迎度
    j+=expandSomeField(graphConn,masterNode,titleName,csvData)
    return j

def expandSomeField(graphConn,masterNode,titleName,csvData):
    j=0
    # 补上拓展的BookType信息,csvData[9]是一串字符串，包含了书籍类别
    j+=expandBookType(graphConn,masterNode,str(titleName[9]),csvData[9])
    return j

# 补充书籍用户标签
def expandBookType(graphConn, masterNode, label, bookTypeSets):
    bookTypes = bookTypeSets.split(" ")
    j=0
    for bookType in bookTypes:
        bookTypeNode = createGeneralNode(graphConn, label, bookType)
        if createRelation(graphConn,masterNode,label,bookTypeNode):
            j+=1
    return j
# 核心函数代码
def createNodeAndRelation(graphConn, csvDatas):
    # Csv列名
    titleName = csvDatas[0]
    # 统计创建关系次数
    j=1
    # 轮次数
    times = 1
    # 计划重试的关系数据集
    failData = []
    # 默认从1开始
    for csvData in csvDatas[1:]:
        # 弄个人看的名字
        bookName = csvData[2]
        author = csvData[8]
        print("第",times,"轮,书名:",bookName,"作者:",author)
        times+=1
        #将对CSV文件的内容做节点与关系扩充
        j+=createNodeAndRelationFromCsv(graphConn,titleName,csvData)
        #通过CN_DB扩充
        # 扩充作者信息
        ans = expandDataFromCN_DB(graphConn,getNeo4jNode(graphConn, titleName[8], author))
        if type(ans)==type(1):
            j+=ans
        else:
            failData.append(ans)
        # 扩充作品信息
        ans = expandDataFromCN_DB(graphConn,getNeo4jNode(graphConn, str(titleName[2]), bookName))
        if type(ans)==type(1):
            j+=ans
        else:
            failData.append(ans)
        print("已创建第", j, "个关系")
    # 失败重试的机会
    j+=failRecover(graphConn,failData)
    print("共", j, "个关系创建成功")
    return


def failRecover(graphConn,failData):
    print("有", len(failData), "个节点请求http时失败了,重试ing")
    k = 0
    j=0
    for i in failData:
        ans = expandDataFromCN_DB(graphConn, i)
        if type(ans) == type(1):
            j += ans
            k += 1
        else:
            print(i.get("name"), "节点恢复失败,建议后续手动处理")
            print(i, "感觉不会有太多,打印完整的瞅瞅")
    print("错误节点中恢复成功", k, "个")

    return j

def createNeo4jByCsv(graphConn,title:str,tag:str):
    loadPath = r"../bookData/" + title + "/book-list-" + tag + ".csv"
    csvData = getCsv(loadPath)
    labels = csvData[0] # ['书籍详情链接', '图片链接', '书名', '图书别名', '评分', '评价数', '概况', '出版相关信息', '作者', '用户标签', '出版社']
    for bookData in csvData[1:]:
        ##  创建节点
        # 图书节点
        bookNode = createBookNode(graphConn,bookData[:-3],labels[:-3])
        # 作者节点(可能有多个作者)
        authorsNode = []
        authorsName = bookData[8].split('&')
        for authorName in authorsName:
            authorNode = createGeneralNode(graphConn,labels[8],authorName)
            authorsNode.append(authorNode)
        # 用户标签节点(可能有多个标签)
        userLabelsNode = []
        userLabels = bookData[9].split('&')
        for userLabelName in userLabels:
            userLabelNode = createGeneralNode(graphConn,labels[9],userLabelName)
            userLabelsNode.append(userLabelNode)
        # 出版社节点
        publisherNode = createGeneralNode(graphConn,labels[10],bookData[10])
        ##  创建关系
        createRelation(graphConn,bookNode,"专业类型标签",createGeneralNode(graphConn,"专业类型标签",tag))
        createRelation(graphConn,bookNode,"出版社",publisherNode)
        for authorNode in authorsNode:
            createRelation(graphConn,bookNode,"作者",authorNode)
            createRelation(graphConn,publisherNode,"拥有",authorNode)

        uselessTitleNode = createGeneralNode(graphConn,"无意义标签","useless"+title)
        for userLabelNode in userLabelsNode:
            createRelation(graphConn,bookNode,"用户标签",userLabelNode)
            # 在生成关系的时候，把所有的用户标签绑定到一个无意义的节点上去
            createRelation(graphConn,uselessTitleNode,"onlyCount",userLabelNode)


def relateTitleAndTags(graphConn,title,tags):
    titleNode = createGeneralNode(graphConn,"专业类型标签",title)
    for tag in tags:
        tagNode = createGeneralNode(graphConn, "专业类型标签", tag)
        createRelation(graphConn,titleNode,"包含",tagNode)

# 这个完全是补丁，前面的代码createNeo4jByCsv写掉了一块
# 功能：更新作者拥有哪些用户标签和专业类型标签
def addAuthorBookTypeRelations(graphConn,title,tag):
    tagNode = createGeneralNode(graphConn, "专业类型标签", tag)
    loadPath = r"../bookData/" + title + "/book-list-" + tag + ".csv"
    csvData = getCsv(loadPath)
    labels = csvData[0]
    for bookData in csvData[1:]:
        # 作者节点(可能有多个作者)
        authorsNode = []
        authorsName = bookData[8].split('&')
        for authorName in authorsName:
            authorNode = createGeneralNode(graphConn, labels[8], authorName)
            authorsNode.append(authorNode)

        # 用户标签节点(可能有多个标签)
        userLabelsNode = []
        userLabels = bookData[9].split('&')
        for userLabelName in userLabels:
            userLabelNode = createGeneralNode(graphConn, labels[9], userLabelName)
            userLabelsNode.append(userLabelNode)

        for authorNode in authorsNode:
            for userLabelNode in userLabelsNode:
                createRelation(graphConn, authorNode, "被标记", userLabelNode)
            createRelation(graphConn, authorNode, "被标记", tagNode)


