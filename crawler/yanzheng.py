#!/usr/bin/env python
# encoding: utf-8
# @author: jiajia
# @time: 2018/10/15 16:44
# @Version : Python3.6
import requests
import re
import json
import time

from crawler.shibie import ImageProcessing

class Yanzheng:

    def shibie(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

        while True:
            ses = requests.Session()
            html = ses.get(url='http://china.findlaw.cn/', headers=headers)
            if 'ipfilter.lsurl' in html.url:
                contin = re.findall('continue=([A-Za-z0-9]*)', html.url)
                contin = contin[0] if contin else ''
                list_powerkey = re.findall('name="powerkey" value="(.+)"', html.text)
                the_powerkey = list_powerkey[0] if list_powerkey else ''

                pict_url = re.findall('id=\'vimg\' src="(.+)">', html.text)[0]
                p = ses.get(pict_url).content
                # dz = 'imagexxx.jpg'
                # local = open(dz, 'wb')
                # local.write(p)
                # local.close()
                print("获得验证码成功")
                vgcode = ImageProcessing(p).ImageRecognition()
                vgcode = '1234' if not vgcode else vgcode
                print(vgcode)

                post_url = 'http://ipfilter.lsurl.cn/index.php?m=Home&c=IpFilter&a=submit_verification'

                post = {
                    'vgcode': vgcode,
                    'powerkey': the_powerkey,
                    'continue': contin
                }
                a = ses.post(post_url, data=post)
                if a.status_code == 200:
                    print('验证码输入成功')
                    break
                else:
                    print('验证码输入错误，重新输入')
            else:
                break


if __name__ == '__main__':
    Yanzheng().shibie()