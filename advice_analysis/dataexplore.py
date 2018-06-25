#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : dataexplore.py
# @Author: Lmm
# @Date  : 2018-06-23 14:33
# @Desc  : 数据探索，查看数据大概长什么样子

# pandas 提供了IO工具可以将大文件分块读取，测试了一下性能,还ok

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#设置路径
path = ""
reader = pd.read_csv("./data/adFeature.csv",iterator=True)

#设置每次读取的条数，可以根据数据的大小自己调整参数
number = 1000
dfs = []
try:
	df = reader.get_chunk(number)
	dfs.append(df)
except StopIteration:
	print ("Iteration is stopped.")
df = pd.concat(dfs, ignore_index=True)

# print(df.head())#查看数据的前十行
# print(df.tail())#查看数据的后十行


#查看数据的整体情况
# count 数量
# mean 平均值
# std 标准差
# min 最小值
# 25% 第一四分位数 (Q1)，又称“较小四分位数”，等于该样本中所有数值由小到大排列后第25%的数字。
# 50% 中位数
# 75% 同上类似
# max 最大值
# print(df.describe())


#查看aid和advertiserid的数据分布
# skew是指数据的偏度
fig = plt.figure(figsize = (12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

g1 = sns.distplot(df["aid"],hist = True,label='skewness:{:.2f}'.format(df['aid'].skew()),ax = ax1)

g1.legend()
g1.set(xlabel = 'aid')

g2 = sns.distplot(np.log1p(df['aid']),hist = True,label='skewness:{:.2f}'.format(np.log1p(df['aid']).skew()),ax=ax2)
g2.legend()
g2.set(xlabel = 'log(aid+1)')
plt.show()


fig = plt.figure(figsize = (12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
g1 = sns.distplot(df["advertiserId"],hist = True,label='skewness:{:.2f}'.format(df['advertiserId'].skew()),ax = ax1)

g1.legend()

g1.set(xlabel = 'aidadvertiserId')

g2 = sns.distplot(np.log1p(df['advertiserId']),hist = True,label='skewness:{:.2f}'.format(np.log1p(df['advertiserId']).skew()),ax=ax2)
g2.legend()
g2.set(xlabel = 'log(advertiserId+1)')
plt.show()

#多图形式
output,var, = 'aid', 'advertiserId',
fig, axes = plt.subplots(figsize=(16,5))
df.plot.scatter(x=output,y=var,ax=axes)
plt.show()

#箱图
output,var, = 'advertiserId', 'aid'
fig, ax = plt.subplots(figsize=(16,30))
sns.boxplot(x=var,y=output,data=df)
plt.xticks(rotation=90)
# # ax.set_ylim(0,100000)
plt.show()








	
	