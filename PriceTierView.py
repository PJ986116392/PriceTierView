import requests, urllib, bs4, re, string
from bs4 import BeautifulSoup
from urllib.parse import quote
import os
import numpy as np

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
            resp.raise_for_status()
            print(resp.text)
        except:
            print("请求超时")
            return ''
    else:
        print("请求方式有误")
        return ""

if __name__ == '__main__':
    cookie_str = r'Hm_lvt_2d41db31b18b75206ed7c59c33f5c313=1587202643,1587204715; Hm_lpvt_2d41db31b18b75206ed7c59c33f5c313=1587205027'
    Query_String = {
                    'callback':'jQuery',
                    'paramsDTO': {  "aggFields": "brand", "page": 0, "pageSize": 10, "supplierId": "1", "categoryId": "1223",
                                    "keyword": "", "brand_id_filters[]": [],
                                    "agg_attr_name_filters[]": ["封装/外壳", "容值", "偏差", "电压", "温度系数(材质)"],
                                    "token": "on@hol11kkonrpxsp50!xm@bkkskhn91mrekirsz1wynot792y77ik3llw1luw9h6d6eyac$der",
                                    "xlsToken": "on@hol11y8exnb6bk66!xm@xnm0le0to0jktij571wyno09lfahgqd0ls80js6hnr34eyac$der",
                                    "attr_封装/外壳[]": ["0402"], "attr_容值[]": ["100nF"], "attr_偏差[]": ["±20%"], "attr_电压[]": ["16V"],
                                    "attr_温度系数(材质)[]": ["X7R"]},
                    '_':'1587643656390'
                    }
    Str = urlencode(Query_String)
    print(Str)

    url = 'https://soic.oneyac.com/search?' + urlencode(Query_String)
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
    gethtmltext('get',url,cookie_str,**headers)