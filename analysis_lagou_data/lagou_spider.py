#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : lagou_spider.py
# @Author: Lmm
# @Date  : 2018-06-02 21:05
# @Desc  : 用于获取拉勾网深圳地区数据分析师的职位信息

import requests
import math
import pandas as pd
import time

def get_json(url,num):
   '''''从网页获取JSON,使用POST请求,加上头部信息'''
   my_headers = {
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
           'Host':'www.lagou.com',
           'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
           'X-Anit-Forge-Code':'0',
           'X-Anit-Forge-Token': 'None',
           'X-Requested-With':'XMLHttpRequest'
           }

   my_data = {
           'first': 'true',
           'pn':num,
           'kd':'数据分析'}

   res = requests.post(url, headers = my_headers, data = my_data)
   res.raise_for_status()
   res.encoding = 'utf-8'
   # 得到包含职位信息的字典
   page = res.json()
   return page


def get_page_num(count):
   '''''计算要抓取的页数'''
   # 每页15个职位,向上取整
   res = math.ceil(count/15)
   # 拉勾网最多显示30页结果
   if res > 30:
       return 30
   else:
       return res

def get_page_info(jobs_list):
   '''''对一个网页的职位信息进行解析,返回列表'''
   page_info_list = []
   for i in jobs_list:
       job_info = []
       job_info.append(i['companyFullName'])
       job_info.append(i['companyShortName'])
       job_info.append(i['companySize'])
       job_info.append(i['financeStage'])
       job_info.append(i['district'])
       job_info.append(i['positionName'])
       job_info.append(i['workYear'])
       job_info.append(i['education'])
       job_info.append(i['salary'])
       job_info.append(i['positionAdvantage'])
       for i, single in enumerate(job_info):
           if single == None:
               continue
           job_info[i] = single.encode('utf-8')
       page_info_list.append(job_info)
       print (job_info)
      
       
   return page_info_list

def main():
   url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
   # 先设定页数为1,获取总的职位数
   page_1 = get_json(url,1)
   total_count = page_1['content']['positionResult']['totalCount']
   num = get_page_num(total_count)
   total_info = []
   time.sleep(5)
   print('职位总数:{},页数:{}'.format(total_count,num))
   num = int(num)

   for n in range(1,num+1):
       # 对每个网页读取JSON, 获取每页数据
       page = get_json(url,n)
       jobs_list = page['content']['positionResult']['result']
       page_info = get_page_info(jobs_list)
       total_info += page_info
       print('已经抓取第{}页, 职位总数:{}'.format(n, len(total_info)))
       # 每次抓取完成后,暂停一会,防止被服务器拉黑
       time.sleep(20)
   #将总数据转化为data frame再输出
   df = pd.DataFrame(data = total_info,columns = [u'公司全名',u'公司简称',u'公司规模',u'融资阶段',u'区域',u'职位名称',u'工作经验',u'学历要求',u'工资',u'职位福利'])
   df.to_csv('lagou_jobs.csv',index = False,encoding="utf-8")
   print(u'已保存为csv文件.')

if __name__== "__main__":
   main()