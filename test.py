from neo4jUtil import getNeo4jConn,getNeo4jNode,createRelation,createSlaveNode,whetherRelationshipExist
import csv
from csvUtil import getCsv
import re
import json
import io
import requests

if __name__ == "__main__":
    # listN = []
    # strl = "理查德·费曼 弗里德利希・冯・哈耶克 阿来 凑佳苗 罗素 岸见一郎 尼尔·波兹曼 紫金陈 彼得·德鲁克 高野和明 理查德·格里格 保罗·卡拉尼什 刘亮程 罗宾德拉纳特·泰戈尔 桐华"
    # listN = strl.split(" ")
    # print(listN)
    html = requests.get(r"https://search.douban.com/book/subject_search?search_text=曹雪芹").text
    print(html)





