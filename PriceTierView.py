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
        'Cookie':'_uab_collina=158799928489869207697766; Hm_lvt_2d41db31b18b75206ed7c59c33f5c313=1588864465,1588951959,1589381005,1589468101; _uab_collina=158800408134736474834968; _rme_=MTUzMzg4ODQyMTM6MTU5MDc2Mzk0NDc3NDo2MDdkYzFmM2ZjMmUzNDBjYTI2YWE2NTNjMDI5MzlkMQ; SESSION=N2Y3ZWUwMDYtMDdjYy00NGU2LWE5N2YtZTQyZDEyYWY2ZDcz; Hm_lpvt_2d41db31b18b75206ed7c59c33f5c313=1589469656',
        'Host': 'www.oneyac.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    }
    try:
        resp = requests.get('https://www.oneyac.com/category/1207.html', headers=headers, timeout=30)
        if resp.status_code == 200:
            htmlText = resp.text
            token = re.search('"token": getSearchToken(.*)', htmlText).group(0).split(',')[1][2:-2]
            xlsToken = re.search('"xlsToken": getSearchToken(.*)', htmlText).group(0).split(',')[1][2:-3]
            return token,xlsToken
    except:
        print("token请求超时")
        exit()

def getUrl(api,specAttr):
    # 处理url
    # https://soic.oneyac.com/agg_attr?
    # callback=jQuery1124019459650479182689_1589471189093
    # &paramsDTO={"aggFields":"brand","page":0,"pageSize":10,"supplierId":"1","categoryId":"1207","keyword":"","brand_id_filters[]":[],"agg_attr_name_filters[]":["封装/外壳","容值","偏差","电压"],"token":"on@hol11jiwZeyidrCS!xm@32xqMGUOLLdPJHG7dcK"1wyno"qxlhs8W7YkC4kMZF7V0Jeyac$der","xlsToken":"on@hol11WQ3ZM8JQHuz!xm@5wO7nSIii4OC1EbhePg"1wyno"VmnoQjqhbpLm2hRoLEwceyac$der","attr_封装/外壳[]":["0402"]}
    # &_=1589471189094
    # 由此可以看出，URL分为三个部分
    #   第一部分：searchApi （https://soic.oneyac.com/search?） or aggAttrApi （https://soic.oneyac.com/agg_attr?）
    #   第二部分：回调函数callback
    #   第三部分：元器件请求规格 + token + xlstoken
    #   第四部分：参数_ (多次观看数据，可以猜测为时间秒数)

    # 第四个参数：时间函数
    Time = int(time.time() * 1000)
    timeStr = '_=' + str(Time)
    #timeStr = '_=1589698385688'
    # 第二个参数：回调函数
    m = '1.12.4'
    callBack = 'callback=jQuery' + m + str(random.uniform(0, 1))
    callBackstr = str(callBack).replace('.', '') + '_' + str(Time - 3)
    #callBackstr = 'callback=jQuery112404027800660922535_1589698385685'


    # 第三个参数：aggAttr
    aggAttr = specAttr

    # {"aggFields": "brand", "page": "0", "pageSize": 10, "supplierId": "1", "categoryId": "1207", "keyword": "", "brand_id_filters[]": [], "agg_attr_name_filters[]": ["\u5c01\u88c5/\u5916\u58f3", "\u5bb9\u503c", "\u504f\u5dee", "\u7535\u538b"], "token": "XXX", "xlsToken": "XXX"}
    aggAttrstr = json.dumps(aggAttr)

    # 删除字典更换为字符串后多余的空号
    aggAttrstr = aggAttrstr.replace(' ', '')

    # agg_attr_name_filters[]中\u5bb9\u503c等字符转为中文,参考url:https://blog.csdn.net/u014519194/article/details/53927149
    aggAttrstr = aggAttrstr.encode('utf-8').decode('unicode_escape')  # python3以上取消了decode，所以你直接想st.decode(“utf-8”)的话会报str没有decode方法的错

    # url 编码，参考url：https://www.cnblogs.com/lu-test/p/9962640.html
    aggAttrstr = quote_plus(aggAttrstr)  # quote 除了 -._/09AZaz ,都会进行编码。quote_plus 比 quote 『更进』一些，它还会编码 /
    aggAttrstr = aggAttrstr.replace('%21', '!')  # 查看原url可知，xlstoken中的’！‘并未被转码，将其转回

    paramsDTO = 'paramsDTO=' + aggAttrstr

    url = api + callBackstr + '&' + paramsDTO + '&' + timeStr
    return url

def getJosn(api, specAttr):
    '''
    :param api:             url 链接
    :param specAttr:        元器件规格
    :return:
    如果api是搜索电容价格并且元器件参数正确，返回价格最低的品牌电容的相关信息（字典）
    如果api是过滤元器件参数，则返回过滤结果（字典）
    '''
    url= getUrl(api, specAttr)

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep - alive',
        'Cookie': 'Hm_lvt_2d41db31b18b75206ed7c59c33f5c313=1588864465,1588951959,1589381005,1589468101; Hm_lpvt_2d41db31b18b75206ed7c59c33f5c313=1589698387',
        'Host': 'soic.oneyac.com',
        'Referer': 'https://www.oneyac.com/category/1207.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    }
    try:
        resp = requests.get(url=url, headers=headers)
        if resp.status_code == 200 and 'search' in url:
            #print(resp.text)
            Json = loads_jsonp(resp.text)
            result = Json['page']['content'][0]
            return result
        elif resp.status_code == 200 and 'agg' in url:
            Json = loads_jsonp(resp.text)
            result = Json['filterConditions']
            return result
    except:
        print('获取价格失败')
        exit()

