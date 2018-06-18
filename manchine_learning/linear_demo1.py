#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : linear_demo1.py
# @Author: Lmm
# @Date  : 2018-05-13 18:13
# @Desc  : 机器学习最小二乘法例子
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets,linear_model
from sklearn.metrics import mean_squared_error,r2_score

#加载数据集
diabetes = datasets.load_diabetes()

#仅仅使用一个特征值
diabetes_X = diabetes.data[:,np.newaxis,2]

#将数据中训练集中分离出来
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

#将目标对象从训练集中分离出来
diabetes_y_train = diabetes_X[:-20]
diabetes_y_test = diabetes_X[-20:]

#创建最小回归二乘法对象
regr = linear_model.LinearRegression()

#利用训练集训练模型
regr.fit(diabetes_X_train,diabetes_y_train)

#利用训练集做预测
diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()