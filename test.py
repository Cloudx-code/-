from neo4jUtil import getNeo4jConn,getNeo4jNode,createRelation,createSlaveNode,whetherRelationshipExist
import csv
from csvUtil import getCsv
import re
import io
findTheme = re.compile(r'<a.*title="(.*?)"')
findTheme = re.compile(r'<a class="  tag" href="/tag/.*?">(.*?)</a>')

if __name__ == "__main__":
    data = getCsv(r"F:\文献（看完）\论文\爬虫\豆瓣读书Top250bookType.csv")

    for i in data[1:]:

        if float(i[4])>9.5:
            print(1)



