#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : api_demo02.py
# @Author: Lmm
# @Date  : 2018-04-22 19:41
# @Desc  :
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

# from requests import put,get
# put('http://127.0.0.1:5000/todo1', data={'data': 'Remember the milk'}).json()

if __name__ == '__main__':
    app.run(debug=True)