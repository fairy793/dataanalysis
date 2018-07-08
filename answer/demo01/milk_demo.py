#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : milk_demo.py
# @Author: Lmm
# @Date  : 2018-04-21
# @Desc  : 简单用于爬取京东牛奶数据
import requests
from lxml import etree
import csv


class Get_Milk_Info:
	def __init__(self, url,keyword):
		self.url = url.format(keyword)
		print (self.url)
	def get_html(self):
		'''
		用于获得页面源码
		:param keyword: 搜索关键词
		:return: 如果请求状态为200则返回lxml结构化的数据，否则返回None
		'''
	    #请求头仿照
		headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"Cache-Control": "max-age=0",
		"Connection": "keep-alive",
		#Cookie: 3AB9D23F7A4B3C9B=5KV3EDF5GU2R3CMTGAW725RJ77HKAQY2PZP3NDOXPMRPU7TQRI4JRGKNXATEPQTWRXACGVTNS3VCI2X3ACVWUDIT2Q; unpl=V2_ZzNtbUJWQ0B9DkVTKx4JV2IDFFtLVkZGJVsVU3tLWVczURMNclRCFXwUR1FnGlwUZwcZXEpcQRNFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2UX8fXQRnBRBtclBzJUUBRVd%2bHlw1ZjMTbQADHxJyDUNRfFRZAWECE11EVXMURQs%3d; CCC_SE=ADC_qwq7oTWNPne6y0GQIRAHo9CDO0Z6evznZvEDKjb9KRP%2bnOCf5X3BHweYRqVfRjLJ38%2bXo46ElBnul30nBZLdQMDcCC%2b4FS5G%2f6kjDqA9z5HKt15wA83KJ9aJCSg%2btpk3HYggaOmvK%2fhouUBgCYs4l1c4IVQYpwX6GQYOjOhRXsup74Zfovf8X7pR8yVEFaJSHeqOyy%2f4WqmZVimEy6VHjDflVjy9QjOzxa4d%2bMLR8kXnXqdAtIzTSLTO1repOlG58mLCfWlhY9NbbcmWN%2ba2%2f7pkky3jyXRnTocxhHD%2bw%2fOoIEPJ1CZR0%2fhpoaI0J%2fwCJpCnjjl2HSNFqKYToF1PxJQSPQB%2blJQLXD0hQJrG1EewFWyvyaLbezDG6c0rgjcrqB%2fklhieUYH%2fW6ULIujeYkP63OM5fbIXLfR8l8ujNItn%2bf7qgcEzDmS3UA27OaJH%2bDxaUTYZcx7vr8tGFIqc%2fPpzOKv0ex43tXAidzhz9Sbsk7874v057Z5zI7SwVXqyQWg6KM%2b85aTryvXjdt4IKiiZV7lXmWPK592mUR4NwNqhZ7mxu%2fSU5DmTI1fIu1Ml; __jda=122270672.45700173.1520676752.1520676752.1524294578.1; __jdc=122270672; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_101d9726a6dc4177804babb61c4cec0a|1524294577960; __jdu=45700173; PCSYCityID=248; xtest=6288.cf6b6759; ipLoc-djd=1-72-2799-0; rkv=V0600; mt_xid=V2_52007VwYWVFxZUlwdeUkLUTVWQVsJRAEPFksFWVUyUQ4BXlBWRh9PTFRQMwtGBV0NVGocSBlVGWYGDlFdSVJeFEwZVwBiMxBiXWhRWx1PGl0GYgUiUlheVQ%3D%3D; __jdb=122270672.4.45700173|1.1524294578; qrsc=2
		"Host": "search.jd.com",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
  
		}
		result = requests.get(self.url, headers=headers)
		status_code = result.status_code
		if status_code == 200:
			html = etree.HTML(result.content,parser=etree.HTMLParser(encoding='utf-8'))
		else:
			html = None
		return html
	def get_need_info(self,html):
		'''
		用于抽取所需数据
		:param html: 参数为结构化过的HTML源码信息，并保存到csv文件中
		:return:返回抽取的列表信息数据
		'''
		info_list = {}
		if html!=None:
			li_list = html.xpath(".//div[@id='J_goodsList']//li[@class = 'gl-item']")
			for i,good in enumerate(li_list,1):
				item = {}
				item['ID'] = good.xpath('./@data-sku')[0].strip()
				item['name'] = good.xpath('.//div[@class="p-name p-name-type-2"]/a/em')
				item["name"] = item["name"][0].xpath("string(.)").strip()
				shop_name = good.xpath('.//div[@class="p-shop"]/span[@class= "J_im_icon"]/a/@title')
				if shop_name:
					item["shop_name"] = shop_name[0].strip()
				else:
					item["shop_name"] = ''
				item['link'] = good.xpath('.//div[@class="p-img"]/a/@href')[0].strip()
				
				img_url = good.xpath(".//div[@class = 'p-img']//img[@class = 'err-product']/@src")
				if img_url:
					img_url = img_url[0]
				else:
					img_url = good.xpath(".//div[@class = 'p-img']//img[@class = 'err-product']/@data-lazy-img")[0]
				item["img_url"] = "https:"+img_url
		
				info_list[i] = item
		return info_list
	   
	def write_to_file(self,info_list):
		'''
		#将获取到的信息保存到csv文件中
		:param info_list:
		:return:
		'''
		with open("test.csv", "wb") as csvfile:
			writer = csv.writer(csvfile)
			# 先写入columns_name
			writer.writerow(["index", "ID", "name", "shop_name", "url"])
			#将数据写入到文件中,由于中文写入时会出现编码问题，因此对数据编码格式进行了统一设置
			for key, value in info_list.iteritems():
				writer.writerow([key, value["ID"], value["name"].encode('utf-8'), value["shop_name"].encode('utf-8'), value["link"].encode("utf-8")])
				

def main():
	#进口牛奶的链接
	url = 'https://search.jd.com/Search?keyword={0}&enc=utf-8&suggest=1.def.0.V16&wq=jink&pvid=a563eb60454a4864a275e1d45d1d40ae'
	keyword = u'进口牛奶'.encode("utf-8")
	obj = Get_Milk_Info(url, keyword)
	html = obj.get_html()
	info_list = obj.get_need_info(html)
	if info_list:
		obj.write_to_file(info_list)
	
if __name__ == '__main__':
    main()
	