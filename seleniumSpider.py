from selenium import webdriver
from selenium.webdriver.common.by import By
from csvUtil import getOneRowInCsv
import json
from selenium.webdriver.chrome.options import Options
import re
from fake_useragent import UserAgent
import requests

def getSeleniumDriver():
    # 加上参数，禁止 chromedriver 日志写屏
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 这里指定 options 参数
    driver = webdriver.Chrome(r"E:\chromeDriver\chromedriver.exe", options=options)
    return driver

def getAuthorInfo(driver,authorName):
    url = r"https://search.douban.com/book/subject_search?search_text="+str(authorName)
    driver.get(url)
    driver.find_element(By.CLASS_NAME, "title-text").click()
    elem = driver.find_element(By.CLASS_NAME,"info")
    while elem.text==None:
        driver.get(url)
        driver.find_element(By.CLASS_NAME, "title-text").click()
        elem = driver.find_element(By.CLASS_NAME, "info")
        print("重试ing")
    with open("test.txt","a",encoding='utf=8') as f:
        print("作者: "+authorName+"\n"+elem.text+"\n\n")
        f.write("作者: "+authorName+"\n"+elem.text+"\n\n")


def getAuthorsInfo(driver,authorData):
    with open("authorName.json", "r+", encoding="utf-8") as f:
        haveStoredList = {}
        if "num" not in haveStoredList:
            num = 0
        else:
            num = int(haveStoredList["num"])

        for authorName in authorData:
            if authorName not in haveStoredList:
                while(1):
                    try:
                        getAuthorInfo(driver,authorName)
                        break
                    except:
                        print("some thing wrong")
                        driver.wa

                haveStoredList[authorName]=str(num)
                num+=1
        haveStoredList["num"] = num
        json.dump(haveStoredList, f, ensure_ascii=False)

def main():
    # 获得驱动
    driver = getSeleniumDriver()
    #获得作者信息
    authorData = getOneRowInCsv(r"豆瓣读书Top250bookType.csv",8)[1:]
    # 爬取信息
    getAuthorsInfo(driver,authorData[0:5])
    #关闭驱动
    driver.quit()


if __name__ == "__main__":
    main()


