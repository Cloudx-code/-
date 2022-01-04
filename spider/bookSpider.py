import re
import requests
from REModule import findLink,findImgSrc,findBookName,findBookScore,findJudgeAmount,findBookNameSupply,findPublicationInfo,findSummary
from util.spiderUtil import getFakeHeader
import numpy as np
import time
from bs4 import BeautifulSoup
from util.csvUtil import saveToCsv

#根据图书类型获取图书数据(可能有多页)
def getBookDataByTag(bookTag:str):
    start = 0
    allBookData = []
    while(1):
        url = r"http://book.douban.com/tag/"+bookTag+"?start=" + str(start)
        time.sleep(np.random.rand() * 5)
        print(url)
        # 获取一份URL的图书信息，并将其存入allBookData中
        oneURLBookData = getOneURLBookData(url)
        for oneBookData in oneURLBookData:
            allBookData.append(oneBookData)
        start+=len(oneURLBookData)
        print("已记录",start,"条数据")
        if len(oneURLBookData) < 20:
            break
    return allBookData


# 获取当前页URL的所有书籍信息。返回一个list,列表的每个元素代表一本书籍的信息
def getOneURLBookData(url:str):
    oneURLBookData = []
    # 1.获取HTML信息
    response = requests.get(url, headers=getFakeHeader())
    html = response.text
    # 2.逐一解析书籍数据
    soup = BeautifulSoup(html,"html.parser")
    for bookItem in soup.find_all('li', class_="subject-item"):
        # 解析一本图书的数据信息，并将其加入到列表中
        try:
            oneBookInfo = parseBookItem(str(bookItem))
            oneURLBookData.append(oneBookInfo)
        except Exception as e:
            print("解析某本书籍信息时出错，出错信息为：",end=" ")
            print(e)
            print(str(bookItem))
            exit()
    return oneURLBookData


# 解析单个HTML中Li包含的书籍信息(一本书的全部信息)，其中许多特殊情况已特殊处理，但是代码会看着有点乱
def parseBookItem(bookItem:str):
    oneBookInfo = []
    # 图书详情链接
    link = re.findall(findLink, bookItem)[0]
    # 图书图片链接
    imgSrc = re.findall(findImgSrc, bookItem)[0]
    # 书名
    try:
        bookName = re.findall(findBookName,bookItem)[0]
    except IndexError:
        bookName = re.findall(re.compile(r"<a.*title='(.*?)'"),bookItem)[0]
    # 书名拓展
    bookNameSupply = re.findall(findBookNameSupply,bookItem)
    if len(bookNameSupply)==0:
        bookNameSupply = " "
    else:
        bookNameSupply = bookNameSupply[0]
    # 评分
    try:
        bookScore = re.findall(findBookScore,bookItem)[0]
    except IndexError:
        bookScore = "暂无"
    # 评价人数
    judgeAmount = re.findall(findJudgeAmount, bookItem)[0]
    # 出版相关信息
    try:
        publicationInfo = re.findall(findPublicationInfo,bookItem)[0]
    except:
        print("publicationInfo err")
        publicationInfo = re.findall(re.compile(r'<div class="pub">\s*(.*\s*.*)\s*</div>'), bookItem)[0]
    # 概况
    summary = re.findall(findSummary,bookItem)
    if len(summary)==0:
        summary = "暂无"
    else:
        summary = summary[0]

    # 添加各项数据
    oneBookInfo.append(link)
    oneBookInfo.append(imgSrc)
    oneBookInfo.append(bookName)
    oneBookInfo.append(bookNameSupply)
    oneBookInfo.append(bookScore)
    oneBookInfo.append(judgeAmount)
    oneBookInfo.append(publicationInfo)
    oneBookInfo.append(summary)
    return oneBookInfo


