# PriceTierView
查询电子元器件价格步骤：
 - URL:https://www.oneyac.com/category/1207.html
 - 每次请求发现URL都不同，最终发现URL组成格式：/search?callback=jQuery + 数字 + 请求数据
    - 请求数据包含：
        - 回调函数callback （callback=jQuery1124032359969327551297_1589472065817）
            - 通过百度搜索URL带jQuery 可知jQuery后面回调函数，数字为函数名（随机生成,libs-all.min-119aef9b16fe132c812e6ef89ac7e9dc.js可查找到源代码）
                - js源代码：'jQuery' + (m + Math.random()).replace(/\D/g, '')，通过查找关键字m，可知 m = '1.12.4'
                - 通过浏览器开发工具调试控制台可知，Math.random()生成0~1的随机浮点数（精度小数点后17位），.replace(/\D/g, '') 表示用‘’替换‘.’
            - _ 后的数字与URL最后一个参数数字相近
        - paramsDTO ： 参数字典
            - 规格参数数组，可以参考网页源代码中LIST_FORM或者多次请求发现规格的字典的变化
            - token ： 令牌
            - xlsToken ： 令牌
                - 查看js源文件可以发现，token由getSearchToken 函数生成
                - 图片一地址
                - data.token : 在网页源代码中可以通过‘token’查询到
                - data.xlsToken ： 在网页源代码中可以通过‘xlsToken’查询到
                - data.requestParameters.supplierId ： 默认为1
                - getSearchToken 全局搜索无法找到相关函数定义，可以通过使用火狐浏览器的调试功能在代码前设置断点，然后点击进入可以查询到源代码，js代码采用加密
                - 图片2，3
                - 解密搜索引擎搜索，发现https://www.sojson.com/question/69720496242191535293.html，由讲解，有专门的人进行解密工作，需要付费，添加微信，将加密源文件发给解密工作人员，最终得到解密js代码
                - 将js代码转换成python代码,这里使用execjs 库进行快速导入js文件执行代码：https://www.jianshu.com/p/df4ae2374a68
        - _ : 多次使用浏览器模拟，发现前面几位始终不变，仅最后两位有变化，猜测与时间有关，查找相关视频最终确认为时间浮点数
        
  
 
