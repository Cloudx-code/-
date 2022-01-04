import csv
import pandas as pd
import requests
import re
from spiderUtil import getFakeHeader
import time
import numpy as np

basePath = r"bookData/"
#爬取信息并存入
def getBookLabelInfo(savePath):
    res = getCsv(savePath)
    data = []
    j = 1
    for i in res[1:]:
        # Csv的第一列是书籍详情链接，第三列是书名
        bookDetail = i[0]
        bookName = i[2]
        #对每个书籍链接做操作
        time.sleep(np.random.rand() * 5)
        bookLabel = getBookLabel(bookDetail)
        if len(bookLabel)<=0:
            bookTypeStr=" "

            print(bookName,"bookType获取有误!!!!!")
        else:
            bookTypeStr = ""+bookLabel[0]
            for k in bookLabel[1:]:
                bookTypeStr+="&"+k
        data.append(bookTypeStr)
        print(j,bookName,"ok")
        j+=1
    print(savePath,"ok!!!!!!!!!!!!!!!!!!!!\n\n\n")
    return data

# 通过爬虫爬取数据
def getBookLabel(bookUrl):
    #对应的正则匹配
    findTheme = re.compile(r'<a class="  tag" href="/tag/.*?">(.*?)</a>')
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        rsp = requests.get(bookUrl, headers=getFakeHeader())
        rsp.content.decode("utf-8")
        result = re.findall(findTheme, rsp.text)
        return result
    except Exception as e:
        print(e)
        print("http wrong")
        try:
            rsp = requests.get(bookUrl, headers=getFakeHeader())
            rsp.content.decode("utf-8")
            # type(result):list
            result = re.findall(findTheme, rsp.text)
            return result
        except requests.exceptions.ConnectionError:
            print("still http wrong")
            return ["error"]

# loadPath:读取相应Csv，savePath:存Csv，仅适用于后面爬取的文件，不适用于之前的top250
def addBookTypeInfoToCsv(loadPath,savePath):
    bookLabelInfo = getBookLabelInfo(loadPath)
    res = pd.read_csv(loadPath)
    # print(res.columns)  # 获取列索引值
    # 设置新列的名字
    res['用户标签'] = bookLabelInfo
    # # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
    res.to_csv(savePath, mode='w', index=False)

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
# 读取csv某一列信息
def getOneRowInCsv(savepath,rows):
    csvData = getCsv(savepath)
    res = []
    for data in csvData:
        res.append(data[rows])
    return res




def saveToCsv(datalist, savepath,headers):
    with open(savepath, 'w',newline="",encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        i= 1
        for data in datalist:
            i+=1
            f_csv.writerow(data)
    print("存入成功!")
    return


# [西] 圣地亚哥·拉蒙-卡哈尔 / 严青、傅贺(校) / 湖南科学技术出版社 / 2020-11 / 148.00元
def getAuthorInfo(savePath):
    # 获取book-list中的出版社相关信息
    publicationInfo = getOneRowInCsv(savePath,6)
    j = 1
    data = []
    # 获取一群未处理的作者信息，现在想处理成全中文，并用"&"分隔不同作者
    for info in publicationInfo[1:]:
        chaosData = info.split('/')[0]
        # print("第", j, "条信息是：",chaosData)
        # j+=1
        fixedData = handleChaosAuthorData(chaosData)
        # print(fixedData)
        data.append(fixedData)
    return data
# 处理单个混乱的作者数据
def handleChaosAuthorData(chaosData:str):
    # authorsData现在表示可能混合国籍与中英文的混合型信息[澳]迈克尔·尼尔森（Michael Nielsen）
    authorsData = chaosData.split('、')
    ans = []
    for author in authorsData:
        # 替换后统一处理，但是这里要注意，中英混合的情况！！！
        author = author.replace('【', '[')
        author = author.replace('［', '[')
        author = author.replace('(', '[')
        author = author.replace('（', '[')
        author = author.replace('】', ']')
        author = author.replace('］', ']')
        author = author.replace(')', ']')
        author = author.replace('）', ']')
        if author.startswith('['):
            author = author[(author.index(']')) + 1:]
        author = author.strip()
        if author.endswith(']'):
            author = author[:author.index('[')]
        ans.append(author.strip())
    return "&".join(ans)
# loadPath:读取相应Csv，savePath:存Csv，仅适用于后面爬取的文件，不适用于之前的top250
def addAuthorInfoToCsv(loadPath,savePath):
    authorInfo = getAuthorInfo(loadPath)
    res = pd.read_csv(loadPath)
    # print(res.columns)  # 获取列索引值
    # 将新列的名字设置为作者
    res['作者'] = authorInfo
    # # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
    res.to_csv(savePath, mode='w', index=False)

if __name__ == '__main__':
    # data = getBookLabel(r"https://book.douban.com/subject/27055156/")
    # for i in data:
    #     print(i)
    # len(data)
    tags = ["科普", "互联网", "科学", "编程", "交互设计", "算法", "用户体验", "web", "交互", "通信", "UE", "神经网络", "UCD", "程序"]
    tags = ["算法", "用户体验", "web", "交互", "通信", "UE", "神经网络", "UCD", "程序"]
    for tag in tags:
        loadPath = r"../bookData/科技/book-list-" + tag + ".csv"
        savePath = r"../bookData/科技/book-list" + tag + ".csv"
        addBookTypeInfoToCsv(loadPath=loadPath, savePath=savePath)
        print(tag, "改进完毕")

