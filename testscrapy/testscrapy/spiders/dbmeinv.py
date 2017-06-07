# -*- coding: utf-8 -*-
import scrapy
import re
import json
import urllib
from testscrapy.items import TestscrapyItem
class DbmeinvSpider(scrapy.Spider):
    name = 'dbmeinv'
    allowed_domains = ['dbmeinv.com']
    start_urls = ['http://www.dbmeinv.com']

    def parse(self, response):
	item = TestscrapyItem()
    selector = scrapy.Selector(response)
	items = selector.xpath('//div[@class="thumbnail"]')
	for each in items:
		#title = re.search('<img class="height_min" title="(.*?)"',item.extract()).group(1)
		img = []		
		src = each.xpath('div[@class="img_single"]/a/img/@src').extract()
		img_name = re.search('http:.*/bmiddle/(.*?).jpg',src[0]).group(1)
		file_name = '/data/scrapy/dbmeinv/%s.jpg'%img_name
		#urllib.urlretrieve(src[0],file_name)
		img.append(str(src[0]))
		item['image_urls'] = img
		yield item
	nextpage = selector.xpath('//li[@class="next next_page"]/a/@href').extract()
	if nextpage:
		url = "http://www.dbmeinv.com" + nextpage[0]
		print(url)
		yield scrapy.http.Request(url,callback=self.parse)
