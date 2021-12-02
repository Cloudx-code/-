import csv
import pandas as pd
import requests
import re
from fake_useragent import UserAgent
#爬取信息并存入
def getBookTypeInfo():
    savepath = "F:\文献（看完）\论文\爬虫\豆瓣读书Top250.csv"
    res = getCsv(savepath)
    data = []
    j=1
    for i in res[1:]:
        #对每个i做操作
        bookType = getBookType(i[0])
        if len(bookType)<=0:
            bookTypeStr=" "
            print(i[2],"bookType获取有误!!!!!")
        else:
            bookTypeStr = ""+bookType[0]
            for k in bookType[1:]:
                bookTypeStr+=" "+k
        data.append(bookTypeStr)
        print("第",j,"个ok")
        j+=1

    # with open("豆瓣读书Top250bookType.csv", "w", encoding="utf-8") as f:
    #     for i in data:
    #         print(i)
    #         print(type(i))
    #         f.write(i+"\n")

    return data

# 通过爬虫爬取数据
def getBookType(bookUrl):
    #对应的正则匹配
    findTheme = re.compile(r'<a class="  tag" href="/tag/.*?">(.*?)</a>')
    ua = UserAgent()
    header = {"User-Agent": ua.random, "Connection": 'close'}
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        rsp = requests.get(bookUrl, headers=header)
        rsp.content.decode("utf-8")
        # type(result):list
        result = re.findall(findTheme, rsp.text)
        return result
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"
        print("http wrong")
        try:
            rsp = requests.get(bookUrl, headers=header)
            rsp.content.decode("utf-8")
            # type(result):list
            result = re.findall(findTheme, rsp.text)
            return result
        except requests.exceptions.ConnectionError:
            print("still http wrong")
            return ["error"]



# 读取csv
def getCsv(savepath):
    res = []
    with open(savepath, 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        res.append(headers)
        for row in f_csv:
            res.append(row)
    return res

def getAuthorInfo():
    savepath = "F:\文献（看完）\论文\爬虫\豆瓣读书Top250.csv"

    res = getCsv(savepath)
    data = []
    for i in res[1:]:
        # print("第", j, "条信息是：", end="")
        list = i[7].split(" ")
        # print(list, len(list[0]))
        if list[0][0] == '(':
            if list[0].endswith(')'):
                data.append(list[1])
            else:
                n = list[0].index(')')
                data.append(list[0][n + 1:])
        elif list[0][0] != '[' or list[0].endswith("]") != True:
            if list[0][0] == '[':
                n = list[0].index(']')
                data.append(list[0][n + 1:])
            else:
                data.append(list[0])
        else:
            data.append(list[1])

    return data

def addAuthorInfoToCsv():
    authorInfo = getAuthorInfo()
    res = pd.read_csv("F:\文献（看完）\论文\爬虫\豆瓣读书Top250.csv")
    # print(res.columns)  # 获取列索引值
    # 将新列的名字设置为作者
    res['作者'] = authorInfo
    # # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
    res.to_csv(r"F:\文献（看完）\论文\爬虫\豆瓣读书Top250带作者.csv", mode='a', index=False)

def addBookTypeInfoToCsv():
    bookTypeInfo = getBookTypeInfo()
    res = pd.read_csv("F:\文献（看完）\论文\爬虫\豆瓣读书Top250带作者.csv")
    # print(res.columns)  # 获取列索引值
    # 将新列的名字设置为作者
    res['图书类别'] = bookTypeInfo
    # # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
    res.to_csv(r"F:\文献（看完）\论文\爬虫\豆瓣读书Top250bookType1.csv", mode='a', index=False)

if __name__ == "__main__":
    addBookTypeInfoToCsv()
    print(1)