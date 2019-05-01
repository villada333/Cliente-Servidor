# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:44:57 2019

@author: villa
"""



import zmq
import sys
import hashlib

context=zmq.Context()
s=context.socket(zmq.REP)
s.bind("tcp://*:5556")

r=0

file = open("prueba.png","wb") 

while True:
	
	m=s.recv()

	file.write(m)




	r=r+1

	if r==2:
		BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

		md5 = hashlib.md5()
		sha1 = hashlib.sha1()

		with open('prueba.png', 'rb') as f:
			while True:
				data = f.read(BUF_SIZE)
				if not data:
					break
				#md5.update(data)
				sha1.update(data)

		#print("MD5: {0}".format(md5.hexdigest()))
		print("SHA1: {0}".format(sha1.hexdigest()))









	
	print(r)
	s.send_string(str(r))




	