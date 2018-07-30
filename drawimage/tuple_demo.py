#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : tuple_demo.py
# @Author: Lmm
# @Date  : 2018-07-30 22:47
# @Desc  :
from turtle import *
import turtle
def draw(radius ,color1 , color2):
    #设置画笔的大小
    turtle.width(3)
    #设置画笔颜色和填充颜色
    turtle.color("black",color1)
    #绘制鱼
    turtle.begin_fill()
    #绘制圆
    #当半径为正数时，逆时针绘制
    #当半径为负数时，顺时针绘制
    turtle.circle(radius/2,180)
    turtle.circle(radius,180)
    #向左旋转180度
    turtle.left(180)
    turtle.circle(-radius/2,180)
    turtle.end_fill()
    turtle.left(90)
    #抬起画笔
    turtle.penup()
    turtle.forward(radius*0.35)
    turtle.right(90)
    #放下画笔
    turtle.pendown()
    turtle.color(color2,color2)
    #绘制鱼眼
    turtle.begin_fill()
    turtle.circle(radius*0.15)
    turtle.end_fill()
    turtle.left(90)
    turtle.penup()
    turtle.backward(radius*0.35)
    turtle.pendown()
    turtle.left(90)

def main():
    turtle.setup(500,500)
    #绘制白色鱼眼的黑鱼
    draw(200,"black","white")

    draw(200,"white","black")

    turtle.hideturtle()

main()
turtle.mainloop()
 
