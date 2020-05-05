import execjs
#js 源代码：
'''
function getSearchToken(r, q) {
    var p, s = "";
    s = q;
    var arr = q;
    var len = arr.length,
        temp,
        gap = 1;
    while(gap < len/3) {
        gap = gap*3+1;
    }
    for (gap; gap > 0; gap = Math.floor(gap/3)) {
        for (var i = gap; i < len; i++) {
            temp = arr[i];
            for (var j = i-gap; j >= 0 && arr[j] > temp; j -= gap) {
                arr[j+gap] = arr[j];
            }
            arr[j+gap] = temp;
        }
    }
    p = "on@hol1" + r + s.substring(22, 33) + "!xm@" + s.substring(33, s.length) + "1wyno" + s.substring(0, 22) + "eyac$der";
    var len = arr.length;
    var minIndex, temp;
    for (var i = 0; i < len - 1; i++) {
        minIndex = i;
        for (var j = i + 1; j < len; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        temp = arr[i];
        arr[i] = arr[minIndex];
        arr[minIndex] = temp;
    }
    return p
}

'''
def getJS(path):
    f = f = open(path, 'r', encoding='UTF-8')
    line = f.readline()
    jsStr = ''
    while line:
        jsStr = jsStr + line
        line = f.readline()
    return jsStr


def getSearchToken(q):
    jsStr = getJS('C:/Users/shabu/Desktop/web/getSearchtoken.js')
    jscontext = execjs.compile(jsStr)
    token = jscontext.call('getSearchToken', 1, q)
    return token


if __name__ == '__main__':
    token = getSearchToken('sMAvzBVzceaiZIQbZ4cHWEXz1dZ48xkS3zqEyJwQnyKU9ukY9G')
    xlsToken = getSearchToken('Kldi3QoWtOyim2ZQ27ZhCM7sA0M7zS0Xo7cyzgramnPEVR85SN')
    print(token)
    print(xlsToken)
