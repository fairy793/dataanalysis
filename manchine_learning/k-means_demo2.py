#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : k-means_demo2.py
# @Author: Lmm
# @Date  : 2018-05-13 20:07
# @Desc  :
import KNN
from numpy import *

dataSet, labels = KNN.createDataSet()
testX = array([1.2, 1.0])
k = 3

outputLabel = KNN.kNNClassify(testX, dataSet, labels, 3)
print "Your input is:", testX, "and classified to class: ", outputLabel

testX = array([0.1, 0.3])
outpuyLabel = KNN.kNNClassify(testX, dataSet, labels, 3)
print "Your input is:", testX, "and classified to class: ", outputLabel

