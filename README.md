# PriceTierView
查询电子元器件价格步骤：
 - URL:https://www.oneyac.com/category/1207.html
 - 每次请求发现URL都不同，最终发现URL组成格式：/search?callback=jQuery + 数字 + 请求数据
    - 请求数据包含：
        - paramsDTO ： 参数字典
            - 
        - token ： 令牌
        - xlsToken ： 令牌
        - _ : 未知参数
  - 查看js源文件可以发现，token由getSearchToken 函数生成
    - 图片一地址
    - data.token : 在网页源代码中可以通过‘token’查询到
    - data.xlsToken ： 在网页源代码中可以通过‘xlsToken’查询到
    - data.requestParameters.supplierId ： 默认为1
    - getSearchToken 全局搜索无法找到相关函数定义，可以通过使用火狐浏览器的调试功能在代码前设置断点，然后点击进入可以查询到源代码，js代码采用加密
        - 图片2，3
        - 解密搜索引擎搜索，发现https://www.sojson.com/question/69720496242191535293.html，由讲解，有专门的人进行解密工作，需要付费，添加微信，将加密源文件发给解密工作人员，最终得到解密js代码
        - 将js代码转换成python代码,这里使用execjs 库进行快速导入js文件执行代码：https://www.jianshu.com/p/df4ae2374a68
 
