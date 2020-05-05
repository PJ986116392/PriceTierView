import requests, urllib, bs4, re, string
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from DecryptToken import getSearchToken
import json
import numpy as np

def getToken():
    # 从首页获得token，xlstoken
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Cookie': '_uab_collina=158799928489869207697766; Hm_lvt_2d41db31b18b75206ed7c59c33f5c313=1587999285,1588575396; _uab_collina=158800408134736474834968; _rme_=MTUzMzg4ODQyMTM6MTU5MDc2Mzk0NDc3NDo2MDdkYzFmM2ZjMmUzNDBjYTI2YWE2NTNjMDI5MzlkMQ; SESSION=OWE1ZWExNTItNDFlZS00NDAzLWEzMmMtYzZkZTNkMzVjYTY4; Hm_lpvt_2d41db31b18b75206ed7c59c33f5c313=1588598907',
        'Host': 'www.oneyac.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    }
    try:
        resp = requests.get('https://www.oneyac.com/category/1207.html', headers=headers, timeout=30)
        if resp.status_code == 200:
            htmlText = resp.text
            token = re.search('"token": getSearchToken(.*)', htmlText).group(0).split(',')[1][:-1]
            xlsToken = re.search('"xlsToken": getSearchToken(.*)', htmlText).group(0).split(',')[1][:-2]
            return token,xlsToken
    except:
        print("请求超时")
        exit()

def gethtmltext(Request_method, url, cookie_str, **Others_data):  # Others_data包括请求数据，请求头
    # 处理cookies
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    # Other_data = {'Referer':'参考链接','User-Agent':'模拟浏览器版本','Requests_data':'请求体内容','pdfpath':'pdf文件完整路径'}
    if Request_method == "get":
        try:
            #url = quote(url, safe=string.printable)
            resp = requests.get(url, headers=Others_data, cookies=cookies, timeout=30)
            if resp.raise_for_status == 200:
                return resp.text
        except:
            print("请求超时")
            return ''
    else:
        print("请求方式有误")
        return ""


if __name__ == '__main__':

    #从首页web获取原始未加密的token，xlsToken
    webToken,webXlsToken = getToken()

    #调用js解密token，xlsToken
    token = getSearchToken('sMAvzBVzceaiZIQbZ4cHWEXz1dZ48xkS3zqEyJwQnyKU9ukY9G')
    xlsToken = getSearchToken('Kldi3QoWtOyim2ZQ27ZhCM7sA0M7zS0Xo7cyzgramnPEVR85SN')

    #规格参数
    LIST_FORM = {
        #"aggFields":"brand",
        #"page":0,
        #"pageSize":10,
        #"supplierId": "1",
        #"categoryId": "1223",
        #"keyword": "",
        #"brand_id_filters[]": [],
        #"agg_attr_name_filters[]": ["封装/外壳", "容值", "偏差", "电压", "温度系数(材质)"],
        "token": token,
        "xlsToken": xlsToken
        # "attr_封装/外壳[]": ["0402"], "attr_容值[]": ["100nF"], "attr_偏差[]": ["±20%"], "attr_电压[]": ["16V"],
        # "attr_温度系数(材质)[]": ["X7R"]},
    }
    #Query_String = json.dumps(LIST_FORM)
    #print(Query_String)
    jQueryStr = urlencode(LIST_FORM)
    jQueryStr = jQueryStr.replace('=','%22%3A%22')
    jQueryStr = jQueryStr.replace('&','%22%2C%22')
    jQueryStr = jQueryStr.replace('%21','!')
    print(jQueryStr)
    cookie_str = r'Hm_lvt_2d41db31b18b75206ed7c59c33f5c313=1587202643,1587204715; Hm_lpvt_2d41db31b18b75206ed7c59c33f5c313=1587205027'
    #searchUrl = 'https://soic.oneyac.com/search?callback=jQuery112405999930967327716_1588598361153&paramsDTO=%7B%22' + jQueryStr + '%22%7D'
    #print(searchUrl)
    searchUrl = 'https://soic.oneyac.com/search?callback=jQuery112405999930967327716_1588598361153&paramsDTO=%7B%22aggFields%22%3A%22brand%22%2C%22page%22%3A%220%22%2C%22pageSize%22%3A10%2C%22supplierId%22%3A%221%22%2C%22categoryId%22%3A%221207%22%2C%22keyword%22%3A%22%22%2C%22brand_id_filters%5B%5D%22%3A%5B%5D%2C%22agg_attr_name_filters%5B%5D%22%3A%5B%22%E5%B0%81%E8%A3%85%2F%E5%A4%96%E5%A3%B3%22%2C%22%E5%AE%B9%E5%80%BC%22%2C%22%E5%81%8F%E5%B7%AE%22%2C%22%E7%94%B5%E5%8E%8B%22%5D%2C%22' \
                'token%22%3A%22on%40hol11JzzLOvPKpd8!xm%40ZjzGXNN9M2PYv1alI1wynohPtAHBG0KSH0SfBDWZxgyYeyac%24der%22%2C%22xlsToken%22%3A%22on%40hol11dJzmZmaABQZ!xm%40K5O3ZAxVS2xDCcfw21wynofGPyCLTSi1q9iGAlPBIY0Seyac%24der%22%7D' \
                '&_=1588598361154'

    headers = {
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Connection':'keep - alive',
                'Host': 'soic.oneyac.com',
                'Referer': 'https://www.oneyac.com/category/1223.html',
                'Sec-Fetch-Dest':'script',
                'Sec - Fetch - Mode':'no - cors',
                'Sec - Fetch - Site':'same - site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
               }
    result = gethtmltext('get',searchUrl,cookie_str,**headers)
    print(result)

