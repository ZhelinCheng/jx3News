# -*- coding: utf-8 -*-
import scrapy
import re
from pyquery import PyQuery as pq
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import redis


try:
    redis_db = redis.Redis(host='192.168.84.129', port=6379, db=4, password='test')
    redis_data_dict = "f_url"
    print "db ok!"
except:
    print "db err!"

class CountrySpider(CrawlSpider):
    name = 'xoyo'
    allowed_domains = ['jx3.xoyo.com']
    start_urls = ['https://jx3.xoyo.com/allnews/']

    rules = (
        Rule(LinkExtractor(allow=r'https?:\/\/jx3\.xoyo\.com.*|allnews/|press/|announce/|hd/'), callback='parse_item', process_links='url_repeat', follow=True),
    )

    def url_repeat(self, list):
        newList = []
        for item in list:
            url = item.url
            pd = redis_db.hexists(redis_data_dict, url)
            if not pd:
                newList.append(item)
                redis_db.hset(redis_data_dict, url, 0)

        return newList

    def parse_item(self, response):
        dom = pq(response.body)
        title = dom("title").text()
        date = dom(".detail_time").text()
        abstract = dom(".detail_con").text()
        date = re.sub(u'\u65f6\u95f4: ', '', date)

        item = {}
        item['url'] = response.url
        item['title'] = title
        item['date'] = date
        item['abstract'] = abstract[0:255]
        return item

if __name__ == '__main__':
    date = '时间: 2011-05-27 11:22:24'
    date = re.sub('时间: ', '', date)
    print date