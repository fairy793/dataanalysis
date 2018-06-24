#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : data_explore.py
# @Author: Lmm
# @Date  : 2018-06-17 18:14
# @Desc  : 主要对数据进行探索，对数据的基本特征有一个全局的大致了解

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns
from scipy.stats import norm
from scipy import stats
# import warnings
# warnings.filterwarnings('ignore')
# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'inline')
# %config InlineBackend.figure_format = 'retina' #set 'png' here when working on notebook
# %matplotlib inline

df_train = pd.read_csv("./data/train.csv")
# 与 numpy 的ndarray数据相比，DataFrame数据自带有行列信息，且有很多便捷的方法可以直接进行快速分析。

# 查看数据的基本信息
print(df_train.head())#可以查看默认前5行的数据信息
print(df_train.tail())#可以查看后10行的信息
# df_train.column  # 查看各个特征的具体名称

# 若想对数据的基本情况进行快速了解，可以用如下方式获得：
print(df_train.describe())  # df_train['SalePrice'].describe()能获得某一列的基本统计特征

#需要注意的是上述操作只能对数值型特征有效，
#同时也可以利用直方图查看某一特征数据的具体分布情况
# sns.distplot(df_train['SalePrice'])  # 图中的蓝色曲线是默认参数 kde=True 的拟合曲线特征
# plt.show()

#利用DataFrame的自身特性，可以很容易做出反应变量关系的散点图
# output,var,var1,var2 = 'SalePrice', 'GrLivArea', 'TotalBsmtSF', 'OverallQual'
# #
#
# fig,axes = plt.subplots(nrows=1,ncols=3,figsize=(16,5))
# df_train.plot.scatter(x=var,y=output,ylim=(0,800000),ax=axes[0])
# df_train.plot.scatter(x=var1,y=output,ylim=(0,800000),ax=axes[1])
# df_train.plot.scatter(x=var2,y=output,ylim=(0,800000),ax=axes[2])
# plt.show()

#从上图我们注意到，OverQual属性虽然是数值型变量，但具有明显的有序性，此时对于这样的变量，采用箱形图显示效果更佳：
# fig, ax = plt.subplots(figsize=(8,6))
# sns.boxplot(x=var2,y=output,data=df_train)
# ax.set_ylim(0,800000)
# plt.show()


#上述箱形图的绘制matplotlib也能做到，但相对麻烦，而对于下面YearBuilt这个特征，用seaborn绘制出来的效果简洁而美观：

# var3 = 'YearBuilt'
# fig,ax = plt.subplots(figsize = (16,8))
# sns.boxplot(x=var3,y=output,data=df_train)
# ax.set_ylim(0,800000)
# plt.xticks(rotation=90)
# plt.show()

# 除此之外，seaborn一个比较强大而方便的功能在于，可以对多个特征的散点图、直方图信息进行整合，得到各个特征两两组合形成的图矩阵：


# var_set = ['SalePrice', 'OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath', 'YearBuilt']
# sns.set(font_scale=1.25)  # 设置横纵坐标轴的字体大小
# sns.pairplot(df_train[var_set])  # 7*7图矩阵
# # 可在kind和diag_kind参数下设置不同的显示类型，此处分别为散点图和直方图，还可以设置每个图内的不同类型的显示
# plt.show()

#有数据特征较多，为了方便展示，我们先创建一些数据：
# df_tr = pd.read_csv(r'./train.csv').drop('Id',axis=1)
# df_X = df_tr.drop('SalePrice',axis=1)
# df_y = df_tr['SalePrice']
# quantity = [attr for attr in df_X.columns if df_X.dtypes[attr] != 'object']  # 数值变量集合
# quality = [attr for attr in df_X.columns if df_X.dtypes[attr] == 'object']  # 类型变量集合

#对数值型数据进行melt操作，使其具有两列，分别为变量名，取值
# melt_X = pd.melt(df_X,value_vars = quantity)
# melt_X.head()
# melt_X.tail()

# sns.FacetGrid()默认会根据melt_X['variable']内的取值做unique操作，得到最终子图的数量，然后可以利用col_wrap设置每行显示的子图数量（不要求必须填满最后一行），sharex、sharey设置是否共享坐标轴；

# g = sns.FacetGrid(melt_X, col="variable",  col_wrap=5, sharex=False, sharey=False)
# g = g.map(sns.distplot, "value")  # 以melt_X['value']作为数据

#上面主要是单个或两个特征的数据分布进行分析
#下面是对各个特征间的关系进行分析
# 最简单地，直接获取整个DataFrame数据的协方差矩阵并利用sns.heatmaP()进行可视化

# corrmat = df_train.corr()
# f, ax = plt.subplots(figsize=(12, 9))
# sns.heatmap(corrmat, vmax=.8, square=True, ax=ax)  # square参数保证corrmat为非方阵时，图形整体输出仍为正方形
# plt.show()

#然后我们可以选取与output变量相关系数最高的10个特征查看相关情况，
#找出那些相互关联性比较强的特征
# k = 10
# top10_attr = corrmat.nlargest(k, output).index
# top10_mat = corrmat.loc[top10_attr, top10_attr]
# fig,ax = plt.subplots(figsize=(8,6))
# sns.set(font_scale=1.25)
# sns.heatmap(top10_mat, annot=True, annot_kws={'size':12}, square=True)
# # 设置annot使其在小格内显示数字，annot_kws调整数字格式
# plt.show()