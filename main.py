import os
import configparser
import time
import logging
from fake_useragent import UserAgent
import pwba_wblogin


# 配置日志记录器
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - %(levelname)s] %(message)s')
ua = UserAgent()
conf = configparser.ConfigParser()

logging.info("PY-WBHTTP 自动化程序 BY:Miaowuawa Github:quqi2")
logging.info("B站：喵呜Miaowuawa 微博：喵呜Miaowuawa")
logging.info("Version:Beta v0.1")
logging.info("禁止使用本程序进行违法犯罪活动！")
logging.info("即将开始处理登录信息……等待3秒（按Ctrl+C以取消此操作！）")
time.sleep(3);

#没有配置文件就创建
if os.path.exists("./config.ini"):
    conf.read("./config.ini")
else:
    logging.warning("未找到配置文件或者读取失败！生成新的默认配置……")
    conf.add_section('mode')
    conf.set('mode', 'account_mode', 'singal')
    conf.set('mode', 'shouwindow_mode', 'false')
    logging.infoinfo("成功，请修改配置，并重新启动")

conf_mode = conf.get("mode", "account_mode")

if conf_mode == "singal":
    logging.info("当前模式：单账号")
    logging.info("开始处理登录信息！")
    
    if os.path.exists("./account.ini"):
        conf.read("./config.ini")
        protocol = conf.get("protocol", "type")
        deviceinfo = conf.get("protocol", "type")
        logging.info("获取到account.ini")
        logging.info("登录开始！")
        pwba_wblogin.wblogin()
        

    else :
        with open('./account.ini', 'w') as configfile:
            logging.warning("未找到账号文件或者读取失败！生成新的默认配置……")
            rua = ua.random
            logging.info("新的设备信息："+rua)
            conf.add_section('protocol')
            conf.set('protocol', 'type', '0')
            conf.set('protocol', 'deviceinfo', rua)
            conf.add_section('login')
            conf.set('login', 'way', '0')
            conf.set('login', 'phone', 'none')
            conf.set('login', 'password', 'none')
            conf.set('login', 'cookie', 'none')
            conf.write(configfile)
        print("账号配置已经生成，请退出程序，进入")

if conf_mode == "multi":
    logging.error("暂未开发多账号功能")
    exit()
