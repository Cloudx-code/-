import csv
import pandas as pd
import requests
import re
import time
import numpy as np
from util.spiderUtil import wheTherProxies,getRandomProxies
# 不加的话会出路径问题（简直莫名其妙）
import sys
sys.path.append(r'F:\文献（看完）\论文\爬虫2\spider')

from spider.bookSpider import getPublisherByURL
import spider.bookSpider

#爬取信息并存入
def getBookLabelInfo(savePath):
    res = getCsv(savePath)
    data = []
    j = 1

    proxies = getRandomProxies()
    for i in res[1:]:
        # Csv的第一列是书籍详情链接，第三列是书名
        bookDetail = i[0]
        bookName = i[2]
        #对每个书籍链接做操作,获取失败则循环获取

        if wheTherProxies()==1:
            while(1):
                print('当前ip为：',proxies['http'])
                try:
                    bookLabel = getBookLabel(bookDetail,proxies)
                    print(bookLabel)
                    break
                except Exception as e:
                    print(e)
                    print("更换ip")
                    proxies = getRandomProxies()

        else:
            try:
                bookLabel = getBookLabel(bookDetail)
            except Exception as e:
                print(e)
                print("尝试用代理抢救一下")
                bookLabel = getBookLabel(bookDetail,proxies)

        if len(bookLabel)<=0:
            bookTypeStr=" "
            print(bookName,"bookType获取有误!!!!!")
        else:
            bookTypeStr = ""+bookLabel[0]
            for k in bookLabel[1:]:
                bookTypeStr+="&"+k
        data.append(bookTypeStr)
        print(j,"用户标签：",bookTypeStr,"ok")
        j+=1
    print(savePath,"ok!!!!!!!!!!!!!!!!!!!!\n\n\n")
    return data

# 通过爬虫爬取数据
def getBookLabel(bookUrl:str,proxies:dict={}):
    #对应的正则匹配
    findTheme = re.compile(r'<a class="  tag" href="/tag/.*?">(.*?)</a>')
    requests.adapters.DEFAULT_RETRIES = 5

    if 'http' in proxies:
        rsp = requests.get(bookUrl, headers=spider.bookSpider.getFakeHeader(),proxies=proxies)
    else:
        # 不用代理的话需要短暂的停一下，用代理则不用
        time.sleep(np.random.rand() * 5)
        rsp = requests.get(bookUrl, headers=spider.bookSpider.getFakeHeader())
    if rsp.status_code!=200:
        raise Exception("访问失败，status_code不等于200")
    rsp.content.decode("utf-8")
    result = re.findall(findTheme, rsp.text)
    return result


# loadPath:读取相应Csv，savePath:存Csv，仅适用于后面爬取的文件，不适用于之前的top250
def addBookLabelInfoToCsv(loadPath, savePath):
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
        print("第", j, "条信息是：",chaosData)
        j+=1
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
        author = author.replace('〕',']')
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

# 添加出版社信息到Csv
def addPublisherToCsv(loadPath,savePath):
    publisherInfo = getPublisherInfo(loadPath)
    res = pd.read_csv(loadPath)
    # print(res.columns)  # 获取列索引值
    # 将新列的名字设置为作出版社
    res['出版社'] = publisherInfo
    # # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
    res.to_csv(savePath, mode='w', index=False)

# 获取出版社信息,# [西] 圣地亚哥·拉蒙-卡哈尔 / 严青、傅贺(校) / 湖南科学技术出版社 / 2020-11 / 148.00元
def getPublisherInfo(loadPath):
    # 获取book-list中的出版社相关信息
    publicationInfo = getOneRowInCsv(loadPath, 6)
    bookURLs = getOneRowInCsv(loadPath, 0)
    data = []
    j=1
    # 获取一群未处理的作者信息，现在想处理成全中文，并用"&"分隔不同作者
    proxies = getRandomProxies()
    for info,bookURL in zip(publicationInfo[1:],bookURLs[1:]):
        print("处理第",j,"个数据",end=" ")
        j+=1
        publisher = analyzingPublisherData(info)
        if publisher==" ":
            print("尝试通过URL获取一下")
            if wheTherProxies()==1:
                while 1:
                    try:
                        publisher = getPublisherByURL(bookURL,proxies)
                        break
                    except Exception as e:
                        print(e)
                        print("失败，重试换IP")
                        proxies = getRandomProxies()
            else:
                publisher = getPublisherByURL(bookURL)
        print(publisher)
        data.append(publisher)
    return data



# 分析已爬取的CSV中是否可以直接提取出出版社信息，返回” “表示没找到
def analyzingPublisherData(info):
    chaosData = info.split('/')
    result = " "
    for data in chaosData:
        if data.find("出版")!=-1 or data.find("Media")!= -1 or data.find("Publish")!=-1:
            if data.find("出版社")!=-1:
                data = re.findall(re.compile(r".*?出版社"),data)[0]
            result = data.strip()
            break
    return result

# [清] 曹雪芹 著   人民文学出版社   1996-12   59.70元
def getPopularBookPublisher():
    loadPath = "../bookData/豆瓣读书Top250bookType.csv"
    publicationInfo = getOneRowInCsv(loadPath, 7)
    bookURLs = getOneRowInCsv(loadPath, 0)
    data = []
    j = 1
    #
    for info, bookURL in zip(publicationInfo[1:], bookURLs[1:]):
        print("处理第", j, "个数据", end=" ")
        j += 1
        publisher = analyzingPopularPublisherData(info)
        if publisher == " ":
            print("尝试通过URL获取一下")
        publisher = getPublisherByURL(bookURL)
        print(publisher)
        data.append(publisher)
    return data

# 分析最受欢迎的250本书籍信息
def analyzingPopularPublisherData(info):
    chaosData = info.split(' ')
    result = " "
    print(len(chaosData))
    for data in chaosData:
        if data.find("出版")!=-1 or data.find("Media")!= -1 or data.find("Publish")!=-1:
            if data.find("出版社")!=-1:
                data = re.findall(re.compile(r".*?出版社"),data)[0]
            result = data.strip()
            break
    return result

# 添加出版社信息到Csv
def addPopularPublisherToCsv(loadPath,savePath):
    publisherInfo = getPopularBookPublisher()
    res = pd.read_csv(loadPath)
    # print(res.columns)  # 获取列索引值
    # 将新列的名字设置为作出版社
    res['出版社'] = publisherInfo
    # # mode=a，以追加模式写入,header表示列名，默认为true,index表示行名，默认为true，再次写入不需要行名
    res.to_csv(savePath, mode='w', index=False)




if __name__ == '__main__':

    title = "生活"
    tags = ["旅行"]


    for tag in tags:
        loadPath = r"../bookData/"+title+"/book-list-" + tag+ ".csv"
        savePath = r"../bookData/"+title+"/book-list-" + tag+ ".csv"
        # # 添加作者类型
        # addAuthorInfoToCsv(loadPath=loadPath, savePath=savePath)
        # print(tag, "类型增加作者列执行完毕")
        # 添加用户标签
        addBookLabelInfoToCsv(loadPath=loadPath, savePath=savePath)
        print(tag, "类型增加用户标签执行完毕")
        # 添加出版社
        addPublisherToCsv(loadPath=loadPath, savePath=savePath)
        print(tag, "类型增加出版社执行完毕")

        # bookLabel = getBookLabelInfo(loadPath)
        # res = pd.read_csv(loadPath)
        # for i in range(len(res['用户标签'])):
        #     res['用户标签'].loc[i]=bookLabel[i]
        # res.to_csv(savePath)
