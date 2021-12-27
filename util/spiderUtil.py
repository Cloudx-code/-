from fake_useragent import UserAgent

def getFakeHeader():
    ua = UserAgent()
    headers = {"User-Agent": ua.random,"Connection": 'close'}
    return headers