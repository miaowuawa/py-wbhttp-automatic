import requests
import base64
import http.cookiejar
import re
import json
import time
import datetime
from PIL import Image
import logging
session = requests.session()
timestamp = time.time
def fetch_qrcode_image(UA):
    url = "https://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_"+timestamp
    headers = {
        'User-Agent': UA,
        'accept-language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://weibo.com/',
        'Accept': '*/*',
        'Host': 'login.sina.com.cn',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers)
    qrid = re.search(r'"qrid":"([^"]+)"', response)
    imagel = re.search(r'"image":"([^"]+)"', response)
    image = requests.request("GET", image, headers=headers)
    with open('./qrcode.jpg', 'wb') as f:
        f.write(image.content)

    '''if showwindow:
        logging.info("请扫描二维码后在手机上确认，然后关闭窗口，自动登录")
        img=Image.open('./qrcode.jpg')
        img.show()'''

    return qrid



def wblogin(deviceinfo,protocol,waytologin):
    if protocol == 0:
        if waytologin == 0:
            qrid = fetch_qrcode_image(deviceinfo)
            logging.info("请打开目录下的qrcode.jpg，扫描后确认登录！")




        
    
                 

#Protocols:
#0:WEB protocol(weibo.com)
#1:H5 protocol(m.weibo.com)
#2:APP
#3:Lite/international APP protocol(国际/轻量)
#Ways to Login:
#0:QRcode(WEB only!)
#1:SMS code(ALL)
#2:Password(ALL)