def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
    except:
        raise ValueError('Invalid Input')

def specJudgment(aggAttrApi,capacitance,package,voltage,accuracy):
    # 初始化封装
    initPackage = ['0201','0402','0603','0805','1206']
    specAttr = {
        "aggFields": "brand",
        "page": 0,
        "pageSize": 10,
        "supplierId": "1",
        "categoryId": "1207",
        "keyword": "",
        "brand_id_filters[]": [],
        "agg_attr_name_filters[]": ["封装/外壳", "容值", "偏差", "电压"],
        "token": 'on@hol113ekipbgatp2!xm@cn4oe5t6pubg4rgj61wynozdd9jxhqmcoe4lo3oxwbiheyac$der',
        "xlsToken": 'on@hol11ywj5da0witd!xm@533x09zspzeosto9q1wynozi33ezuo547d14w73dz6deeyac$der'
    }

    # 检查封装
    if package not in initPackage :
        msgbox = '电容封装有误（不是0201，0402，0603，0805，1206物料）'
        return False,msgbox
    specAttr.update({"attr_封装/外壳[]": [package]})
    filterConditions = getJosn(aggAttrApi, specAttr)

    # 检查封装 + 电压
    if voltage not in filterConditions['电压']:
        msgbox = '电容电压有误，正确电压' + str(filterConditions['电压'])
        return False,msgbox
    specAttr.update({"attr_电压[]": [voltage]})
    filterConditions = getJosn(aggAttrApi, specAttr)

    # 检查封装 + 电压 + 偏差
    if accuracy not in filterConditions['偏差']:
        msgbox = '电容偏差有误，正确偏差' + str(filterConditions['偏差'])
        return False, msgbox
    specAttr.update({"attr_偏差[]": [accuracy]})
    filterConditions = getJosn(aggAttrApi, specAttr)
    # 检查封装 + 电压 + 偏差 + 容量
    if capacitance not in filterConditions['容值']:
        msgbox = '电容容值有误，正确容值' + str(filterConditions['容值'])
        return False,msgbox
    else:
        msgbox = '电容规格正确!'
        return True, msgbox


def getPrice(orderCount,capacitance,package,voltage,accuracy):
    '''
    从唯详商城获取指定电容最低价格
    :param orderCount:      采购数量
    :param capacitance:     电容容量
    :param package:         电容封装
    :param voltage:         电容耐压
    :param accuracy:        电容精度
    :return:返回值
    productPrice = {
        'Flag':True,         # 电容规格是否正确
        '品牌': '',          # 查询到最低价格的品牌
        'price': '',        # 查询到的最低价格
        'Msgbox':''         # 提示字符串
    }
    '''

    # 判断请购数量
    if orderCount<1 :
        print('采购数量有误，请确认！')
        exit()

    # 初始化返回值
    productPrice = {
        'Flag':True,
        '品牌': '',
        'price': '',
        'Msgbox':''
    }
    priceArr = []

    # 设置搜索引擎
    aggAttrApi = 'https://soic.oneyac.com/agg_attr?'
    searchApi = 'https://soic.oneyac.com/search?'

    flag,msg = specJudgment(aggAttrApi, capacitance, package, voltage, accuracy)
    productPrice['Msgbox'] = msg
    # 判断输入电容规格参数是否有误
    if  flag == False:
        productPrice['Flag'] = False
        return productPrice

    # 电容参数正确，执行查找价格
    webToken,webXlstoken = getToken()
    token = getSearchToken(webToken)
    xlstoken = getSearchToken(webXlstoken)

    # 规格参数
    specAttr = {
        "aggFields": "brand",
        "page": 0,
        "pageSize": 10,
        "supplierId": "1",
        "categoryId": "1207",
        "keyword": "",
        "brand_id_filters[]": [],
        "agg_attr_name_filters[]": ["封装/外壳", "容值", "偏差", "电压"],
        "token": token,
        "xlsToken": xlstoken,
        "attr_封装/外壳[]":[package],
        "attr_电压[]": [voltage],
        "attr_容值[]": [capacitance],
        "attr_偏差[]": [accuracy],
        "orderBy": "minPrice",
        "sort": "asc"
    }

    productDic = getJosn(searchApi,specAttr)
    price = productDic['priceModelList']
    print(productDic)
    productPrice['品牌'] = productDic['brandName']

    if len(price) == 0:  # 无价格
        productPrice['price'] = ''
        productPrice['Flag'] = False
        productPrice['Msgbox'] = '暂无价格'
    elif len(price) == 1:
        productPrice['price'] = price[0]['price']  # 仅此一个价格
        return productPrice
    else:
        # 获取所有价格
        for i in range(0, len(price)):
            priceArr.append(int(price[i]['stepNum']))

        if orderCount in priceArr:
            indexNum = priceArr.index(orderCount)
            productPrice['price'] = price[indexNum]['price']
        else:
            # 将订单数据添加至列表，并重新排序
            priceArr.append(orderCount)
            priceArr.sort()
            # 获取指定元素orderCount,index
            print(type(priceArr))
            indexNum = priceArr.index(orderCount)

            # 最终确认价格
            productPrice['price'] = price[indexNum - 1]['price']

    return productPrice

if __name__ == '__main__':
    print(getPrice(2000,'100nF','0402','16V','±20%'))








