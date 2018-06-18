#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : baseline.py
# @Author: Lmm
# @Date  : 2018-06-11 21:03
# @Desc  :

import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer #对文本提供特征向量
from sklearn.preprocessing import OneHotEncoder,LabelEncoder #LabelEncoder是对不连续的数字或者文本进行编号
from scipy import sparse#稀疏矩阵
import os
#OneHotEncoder 用于将表示分类的数据扩维
# sklearn.preprocessing.LabelEncoder()：标准化标签，将标签值统一转换成range(标签值个数-1)范围内
path = "."#设置存放路径
ad_feature = pd.read_csv(path+'/data/adFeature.csv')
if os.path.exists(path +'/data/userFeature.csv'): #读取广告特征文件
    user_feature=pd.read_csv(path+'/data/userFeature.csv')
else:
    userFeature_data = []
    with open(path +'/data/userFeature.data', 'r') as f:
        for i, line in enumerate(f):
            line = line.strip().split('|')
            userFeature_dict = {}
            for each in line:
                each_list = each.split(' ')
                userFeature_dict[each_list[0]] = ' '.join(each_list[1:])
            userFeature_data.append(userFeature_dict)
            if i % 100000 == 0:
                print(i)
        user_feature = pd.DataFrame(userFeature_data)#DataFrame是Pandas中的一个表结构的数据结构，包括三部分信息，表头（列的名称），
        # 表的内容（二维矩阵），索引（每行一个唯一的标记）
        user_feature.to_csv(path+'/data/userFeature.csv', index=False)
        del userFeature_data
train = pd.read_csv(path+'/data/train.csv')#训练集
predict = pd.read_csv(path+'/data/test1.csv')#预测集
train.loc[train['label'] == -1, 'label'] =0 #缺失值处理
predict['label'] = -1
data = pd.concat([train, predict])#合并训练集和测试集
data = pd.merge(data, ad_feature, on='aid', how='left')#数据进行左右拼接
data = pd.merge(data, user_feature, on='uid', how='left')
data = data.fillna('-1')#如果存在缺失值则对其进行处理
train_x = train[['aid']]
test_y = train[['aid']]

#---------------------查看aid的分佈情況Start----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 忽略警告
import warnings
warnings.filterwarnings('ignore')
# 查看训练集的广告ID分布，左图是原始广告ID分布，右图是将广告ID对数化之后的分布
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
g1 = sns.distplot(train_x,hist = True,label='skewness:{:.2f}'.format(train_x.skew()),ax = ax1)
g1.legend()
g1.set(xlabel = 'aid')
g2 = sns.distplot(np.log1p(train_x),hist = True,label='skewness:{:.2f}'.format(np.log1p(train_x).skew()),ax=ax2)
g2.legend()
g2.set(xlabel = 'log(aid+1)')
plt.show()

# ----------------------------查看分布情況end --------------------------------------------------------------------------
one_hot_feature = ['LBS', 'age','carrier','consumptionAbility','education','gender','house','os','ct','marriageStatus','advertiserId','campaignId', 'creativeId',
       'adCategoryId', 'productId', 'productType']
vector_feature = ['appIdAction', 'appIdInstall','interest1','interest2','interest3','interest4','interest5','kw1','kw2','kw3','topic1','topic2','topic3']
for feature in one_hot_feature:
    try:
        data[feature] = LabelEncoder().fit_transform(data[feature].apply(int))
    except:
        data[feature] = LabelEncoder().fit_transform(data[feature])

train = data[data.label != -1] #将训练集合设置为lable不是-1的
train_y = train.pop('label') #删除lable列
# train, test, train_y, test_y = train_test_split(train,train_y,test_size=0.2, random_state=2018)
test = data[data.label == -1]
res = test[['aid', 'uid']]
test = test.drop('label',axis=1)#去掉非属性列
enc = OneHotEncoder() #对分类数据进行扩维
# train_x = train[['creativeSize']]
# test_x = test[['creativeSize']]
train_x = train[['aid']]
test_y = train[['aid']]



# for feature in one_hot_feature:
#     enc.fit(data[feature].values.reshape(-1, 1))
#     train_a = enc.transform(train[feature].values.reshape(-1, 1))
#     test_a = enc.transform(test[feature].values.reshape(-1, 1))
#     train_x = sparse.hstack((train_x, train_a))
#     test_x = sparse.hstack((test_x, test_a))
# print('one-hot prepared !')
#
# cv = CountVectorizer() #特征提取
# for feature in vector_feature:
#     cv.fit(data[feature])
#     train_a = cv.transform(train[feature])
#     test_a = cv.transform(test[feature])
#     train_x = sparse.hstack((train_x, train_a))
#     test_x = sparse.hstack((test_x, test_a))
# print('cv prepared !')
#
# def LGB_test(train_x,train_y,test_x,test_y):
#     print("LGB test")
#     clf = lgb.LGBMClassifier(
#         boosting_type='gbdt', num_leaves=31, reg_alpha=0.0, reg_lambda=1,
#         max_depth=-1, n_estimators=1000, objective='binary',
#         subsample=0.7, colsample_bytree=0.7, subsample_freq=1,
#         learning_rate=0.05, min_child_weight=50,random_state=2018,n_jobs=-1
#     )
#     clf.fit(train_x, train_y,eval_set=[(train_x, train_y),(test_x,test_y)],eval_metric='auc',early_stopping_rounds=100)
#     # print(clf.feature_importances_)
#     return clf, clf.best_score_[ 'valid_1']['auc']
#
# def LGB_predict(train_x,train_y,test_x,res):
#     print("LGB test")
#     clf = lgb.LGBMClassifier(
#         boosting_type='gbdt', num_leaves=31, reg_alpha=0.0, reg_lambda=1,
#         max_depth=-1, n_estimators=1500, objective='binary',
#         subsample=0.7, colsample_bytree=0.7, subsample_freq=1,
#         learning_rate=0.05, min_child_weight=50, random_state=2018, n_jobs=-1
#     )
#     clf.fit(train_x, train_y, eval_set=[(train_x, train_y)], eval_metric='auc',early_stopping_rounds=100)
#     res['score'] = clf.predict_proba(test_x)[:,1]
#     res['score'] = res['score'].apply(lambda x: float('%.6f' % x))
#     res.to_csv('../data/submission.csv', index=False)
#     os.system('zip ../data/baseline.zip ../data/submission.csv')
#     return clf
#
# model=LGB_predict(train_x,train_y,test_x,res)