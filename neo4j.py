
from CN_DBpedia import getTripleInfoFromCN_DB
from neo4jUtil import getNeo4jConn,createRelation,createMasterNode,createSlaveNode,\
    whetherNodeExist,getNeo4jNode,whetherRelationshipExist
from csvUtil import getCsv
# match (n) detach delete n
# 删库

# 通过CN_DB扩充数据
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
        node2 = createSlaveNode(graphConn,"CN_DB",str(node2Info))
        if createRelation(graphConn,node1,str(relationship),node2):
            j+=1
    return j
#从CSV中创建节点与关系
def createNodeAndRelationFromCsv(graphConn,tableName,i):
    j=0
    # # 1.书籍链接详情
    # createSlaveNode(graphCon, str(tableName[0]), str(i[0]))
    # # 2.图片链接
    # createSlaveNode(graphCon, str(tableName[1]), str(i[1]))
    # 3.图书中文名,node = Node(label,name = name,书籍链接=bookInfo,图片链接=picInfo,相关信息=relatedInfo)
    masterNode = createMasterNode(graphConn, str(tableName[2]), str(i[2]), str(i[0]), str(i[1]), str(i[7]))
    # 4.评分
    slaveNode1 = createSlaveNode(graphConn, str(tableName[4]), str(i[4]))
    # 5.评价数
    slaveNode2 = createSlaveNode(graphConn, str(tableName[5]), str(i[5]))
    # 6.概况
    slaveNode3 = createSlaveNode(graphConn, str(tableName[6]), str(i[6]))
    # # 7.相关信息
    # createSlaveNode(graphCon, str(tableName[7]), str(i[7]))
    # 8.图书别名
    if str(i[3]) != " " and str(i[3]) != '':
        slaveNode4 = createSlaveNode(graphConn, str(tableName[3]), str(i[3]))
        if createRelation(graphConn, masterNode, str(tableName[3]), slaveNode4):
            j += 1
    # 作者,若作者节点不存在，则创建节点，若存在则只创建关系
    slaveNode5 = createSlaveNode(graphConn, str(tableName[8]), str(i[8]))
    # 创建关系
    # 作者与书籍
    if createRelation(graphConn, slaveNode5, str(tableName[8]), masterNode):
        j += 1
    # 书籍与评分
    if createRelation(graphConn, masterNode, str(tableName[4]), slaveNode1):
        j += 1
    # 书籍与评价数
    if createRelation(graphConn, masterNode, str(tableName[5]), slaveNode2):
        j += 1
    # 书籍与概况
    if createRelation(graphConn, masterNode, str(tableName[6]), slaveNode3):
        j += 1
    # 补上拓展的BookType信息

    return j
# 核心函数代码
def createNodeAndRelation(graphConn, csvData):
    # Csv列名
    tableName = csvData[0]
    # 统计创建关系次数
    j=1
    # 轮次数
    times = 1
    # 计划重试的关系数据集
    failData = []
    # 默认从1开始
    for i in csvData[1:]:
        print("第",times,"轮,书名:",str(i[2]),"作者:",str(i[8]))
        times+=1
        #将对CSV文件的内容做节点与关系扩充
        j+=createNodeAndRelationFromCsv(graphConn,tableName,i)
        #通过CN_DB扩充
        # 扩充作者信息
        ans = expandDataFromCN_DB(graphConn,getNeo4jNode(graphConn, str(tableName[8]), str(i[8])))
        if type(ans)==type(1):
            j+=ans
        else:
            failData.append(ans)
        # 扩充作品信息
        ans = expandDataFromCN_DB(graphConn,getNeo4jNode(graphConn, str(tableName[2]), str(i[2])))
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

if __name__ == "__main__":
    savepath = r"F:\文献（看完）\论文\爬虫\豆瓣读书Top250带作者.csv"
    # 获取neo4j连接
    graphCon = getNeo4jConn()
    # 读取爬虫数据i
    csvData = getCsv(savepath)
    # 建立节点与关系
    createNodeAndRelation(graphCon, csvData)




