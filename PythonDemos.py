#需要先安装pipywin32模块
import pythoncom,json
import PriceTierView
from DecryptToken import getSearchToken

class PythonUtilities:

    _public_methods_=['VbgetPrice']                 # 对外调用函数名称
    _reg_progid_='PythonDemos.Utilities'            # 对外申请Com接口
    _reg_clsid_=pythoncom.CreateGuid()              # 获取本机注册码

    def VbgetPrice(self,orderCount, capacitance, package, voltage, accuracy):
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
        # 声明变量类型
        orderCount = int(orderCount)
        capacitance =str(capacitance)
        package = str(package)
        voltage = str(voltage)
        accuracy = str(accuracy)

        # 初始化返回值
        productPrice = {
            'Flag': True,
            '品牌': '',
            'price': '',
            'Msgbox': ''
        }

        # 判断请购数量
        if orderCount < 1:
            productPrice['Flag'] = False
            productPrice['Msgbox'] = '订单数量有误'
            return json.dumps(productPrice).encode('utf-8').decode('unicode_escape')

        priceArr = []

        # 设置搜索引擎
        aggAttrApi = 'https://soic.oneyac.com/agg_attr?'
        searchApi = 'https://soic.oneyac.com/search?'

        flag, msg = PriceTierView.specJudgment(aggAttrApi, capacitance, package, voltage, accuracy)
        productPrice['Msgbox'] = msg

        # 判断输入电容规格参数是否有误
        if flag == False:
            productPrice['Flag'] = False
            return json.dumps(productPrice).encode('utf-8').decode('unicode_escape')

        # 电容参数正确，执行查找价格
        respText,webToken, webXlstoken = PriceTierView.getToken()

        if respText == "webToken获取失败":
            productPrice['Flag'] = False
            productPrice['Msgbox'] = "webToken获取失败"
            return json.dumps(productPrice).encode('utf-8').decode('unicode_escape')

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
            "attr_封装/外壳[]": [package],
            "attr_电压[]": [voltage],
            "attr_容值[]": [capacitance],
            "attr_偏差[]": [accuracy],
            "orderBy": "minPrice",
            "sort": "asc"
        }

        productDic = PriceTierView.getJosn(searchApi, specAttr)
        price = productDic['priceModelList']
        productPrice['品牌'] = productDic['brandName']

        if len(price) == 0:  # 无价格
            productPrice['price'] = ''
            productPrice['Flag'] = False
            productPrice['Msgbox'] = '暂无价格'
        elif len(price) == 1:
            productPrice['price'] = price[0]['price']  # 仅此一个价格
            return json.dumps(productPrice).encode('utf-8').decode('unicode_escape')
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
                indexNum = priceArr.index(orderCount)

                # 最终确认价格
                productPrice['price'] = price[indexNum - 1]['price']

        return json.dumps(productPrice).encode('utf-8').decode('unicode_escape')

# VBA 代码
'''
Private Sub text()

    Set PythonUtils = CreateObject("PythonDemos.Utilities")
    
    ss = PythonUtils.VbgetPrice(10000, "100nF", "0402", "16V", "±20%")

End Sub
'''


if __name__=='__main__':
    print ('Registering COM server...')
    import win32com.server.register
    win32com.server.register.UseCommandLine(PythonUtilities)