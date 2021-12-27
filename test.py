import re
import requests
import urllib3
urllib3.disable_warnings()

if __name__ == "__main__":
    # listN = []
    # strl = "理查德·费曼 弗里德利希・冯・哈耶克 阿来 凑佳苗 罗素 岸见一郎 尼尔·波兹曼 紫金陈 彼得·德鲁克 高野和明 理查德·格里格 保罗·卡拉尼什 刘亮程 罗宾德拉纳特·泰戈尔 桐华"
    # listN = strl.split(" ")
    # print(listN)
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64)"
                      " AppleWebKit / 537.36(KHTML, likeGecko)"
                      " Chrome / 94.0.4606.81 Safari / 537.36"

    }
    proxy={
        'http':"http://27.153.140.126:64256",
        'https':"https://27.153.140.126:64256"
    }
    html = requests.get(r"https://www.kuaidaili.com/free/",headers =  head,proxies=proxy).text

    # <td data-title="IP">220.168.52.245</td>
    findIP = re.compile('<td data-title=\"IP\">(.*?)</td>')
    IPs = re.findall(findIP,html)
    for ip in IPs:
        print(ip)
        try:
            proxys = {
                'http':"http://"+ip,
                'https':"https://"+ip
            }
            html = requests.get("https://www.baidu.com/",headers=head,proxies=proxys)
            print(html.text)
            break
        except Exception as e:
            print(e)
            continue






