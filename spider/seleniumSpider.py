import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from util.csvUtil import getOneRowInCsv,saveToCsv
import json


def getSeleniumDriver():
    # 加上参数，禁止 chromedriver 日志写屏
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 这里指定 options 参数
    driver = webdriver.Chrome(r"D:\chromeDriver\chromedriver.exe", options=options)
    return driver

def getAuthorURL(driver,authorName):
    url = r"https://search.douban.com/book/subject_search?search_text=" + str(authorName)
    driver.get(url)
    # <a href="https://book.douban.com/author/4604358/" data-moreurl="" class="cover-link"><img
    html = driver.page_source
    findURL = re.compile(r'<a href="(.*?)" data-moreurl="" class="cover-link"><img')
    authorURL = re.findall(findURL,html)
    # Selenium自带的方法
    # elem = d.find_element(By.CLASS_NAME, "cover-link")
    # href = elem.get_attribute("href")
    print(authorName,authorURL)
    if authorURL==[]:
        return " "
    return authorURL[0]

def getAuthorsURL(driver,authorsName):
    urlList = []
    for authorName in authorsName:
        times = 0
        while(1):
            try:
                urlInfo = getAuthorURL(driver,authorName)
                urlList.append(urlInfo)
                break
            except:
                print("io wrong")
                times+=1
                if times >= 5:
                    print("重试失败")
                    break
    return urlList

def getAuthorInfo(driver,authorName):
    url = r"https://search.douban.com/book/subject_search?search_text="+str(authorName)
    # driver.implicitly_wait(120)
    driver.get(url)
    driver.find_element(By.CLASS_NAME, "title-text").click()
    elem = driver.find_element(By.CLASS_NAME,"info")
    while elem.text==None:
        driver.get(url)
        driver.find_element(By.CLASS_NAME, "title-text").click()
        elem = driver.find_element(By.CLASS_NAME, "info")
        print("重试ing")
    print("作者: "+authorName+"\n"+elem.text+"\n\n")
    return elem.text



def getAuthorsInfo(driver,authorData):
    # 存储作者列表
    haveStoredList = {}
    haveStoredList["黄元吉"]=""
    haveStoredList["少年儿童出版社"]=""
    # 存储作者信息
    authorTextInfo = []
    # 存储爬取失败的作者
    errAuthorInfo = []
    with open("../bookData/authorName.json", "a+", encoding="utf-8") as f:
        num = 0
        for authorName in authorData:
            if authorName not in haveStoredList:
                times = 1
                while(1):
                    try:
                        text = getAuthorInfo(driver,authorName)
                        authorTextInfo.append("作者: "+authorName+"\n"+text+"\n\n")
                        haveStoredList[authorName] = str(num)
                        num += 1
                        break
                    except:
                        print("some thing wrong")
                        times+=1
                        if times>=5:
                            print("重试次数超过最大值，退出")
                            errAuthorInfo.append(authorName)
                            break


        haveStoredList["num"] = num
        json.dump(haveStoredList, f, ensure_ascii=False)
    with open("../bookData/authorInfo.txt", "a", encoding='utf=8') as f:
        for i in authorTextInfo:
            f.write(i)

    print("信息爬取完毕，爬取失败的作者数量为:"+str(len(errAuthorInfo))+"失败名单为:")
    for errAuthor in errAuthorInfo:
        print(errAuthor,end=" ")
    if len(errAuthorInfo)>=5:
        print("重试ing")
        getAuthorsInfo(errAuthor)



def main():
    # 获得驱动
    driver = getSeleniumDriver()
    #获得作者信息
    authorData = getOneRowInCsv(r"../bookData/豆瓣读书Top250bookType.csv",8)[1:]
    # 爬取信息
    # getAuthorsInfo(driver,authorData)
    authorURL = getAuthorsURL(driver,authorData)
    # 存数据
    saveToCsv(zip(authorData,authorURL),"authorURL.csv",["作者","URL链接"])
    #关闭驱动
    driver.quit()


if __name__ == "__main__":
    main()
    # d = getSeleniumDriver()
    # # <a href="https://book.douban.com/author/4604358/" data-moreurl="" class="cover-link"><img
    # d.get(r"https://search.douban.com/book/subject_search?search_text=曹雪芹")
    # elem = d.find_element(By.CLASS_NAME,"cover-link")
    # href = elem.get_attribute("href")
    # print(href)


