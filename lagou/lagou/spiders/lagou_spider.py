#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
import urllib
import re
import os
import json
from lagou.items import LagouItem


class LaGouSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ["lagou.com"]
    start_urls = ['http://www.lagou.com/zhaopin/',]
    totalPageCount = 0
    curpage = 1
    url = 'http://www.lagou.com/jobs/positionAjax.json?'
    city = u'杭州'
    kds = [u'大数据',u'云计算',u'docker',u'中间件','Node.js',u'数据挖掘',u'自然语言处理',u'搜索算法',u'精准推荐',u'全栈工程师',u'图像处理',u'机器学习',u'语音识别']
    kd = kds[0]
    
    def start_requests(self):
        return [scrapy.http.FormRequest(self.url,formdata={'pn':str(self.curpage),'kd':self.kd,'city':self.city},callback=self.parse)]

    def parse(self,response):
	item = LagouItem()
	jdict = json.loads(response.body)
	jcontent = jdict['content']
	jpositionResult = jcontent['positionResult']
	jresult = jpositionResult['result']
	self.totalPageCount = jpositionResult['totalCount']/15 + 1
	#print(self.totalPageCount)
	for result in jresult:
		#print(result['city'])
		#print(result['companyFullName'])
		#print(result['companySize'])
		#print(result['positionName'])
		#print(result['salary'])
		#print('\n')
		item['city'] = result['city']
		item['companyFullName'] = result['companyFullName']
		item['companySize'] = result['companySize']
		item['positionName'] = result['positionName']
		item['salary'] = result['salary']
		yield item
	if self.curpage <= self.totalPageCount:
		self.curpage += 1
		#print(self.curpage)
		yield scrapy.http.FormRequest(self.url,formdata={'pn':str(self.curpage),'kd':self.kd,'city':self.city},callback=self.parse)
	
