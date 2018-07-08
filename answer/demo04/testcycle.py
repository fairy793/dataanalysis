#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : testcycle.py
# @Author: Lmm
# @Date  : 2018-07-08 18:01
# @Desc  : 约瑟夫环测试
# 有n个人围成一圈，顺序排号，从第一个人
#开始从1到k报数，报到k的人退出圈子，然后圈子
#缩小，从下一个人继续游戏，问最后留下的是原来的几号

def demo1(lst,k):
	#切片，以免影响原来的数据
	t_lst = lst[:]
	
	while len(t_lst) > 1:
		# print(t_lst)
		#模拟报数
		for i in range(k-1):
			print(t_lst.pop(0))
			t_lst.append(t_lst.pop(0))
		t_lst.pop(0)
	#游戏结束
	return t_lst[0]
# lst = list(range(1,11))
# print(demo(lst,3))

from  itertools import cycle
def demo2(lst,k):
	#切片，以免影响原来的数据
    t_lst = lst[:]
	#游戏一直进行到只剩下最后一个人
    while len(t_lst) > 1:
		#创建cycle对象
		c = cycle(t_lst)
		#从1到k报数
		for i in range(k):
			t = next(c)
		#一个人出局，圈子缩小
		index = t_lst.index(t)
		
		t_lst = t_lst[index+1:] + t_lst[:index]
    return t_lst[0]
# lst = list(range(1,11))
# print(demo2(lst,3))

