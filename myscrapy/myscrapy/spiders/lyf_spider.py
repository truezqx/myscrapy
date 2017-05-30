#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
import urllib
import re
import os
import json

class XiaoHuaSpider(scrapy.Spider):
    name = "lyf"
    allowed_domains = ["douban.com"]
    start_urls = []
    for i in range(0,200,40):
	url = "https://movie.douban.com/celebrity/1049732/photos/?type=C&start=%d&sortby=vote&size=a&subtype=a"%i
	start_urls.append(url)
    #print('start_urls:%s'%start_urls)


    def parse(self,response):
        
       # current_url = response.url #爬取时请求的URL
       # body = response.body #返回的Html
       # unicode_body = response.body_as_uncode()#返回的html unicode编码
        hxs = scrapy.Selector(response)
	#sites = hxs.select('//ul/li/div/a/img/@src').extract()
	items = hxs.xpath('//ul/li/div[@class="cover"]/a/img/@src').extract()
	#print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii%s'%items)
	for i in items:
		name = re.findall('https://\w+.doubanio.com/view/photo/thumb/public/(\w+).jpg',i)
		with open('/data/scrapy/pic/lyf.txt','a+') as f:
			f.write(i+'\n')
		file_name = '/data/scrapy/pic/%s.jpg'%name[0]
		i = i.replace('thumb','photo')
		urllib.urlretrieve(i,file_name)
		
			

