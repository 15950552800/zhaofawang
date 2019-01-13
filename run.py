#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/28 16:37
# @Author  : jiajia
# @File    : run.py
from scrapy.cmdline import execute
# excute 执行scrapy命令
import os  # 用来设置路径
import sys  # 调用系统环境，就如同cmd中执行命令一样


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute("scrapy crawl bysj".split())