from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher

# neo4j操作
def getNeo4jConn():
    return Graph('http://localhost:7474',auth=('neo4j', '2019123224'))

# 输入图连接，标签名，和数据库中显示名
def createSlaveNode(graphConn, label, name):
    node = getNeo4jNode(graphConn, label, name)
    if whetherNodeExist(node):
        return node
    node= Node(label,name=name)
    graphConn.create(node)
    return node
#书籍名
def createMasterNode(graphConn,label,name,bookInfo,picInfo,relatedInfo):
    node = getNeo4jNode(graphConn, label, name)
    if whetherNodeExist(node):
        return node
    node = Node(label,name = name,书籍链接=bookInfo,图片链接=picInfo,相关信息=relatedInfo)
    graphConn.create(node)
    return node

def createRelation(graphConn,node1,relation,node2):
    if whetherRelationshipExist(graphConn,node1,relation,node2):
        return False
    node1_relation_node2 = Relationship(node1,relation,node2)
    graphConn.create(node1_relation_node2)
    # print(node1.get("name"),relation,node2.get("name"))
    return True

def whetherRelationshipExist(graphConn,node1,relation,node2):
    relationshipMatcher = RelationshipMatcher(graphConn)
    relationship = list(relationshipMatcher.match((node1, node2), r_type=relation))
    if len(relationship)==0:
        return False
    return True

def whetherNodeExist(node):
    if node==None:
        return False
    return True

def getNeo4jNode(graphConn,label,name):
    nodeMatcher = NodeMatcher(graphConn)
    return nodeMatcher.match(label).where(name=name).first()


