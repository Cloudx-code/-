import re
import requests
from REModule import findLink,findImgSrc,findTitle,findRating,findJudge,findEnName,findInq,findBd
from util.spiderUtil import getFakeHeader
import numpy as np
import time

#根据图书类型获取图书数据
def getBookDataByTag(bookTag:str):
    response = requests.get(r"https://book.douban.com/tag/"+bookTag, headers=getFakeHeader())
    html = response.text
    print(html)
    findLink = re.compile(r'<a class="nbg" href="(.*?)" onclick')
    linkList = re.findall(findLink,html)
    print(linkList)

if __name__ == '__main__':
    # time.sleep(np.random.rand() * 5)
    getBookDataByTag("神经网络")