# -*- coding: utf-8 -*-
import scrapy
import re
from pyquery import PyQuery as pq
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CountrySpider(CrawlSpider):
    name = 'xoyo'
    allowed_domains = ['jx3.xoyo.com']
    start_urls = ['https://jx3.xoyo.com/allnews/']

    rules = (
        Rule(LinkExtractor(allow=r'allnews/|press/|announce/|hd/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        dom = pq(response.body)
        title = dom("title").text()
        date = dom(".detail_time").text()
        abstract = dom(".detail_con").text()

        item = {}

        item['url'] = response.url
        item['title'] = title
        item['date'] = date
        item['abstract'] = abstract[0:255]
        return item
