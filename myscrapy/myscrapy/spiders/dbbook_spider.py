#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
import urllib
import re
import os
import json
from myscrapy.items import MyscrapyItem


class XiaoHuaSpider(scrapy.Spider):
    name = "dbbook"
    allowed_domains = ["douban.com"]
    start_urls = ['https://www.douban.com/doulist/1264675/',]


    def parse(self,response):
        
       # current_url = response.url #爬取时请求的URL
       # body = response.body #返回的Html
       # unicode_body = response.body_as_uncode()#返回的html unicode编码
	item = MyscrapyItem()
	selector = scrapy.Selector(response)
	#sites = hxs.select('//ul/li/div/a/img/@src').extract()
	books = selector.xpath('//div[@class="bd doulist-subject"]')
	for book in books:
		#print(item)
		title = book.xpath('div[@class="title"]/a/text()').extract()[0]
		rate = book.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()[0]
		author = book.xpath('div[@class="abstract"]/text()').extract()[0]
		title = title.replace(' ','').replace('\n','')
		author = author.replace(' ','').replace('\n','')
		item['title'] = title
		item['rate'] = rate
		item['author'] = author
		#print(title)
		#print(rate)
		#print(author)
		#print('\n')
		yield item
		nextpage = selector.xpath('//span[@class="next"]/link/@href').extract()
		if nextpage:
			next = nextpage[0]
			yield scrapy.http.Request(next,callback=self.parse)
