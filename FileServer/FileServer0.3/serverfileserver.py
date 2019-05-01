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

r=0 #contador de partes

file = open("temp","wb") #aqui guardo los datos que van llegando

while True:
	m=s.recv()	#recibe
	file.write(m)	#adjunta al archivo
	sizefile=sys.getsizeof(m)	#determina el tamano para calcular el hash al final
	r=r+1	#aumenta el contador

	if sizefile<10485760: #si llega la ultima parte calcula el hash
		BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
		md5 = hashlib.md5()
		sha1 = hashlib.sha1()
		with open('temp', 'rb') as f:
			while True:
				data = f.read(BUF_SIZE)
				if not data:
					break
				sha1.update(data)
		print("SHA1: {0}".format(sha1.hexdigest()))
		r=0 #reinicio el contador para el proximo envio
	
	print(r) #muestra el numero de partes recibidas
	s.send_string(str(r)) #devuelve el numero se partes recibidas




	
