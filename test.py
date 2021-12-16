from neo4jUtil import getNeo4jConn,getNeo4jNode,createRelation,createSlaveNode,whetherRelationshipExist
import csv
from csvUtil import getCsv
import re
import json
import io
findTheme = re.compile(r'<a.*title="(.*?)"')
findTheme = re.compile(r'<a class="  tag" href="/tag/.*?">(.*?)</a>')

if __name__ == "__main__":
    listN = []


    with open("authorName.json", "a+", encoding="utf-8") as f:
        # f.write("曹雪芹")
        # f.write("\n")
        # f.write("曹雪芹1")
        # f.write("\n")
        for i in f:
            print(i)
    if "曹雪芹" in listN:
        print(2323)





