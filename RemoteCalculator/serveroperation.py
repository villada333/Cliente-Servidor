# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:44:57 2019

@author: villa
"""

import zmq

context=zmq.Context()
s=context.socket(zmq.REP)
s.bind("tcp://*:5556")

while True:
	r=0
	m=s.recv_string()
	maux=m.split(",")   #formato envio +,2,2 = 2+2
	sig=str(maux[0])
	a=int(maux[1])
	b=int(maux[2])
	if sig == "+":
		r=a+b
	elif sig == "-":
		r=a-b
	elif sig == "*":
		r=a*b
	elif sig == "/":
		r=a/b
	else:
		print("pailander")

	print(r)
	s.send_string(str(r))