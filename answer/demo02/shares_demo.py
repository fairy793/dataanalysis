#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : shares_demo.py
# @Author: Lmm
# @Date  : 2018-04-21
# @Desc  : 获取雪球 美国股市涨幅最大的100个股票信息（股票代码，股票名称，当前价，涨跌幅，市值，市盈率）

import requests
import json
import csv
import time
class Get_Shares_Info:
	def __init__(self,headers,cookies):
		self.headers = headers
		self.cookies = cookies
	
	def get_cookies(self,url):
		'''
		用于获取cookies值
		:param url: 访问的链接
		:return: 返回cookies值
		'''
		result = requests.get(url,headers = self.headers)
		status_code = result.status_code
		if status_code ==200:
			cookies = result.cookies
		else:
			cookies = {}
		self.cookies = cookies
	def get_html(self,url):
		
		result = requests.get(url, headers=self.headers, cookies=self.cookies)
		status_code = result.status_code
		if status_code ==200:
			result = json.loads(result.content)
		else:
			result = {}
		return result
	def get_need_info(self,info_url):
		'''
		用于获取所需信息
		:param html:得到的html源码信息
		:return:返回列表
		'''
		info_list = {}
		for i in xrange(1, 3):
			#构造请求链接
			url = info_url.format(i, 60, int(time.time()))
			html = self.get_html(url)
			if html:
				share_info = html["stocks"]
				for i, singleinfo in enumerate(share_info,(i-1)*60):
					if i == 99:
						break
					else:
						item = {}
						item["code"] = singleinfo["code"]
						item["name"] = singleinfo["name"]
						item["current"] = singleinfo["current"]
						item["change"] = singleinfo["change"]
						item["marketcapital"] = singleinfo["marketcapital"]
						item["amount"] = singleinfo["amount"]
						for key,value in item.iteritems():
							item[key] = value.encode("utf-8")
						info_list[i] = item
		return info_list
	
	
	def write_to_file(self, info_list):
		'''
		#将获取到的信息保存到csv文件中
		:param info_list:
		:return:
		'''
		
		with open("test_shares.csv", "wb") as csvfile:
			writer = csv.writer(csvfile)
			# 先写入columns_name
			writer.writerow(["index", "code", "name", "current", "change","marketcapital","amount"])
			# 将数据写入到文件中,由于中文写入时会出现编码问题，因此对数据编码格式进行了统一设置
			for key, value in info_list.iteritems():
				writer.writerow(
					[key+1,value["code"], value["name"], value["current"], value["change"],value["marketcapital"],value["amount"]])

def main():
	url = 'https://xueqiu.com'
	info_url = 'https://xueqiu.com/stock/cata/stocklist.json?page={0}&size={1}&order=1desc&orderby=percent&type=0%2C1%2C2%2C3&isdelay=1&_={2}'
	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"Cache-Control": "max-age=0",
		"Connection": "keep-alive",
		"Host": "xueqiu.com",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
	}
	cookies = None
	obj = Get_Shares_Info(headers, cookies)
	obj.get_cookies(url)
	info_list = obj.get_need_info(info_url)
	if info_list:
		obj.write_to_file(info_list)
		
	
if __name__ == '__main__':
    main()