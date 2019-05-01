# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:44:57 2019

@author: villa
"""


import zmq
import sys
import hashlib


context=zmq.Context()
s=context.socket(zmq.REQ)
s.connect("tcp://localhost:5556")

f = open('im.png', 'rb')

while True:
	piece = f.read(10485760)   #tamano en bytes 10485760 = 10 mb 
	s.send(bytes(piece))
	r=s.recv_string()
	print(r)
	if not piece:
		print("not found piece")
		break
	(piece)
f.close()

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

md5 = hashlib.md5()
sha1 = hashlib.sha1()

with open('im.png', 'rb') as f:
	while True:
		data = f.read(BUF_SIZE)
		if not data:
			break
		#md5.update(data)
		sha1.update(data)

#print("MD5: {0}".format(md5.hexdigest()))
print("SHA1: {0}".format(sha1.hexdigest()))
	

	





	

