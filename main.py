# -*- codeing = utf-8 -*-
# @Time : 2020/3/3 17:51
# @File : spider.py
# @Software: PyCharm

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作

import csv
basePath = r""
def saveToCsv(datalist, savepath):
    headers = ("书籍详情链接", "图片链接", "图书中文名", "图书外国名", "评分", "评价数", "概况", "相关信息")
    with open(savepath, 'w',newline="",encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        i= 1
        for data in datalist:
            print("第",i,"条数据存入ing")
            i+=1
            print(data)
            f_csv.writerow(data)
    return


def main():

    baseurl = "https://book.douban.com/top250?start="
    # baseurl = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=980&type=T"

    # 1.爬取网页

    datalist = getData(baseurl)
    # savepath = "F:\文献（看完）\论文\爬虫\豆瓣读书Top250.csv"
    savepath = basePath+r"豆瓣读书Top250.csv"
    # dbpath = "movie.db"
    print(len(datalist))
    # 3.保存数据
    saveToCsv(datalist,savepath)
    # saveData(datalist, savepath)
    # saveData2DB(datalist,dbpath)

    # askURL("https://movie.douban.com/top250?start=")


# 书籍详情链接的规则
findLink = re.compile(r'<a class="nbg" href="(.*?)" onclick')  # 创建正则表达式对象，表示规则（字符串的模式）
# 书籍图片
findImgSrc = re.compile(r'<img src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
# 书名
findTitle = re.compile(r'<a.*title="(.*?)"')
# 书籍评分
findRating = re.compile(r'<span class="rating_nums">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span class="pl">\(\n                    (.*?)人评价',re.S)

# 英文名：<span style="font-size:12px;">Nineteen Eighty-Four</span>
findEnName = re.compile(r'<span style="font-size:12px;">(.*?)</span>')

# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到书籍的相关内容
findBd = re.compile(r'<p class="pl">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    print("爬数据ing")
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        print("开始爬",i*25,"到",i*25+25,"的信息")
        url = baseurl + str(i * 25)
        try:
            html = askURL(url)  # 保存获取到的网页源码
        except:
            print("重试ing")
            html = askURL(url)  # 保存获取到的网页源码

        # 2.逐一解析数据
        i = 0
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('tr', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)   #测试：查看读书item全部信息
            data = []  # 保存一本书籍的所有信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)  # 添加链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片

            titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，没有外国名

            ctitle = titles[0]  # 添加中文名
            data.append(ctitle)


            otitle = re.findall(findEnName,item)  # 去掉无关的符号
            if len(otitle)==0:
                data.append(' ')
            elif len(otitle)==2:
                data.append(otitle[1])  # 添加外国名
            else:
                if otitle[0][1]==':':
                    data.append(otitle[0][3:])
                else:
                    data.append(otitle[0])

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分

            tables = soup.find_all('table')

            # judgeNum = re.findall(r"\d+", tables[i].find('span', attrs={'class': 'pl'}).text)
            # i+=1
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 提加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append(" ")  # 留空

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格

            datalist.append(data)  # 把处理好的一本图书信息放入datalist

    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64)"
                      " AppleWebKit / 537.36(KHTML, likeGecko)"
                      " Chrome / 94.0.4606.81 Safari / 537.36"

    }

    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据
def saveData(datalist, savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣读书Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("书籍详情链接", "图片链接", "图书中文名", "图书别名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save(savepath)  # 保存
#
# def test1():
#     datalist=[]
#     data=[]
#     data.append('https://book.douban.com/subject/1007305/')
#     data.append('https://img1.doubanio.com/view/subject/s/public/s1070959.jpg')
#     data.append('红楼梦')
#     data.append('[dahsjkdhakdkkjnd] ')
#     data.append('9.6')
#     data.append('351106')
#     data.append('都云作者痴，谁解其中味？')
#     data.append('[清] 曹雪芹 著   人民文学出版社   1996-12   59.70元')
#     data=tuple(data)
#     datalist.append(data)
#     print(datalist)
#     savepath = "F:\文献（看完）\论文\爬虫\豆瓣读书Top250.csv"
#     saveToCsv(datalist,savepath)
#     return

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # test1()
    # init_db("movietest.db")
    print("爬取完毕！")


