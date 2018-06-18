#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : used_demo04.py
# @Author: Lmm
# @Date  : 2018-04-25 12:45
# @Desc  :
from requests import put,get
put("http://localhost:5000/add",data = {"value_array": [{ "value":12},{ "value":18},{ "value":10}]}).json()

get('http://localhost:5000/add').json