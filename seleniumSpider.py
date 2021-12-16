from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from fake_useragent import UserAgent
import requests

def askURL2(url):
    ua = UserAgent()
    headers = {"User-Agent": ua.random, "Connection": 'close'}
    # 请求网站资源
    while(1):
        try:
            requests.adapters.DEFAULT_RETRIES = 5
            html = requests.post(url=url, headers=headers)
            html.content.decode("utf-8")
            return html
        except requests.exceptions.ConnectionError:
            requests.status_code = "Connection refused"
            print("http wrong")
            continue
# 爬取作者信息
def getAuthorData():
    baseUrl = "https://search.douban.com/book/subject_search?search_text=曹雪芹&cat=1001"
    html = askURL2(baseUrl)
    # <a href="https://book.douban.com/author/4508611/" data-moreurl="" class="title-text">曹雪芹 Xueqin Cao</a>
    findAuthorURL = re.compile(r'<a href="(.*?)" data-moreurl="" class="title-text">')
    html.content.decode("utf-8")
    authorURL = re.findall(findAuthorURL,html.text)
    print(authorURL)
    # print(html.text)
    return

if __name__ == "__main__":
    # 加上参数，禁止 chromedriver 日志写屏
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 这里指定 options 参数
    driver = webdriver.Chrome(r"D:\ChromeDriver\chromedriver.exe", options=options)

    driver.get("https://search.douban.com/book/subject_search?search_text=曹雪芹&cat=1001")
    elem = driver.find_element(By.CLASS_NAME, "title-text")
    html = driver.page_source
    print(html)
    driver.quit()