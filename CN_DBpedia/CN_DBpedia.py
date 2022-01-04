import requests
from util.spiderUtil import getFakeHeader


def getTripleInfoFromCN_DB(name):
    # 获取伪装的header
    baseUrl = "http://47.100.22.113:80/api/cndbpedia/avpair?q="
    # 7d8d6d03699ea8e22affc4ff1bf27bc
    url = baseUrl+name+"&apikey=7d8d6d03699ea8e22affc4ff1bf27bc"

    # 请求网站资源
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        html = requests.get(url=url, headers=getFakeHeader())
        html.content.decode("utf-8")
    except requests.exceptions.ConnectionError:
        requests.status_code = "Connection refused"
        print("http wrong")
        return ["http wrong"]

    dictHtml = html.json()
    # 转换后，retInfo的格式是一个二维数组，list:list:["relationship","node2"]
    retInfo = dictHtml['ret']
    # print(retInfo)
    # for i in retInfo:
    #     for j in i:
    #         print(j,end="")
    #     print()
    return retInfo


if __name__ == "__main__":
    getTripleInfoFromCN_DB("金庸")