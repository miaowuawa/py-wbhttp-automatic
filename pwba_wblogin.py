import requests
import base64
import http.cookiejar as ckjar
import re
import json
import time
import datetime
# from PIL import Image
import logging
import os
import urllib
import pwba_basic
logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(levelname)s] %(message)s')
s = requests.session()
session = requests.session()
timestamp = time.time
def fetch_qrcode_image(UserAgent): 

    url = "https://login.sina.com.cn/sso/qrcode/image?entry=weibo&size=180&callback=STK_"+str(time.time())

    headers = {
        'User-Agent': UserAgent,
        'accept-language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://weibo.com/',
        'Accept': '*/*',
        'Host': 'login.sina.com.cn',
        'Connection': 'keep-alive'
    }

    response = s.request("GET", url, headers=headers)
    # 提取JSON数据
    start_index = response.text.find('{')  # 找到第一个左大括号
    end_index = response.text.rfind('}')  # 找到最后一个右大括号
    json_str = response.text[start_index:end_index+1]  # 提取JSON字符串
    # 解析JSON数据
    data = json.loads(json_str)
    qrid = data["data"]["qrid"]
    link = data["data"]["image"]
    api_key = re.search('.*?api_key=(.*)"', json_str).group(1)
    # 构造url
    imgurl = "https://v2.qr.weibo.cn/inf/gen?api_key=" + api_key
    # 获取图片
    img = s.get(imgurl)
    # 写入本地，已取消图片打开
    with open('./scan.png','wb') as f:
        # print(img.content)
        f.write(img.content)
        f.close()
    return qrid

def qrcode_check(qrid,UserAgent):
    #检验二维码状态
    #构造请求url
    headers = {
        'User-Agent': UserAgent,
        'accept-language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://weibo.com/',
        'Accept': '*/*',
        'Host': 'login.sina.com.cn',
        'Connection': 'keep-alive'
    }
    ts=str(time.time()*100000)
    url = 'https://login.sina.com.cn/sso/qrcode/check?entry=sso&qrid=' + qrid + '&callback=STK_'+ts
    response = s.get(url,headers=headers)
    data = re.search('.*?\((.*)\)',response.text).group(1)
    data_js = json.loads(data)
    print(data_js["retcode"])
    #如果成功就返回alt，否则返回False
    if data_js["retcode"] != 20000000:
        return False
    else:
        alt = data_js['data']['alt']
        return alt

def wblogin(protocol,way,deviceinfo):
    headers = {
        'User-Agent': deviceinfo,
        'accept-language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://weibo.com/',
        'Accept': '*/*',
        'Host': 'login.sina.com.cn',
        'Connection': 'keep-alive'
    }
    if way == 0:
        #扫码登陆处理程序
        if protocol == 0:
            qrid = fetch_qrcode_image(deviceinfo)
            while 1:
                ts=str(time.time()*100000)
                tmp = qrcode_check(qrid,deviceinfo)
                if tmp:
                    
                    logging.info("登录成功！")
                    alturl = 'https://login.sina.com.cn/sso/login.php?entry=qrcodesso&returntype=TEXT&crossdomain=1&cdult=3&domain=weibo.com&alt='+tmp+'&savestate=30&callback=STK_'+ts
                    response = s.get(alturl,headers = headers)
                    print(response.text)
                    data = re.search('.*\((.*)\);',response.text).group(1)
                    print(data)
                    data_js = json.loads(data)
                    print(data_js)
                    uid = data_js['uid']
                    nick = data_js['nick']
                    logging.info("账号信息：uid"+str(uid)+" 昵称："+nick)
                    crossDomainUrlList = data_js['crossDomainUrlList']
                    logging.debug("crossdomains:" + crossDomainUrlList)
                    #依次访问另外三个url
                    s.cookies = ckjar.LWPCookieJar(filename='session.info')
                    s.get(crossDomainUrlList[0],headers = headers)
                    s.get(crossDomainUrlList[1] + '&action=login', headers=headers)
                    s.get(crossDomainUrlList[2], headers=headers)
                    s.cookies.save()
                    break
                else:
                    logging.info("请扫描二维码，并确认登录……")
                    logging.info("扫描失败即二维码已失效，请重启程序!")
                time.sleep(1.5)       
            return True
        else:
            print("不支持此方式登录！")
            return False





        
    
                 

#Protocols:
#0:WEB protocol(weibo.com)
#1:H5 protocol(m.weibo.com)
#2:APP
#3:Lite/international APP protocol(国际/轻量)
#Ways to Login:
#0:QRcode(WEB only!)
#1:SMS code(ALL)
#2:Password(ALL)







