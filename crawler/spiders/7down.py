#!/usr/bin/env python
# encoding: utf-8
# @author: jiajia
# @time: 2018/10/15 16:44
# @Version : Python3.6
import re
import time
import json
import random

import scrapy
from scrapy.http import Request
from pyquery import PyQuery as pq
from urllib.parse import urlencode

from crawler.items import CrawlerItem as ITEM


class QuotesSpider(scrapy.Spider):
    name = "bysj"
    allowed_domains = ['china.findlaw.cn']
    start_url = 'http://china.findlaw.cn/ask/browse'
    headers = {
        'Host': 'china.findlaw.cn'
    }

    def start_requests(self):
        url = self.start_url + '_page1'
        yield Request(url=url, headers=self.headers, callback=self.second_requests)

    def second_requests(self, response):
        all_url = response.css('.pagination-item::attr(href)').extract()[-1]
        all_url = re.findall('browse_page([0-9]+)', all_url)
        number = list(map(eval, all_url))[0]
        referer_url = response.url
        # number = 10
        for number in range(1, number + 1):
            url = self.start_url + '_page' + str(number)
            self.headers['referer'] = referer_url
            yield Request(url=url, headers=self.headers, callback=self.get_xinxi, dont_filter=True)
            referer_url = url

    def get_xinxi(self, response):
        xinxi = response.css('.result-list .list-item').extract()
        for i in xinxi:
            a_item = dict()
            doc = pq(i)
            a_item['lx'] = doc('.rli-item.item-classify').text()
            a_item['bt'] = doc('.rli-item.item-link').text()
            a_item['hds'] = doc('.rli-item.item-num').text()
            self.headers['referer'] = response.url
            new_url = doc('.rli-item.item-link').attr('href')
            if new_url:
                yield Request(url=new_url, headers=self.headers, callback=self.get_item, meta=a_item)
            else:
                print(response.url)
                print(new_url)

    def get_item(self, response):
        item = ITEM()
        question = response.css('.q-detail::text').extract()
        answer = response.css('.about-text').extract()
        ans = []
        for i in answer:
            doc = pq(i)
            ans.append(doc.text())

        item['question'] = ''.join(question)
        item['answer'] = ans
        item['lx'] = response.meta['lx']
        item['bt'] = response.meta['bt']
        item['hds'] = response.meta['hds']
        item['time'] = response.css('span.about-item:nth-child(2)::text').extract_first()
        item['dq'] = response.css('.q-about span a ::text').extract_first()

        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute
    # excute 执行scrapy命令
    import os  # 用来设置路径
    import sys  # 调用系统环境，就如同cmd中执行命令一样

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute("scrapy crawl bysj".split())