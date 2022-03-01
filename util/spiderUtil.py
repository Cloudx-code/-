from fake_useragent import UserAgent
import random
import sys
# sys.path.append(r'F:\文献（看完）\论文\爬虫2\util')
sys.path.append(r'..\util')

def getFakeHeader():
    ua = UserAgent()
    headers = {"User-Agent": ua.random,"Connection": 'close'}
    return headers

def wheTherProxies():
    # 返回0表示不启用，1表示启用
    proxyFlag = 0
    return proxyFlag

def getRandomProxies():
    ip = getRandomIp()
    proxies = {
        "http": ip,
        "https": ip
    }
    return proxies

def getAllIP():
    # with open(r"F:\文献（看完）\论文\爬虫2\util\ip.txt","r") as f:
    with open(r"..\util\ip.txt","r") as f:
        a = f.read()
        alist = a.split('\n')

    return alist

def getRandomIp():
    allIP = getAllIP()
    randomIP = allIP.pop(random.randint(0, len(allIP) - 1))
    return randomIP