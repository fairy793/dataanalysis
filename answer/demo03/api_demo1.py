#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : api_demo1.py
# @Author: Lmm
# @Date  : 2018-04-22 19:27
# @Desc  : flask 搭建api初步学习使用

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)