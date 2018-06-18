#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : api_demo04.py
# @Author: Lmm
# @Date  : 2018-04-25 12:31
# @Desc  : api小模板04
from flask import Flask
from flask_restful import Resource,Api,reqparse,request
app = Flask(__name__)
api = Api(app)
todos = {}
class TodoList(Resource):
	def get(self):
		result = 0
		value_array = todos["value_array"]
		for i,single in enumerate(value_array):
			result = single["value"]
		return {"result":result}
		
	def put(self):
		todos["value_array"] = request.form['value_arrat']
		return {
			"value_array":todos["value_array"]
		}
	
api.add_resource(TodoList,
				 '/',
				 'add')

if __name__ == '__main__':
	app.run(debug = True)