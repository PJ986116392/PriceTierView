import requests, urllib, bs4, re, string
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.parse import quote_plus
from DecryptToken import getSearchToken
import json,random
import numpy as np
import time

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
                print(resp.status_code)
                return resp.json()
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
    token = getSearchToken(webToken)
    xlsToken = getSearchToken(webXlsToken)

    # 处理url
    # https://soic.oneyac.com/agg_attr?
    # callback=jQuery1124019459650479182689_1589471189093
    # &paramsDTO={"aggFields":"brand","page":0,"pageSize":10,"supplierId":"1","categoryId":"1207","keyword":"","brand_id_filters[]":[],"agg_attr_name_filters[]":["封装/外壳","容值","偏差","电压"],"token":"on@hol11jiwZeyidrCS!xm@32xqMGUOLLdPJHG7dcK"1wyno"qxlhs8W7YkC4kMZF7V0Jeyac$der","xlsToken":"on@hol11WQ3ZM8JQHuz!xm@5wO7nSIii4OC1EbhePg"1wyno"VmnoQjqhbpLm2hRoLEwceyac$der","attr_封装/外壳[]":["0402"]}
    # &_=1589471189094
    # 由此可以看出，URL分为三个部分
    #   第一部分：searchApi （https://soic.oneyac.com/search?） or aggAttrApi （https://soic.oneyac.com/agg_attr?）
    #   第二部分：回调函数callback
    #   第二部分：元器件请求规格 + token + xlstoken
    #   第三部分：参数_ (多次观看数据，可以猜测为时间秒数)

    # 搜索引擎
    aggAttrApi = 'https://soic.oneyac.com/agg_attr?'
    searchApi = 'https://soic.oneyac.com/search?'
    # 处理时间秒数
    Time = int(time.time()*1000)
    timeStr = '_=' + str(Time)
    # 处理回调函数
    m = '1.12.4'
    callBack = 'callback=jQuery' + m + str(random.uniform(0,1))
    callBackstr = str(callBack).replace('.','') + '_' + str(Time-1)
    #print(callBackstr)

    #规格参数
    specAttr = {
        "aggFields":"brand",
        "page":0,
        "pageSize":10,
        "supplierId": "1",
        "categoryId": "1207",
        "keyword": "",
        "brand_id_filters[]": [],
        "agg_attr_name_filters[]": ["封装/外壳", "容值", "偏差", "电压"],
        "token": token,
        "xlsToken": xlsToken,
        "attr_封装/外壳[]": ["0402"]
        #"attr_封装/外壳[]": ["0402"], "attr_容值[]": ["100nF"], "attr_偏差[]": ["±20%"], "attr_电压[]": ["16V"],
        # "attr_温度系数(材质)[]": ["X7R"]},
    }
    #{"aggFields": "brand", "page": "0", "pageSize": 10, "supplierId": "1", "categoryId": "1207", "keyword": "", "brand_id_filters[]": [], "agg_attr_name_filters[]": ["\u5c01\u88c5/\u5916\u58f3", "\u5bb9\u503c", "\u504f\u5dee", "\u7535\u538b"], "token": "XXX", "xlsToken": "XXX"}
    specAttrstr = json.dumps(specAttr)
    #删除字典更换为字符串后多余的空号
    # agg_attr_name_filters[]中\u5bb9\u503c等字符转为中文
    specAttrstr = specAttrstr.replace(' ','')

    # url:https://blog.csdn.net/u014519194/article/details/53927149
    specAttrstr = specAttrstr.encode('utf-8').decode('unicode_escape')    #python3以上取消了decode，所以你直接想st.decode(“utf-8”)的话会报str没有decode方法的错

    # https://www.cnblogs.com/lu-test/p/9962640.html
    specAttrstr = quote_plus(specAttrstr)             #quote 除了 -._/09AZaz ,都会进行编码。quote_plus 比 quote 『更进』一些，它还会编码 /
    specAttrstr = specAttrstr.replace('%21','!')      #查看原url可知，xlstoken中的’！‘并未被转码，将其转回
    paramsDTO = 'paramsDTO=' + specAttrstr

    url = searchApi + callBackstr + '&' + paramsDTO + '&' + timeStr
    print(url)
    cookie_str = r'Hm_lvt_2d41db31b18b75206ed7c59c33f5c313=1587999285,1588575396; Hm_lpvt_2d41db31b18b75206ed7c59c33f5c313=1588775854'
    headers = {
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection':'keep - alive',
                'Cookie':'Hm_lvt_2d41db31b18b75206ed7c59c33f5c313=1587999285,1588575396,1588775801; Hm_lpvt_2d41db31b18b75206ed7c59c33f5c313=1588775854',
                'Host': 'soic.oneyac.com',
                'Referer': 'https://www.oneyac.com/category/1207.html',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
               }
    try:
        resp = requests.get(url=url,headers = headers)
        if resp.status_code == 200 :
            print(resp.text)
    except:
        print('链接失败')
    #result = gethtmltext('get',searchUrl,cookie_str,**headers)
    #print(result)





