from neo4jUtil import getNeo4jConn,getNeo4jNode,createRelation,createSlaveNode,whetherRelationshipExist
import csv
import re
import io
findTheme = re.compile(r'<a.*title="(.*?)"')
findTheme = re.compile(r'<a class="  tag" href="/tag/.*?">(.*?)</a>')

if __name__ == "__main__":
    str1="红楼梦,古典文学 曹雪芹 经典 古典名著 名著 四大名著 小说"
    str2="红楼梦 古典文学 曹雪芹 经典 古典名著 名著 四大名著 小说"
    # r = csv.reader(io.StringIO(str))
    with open("豆瓣读书Top250bookType.csv", "w", encoding="utf-8") as f:
        # f_csv = csv.writer(f)
        #
        # f_csv.r = csv.reader(io.StringIO(s))(str)
        f.write(str1)


