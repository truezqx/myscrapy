#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
import urllib
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import BaseSpider
import re
import os

class XiaoHuaSpider(scrapy.Spider):
    name = "xiaohua"
    allowed_domains = ["xiaohua.com"]
    start_urls = [
	"http://www.xiaohuar.com/list-1-1.html",
    ]


    def parse(self,response):
        
       # current_url = response.url #爬取时请求的URL
       # body = response.body #返回的Html
       # unicode_body = response.body_as_uncode()#返回的html unicode编码
        hxs = scrapy.Selector(response)
	if re.match('http://www.xiaohuar.com/list-1-\d+.html',response.url):
		items = hxs.xpath('//div[@class="item_list infinite_scroll"]/div')
		for i in range(len(items)):
			src = hxs.xpath('//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/a/img/@src' % i).extract()
			name = hxs.xpath('//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/span/text()' % i).extract()
			school = hxs.xpath('//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/div[@class="btns"]/a/text()' % i).extract()
			if src:
				ab_src = "http://www.xiaohuar.com" + src[0]
				file_name = "%s_%s.jpg" %(school[0],name[0])
				file_path = os.path.join("/data/scrapy/pic/",file_name)
				urllib.urlretrieve(ab_src,file_path)
