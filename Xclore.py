import json

import bs4
import urllib
from csvUtil import getCsv
import requests
baseUrl = "https://api.xlore.org/query?instances="
bookName = "《红楼梦》"
# bookName = urllib.parse.quote(bookName)
baseUrl += bookName
response = requests.get(baseUrl)
response.encoding="utf-8"
print(response.json())
# savepath = r"F:\文献（看完）\论文\爬虫\test.json"
savepath = r"test.json"
with open(savepath, 'w', encoding='utf-8') as f:
    json.dump(response.json(),f,ensure_ascii=False)
# bookName = "《红楼梦》"
# bookName = urllib.parse.quote(bookName)
# baseUrl += bookName
# request = urllib.request.Request(baseUrl)
# html = ""
#
# try:
#     response = urllib.request.urlopen(request)
#     html = response.read().decode("utf-8")
#     print(1)
#     print(html)
#
# except urllib.error.URLError as e:
#     if hasattr(e, "code"):
#         print(e.code)
#     if hasattr(e, "reason"):
#         print(e.reason)



#
# if __name__ == "__main__":
#     savepath = "F:\文献（看完）\论文\爬虫\豆瓣读书Top250.csv"
#     getCsv(savepath)


