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
# fig = plt.figure(figsize = (12,5))
# ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(122)

#偏度，Skewness，是研究数据分布对称的统计量。通过对偏度系数的测量，我们能够判定数据分布的不对称程度以及方向。
#判断数据是否是正态分布的
# g1 = sns.distplot(df["aid"],hist = True,label='skewness:{:.2f}'.format(df['aid'].skew()),ax = ax1)
#
# g1.legend()
# g1.set(xlabel = 'aid')
#
# g2 = sns.distplot(np.log1p(df['aid']),hist = True,label='skewness:{:.2f}'.format(np.log1p(df['aid']).skew()),ax=ax2)
# g2.legend()
# g2.set(xlabel = 'log(aid+1)')
# plt.show()


# fig = plt.figure(figsize = (12,5))
# ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(122)
# g1 = sns.distplot(df["advertiserId"],hist = True,label='skewness:{:.2f}'.format(df['advertiserId'].skew()),ax = ax1)
#
# g1.legend()
#
# g1.set(xlabel = 'aidadvertiserId')
#
# g2 = sns.distplot(np.log1p(df['advertiserId']),hist = True,label='skewness:{:.2f}'.format(np.log1p(df['advertiserId']).skew()),ax=ax2)
# g2.legend()
# g2.set(xlabel = 'log(advertiserId+1)')
# plt.show()

#多图形式
# output,var, = 'aid', 'advertiserId',
# fig, axes = plt.subplots(figsize=(16,5))
# df.plot.scatter(x=output,y=var,ax=axes)
# plt.show()

#箱图
# output,var, = 'advertiserId', 'aid'
# fig, ax = plt.subplots(figsize=(16,30))
# sns.boxplot(x=var,y=output,data=df)
# plt.xticks(rotation=90)
# # # ax.set_ylim(0,100000)
# plt.show()



# 对各个特征之间的关系进行分析
# 最简单地，直接获取整个DataFrame数据的协方差矩阵并利用sns.heatmaP()进行可视化
corrmat = df.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True, ax=ax)  # square参数保证corrmat为非方阵时，图形整体输出仍为正方形
plt.show()


#我们可以选取与output变量相关系数最高的3个特征查看其相关情况，找出那些相互关联性较强的特征
output = 'aid'
k = 5
top3_attr = corrmat.nlargest(k, output).index
top3_mat = corrmat.loc[top3_attr, top3_attr]
fig,ax = plt.subplots(figsize=(8,6))
sns.set(font_scale=1.25)
# 设置annot使其在小格内显示数字，annot_kws调整数字格式
sns.heatmap(top3_mat, annot=True, annot_kws={'size':12}, square=True)

plt.show()







	
	