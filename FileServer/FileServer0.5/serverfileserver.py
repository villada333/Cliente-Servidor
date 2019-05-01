# -*- coding: utf-8 -*-
'''
Created on Thu Apr  4 14:44:57 2019

@author: villa
'''
import zmq
import sys
import hashlib
import os

context=zmq.Context()
s=context.socket(zmq.REP)
s.bind('tcp://*:5556')

def calcularhash(nombrearchivo):
	BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
	sha1 = hashlib.sha1()
	with open('tempserver', 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha1.update(data)
	return sha1

def recibir(diccionario,m):
	r=0 #contador de partes
	file = open('tempserver','wb') #aqui guardo los datos que van llegando
	while True:
		file.write(m[3])	#adjunta al archivo
		sizefile=sys.getsizeof(m[3])	#determina el tamano para calcular el hash al final
		r=r+1	#aumenta el contador
		if sizefile<10485760: #si llega la ultima parte calcula el hash
			hashtemp=str(calcularhash('tempserver').hexdigest())
			if m[1].decode('utf-8') == hashtemp:
				print('\n'+'-------Hash Correcto-------')
				file.close()
				os.rename('tempserver',m[1].decode('utf-8'))
				diccionario[m[1].decode('utf-8')]=m[2].decode('utf-8')
				print('agregado a la base de datos'+'\n')
				r=0 #reinicio el contador para el proximo envio
				s.send_string(str('Hash para descargar este archivo '+hashtemp+'\n')) #devuelve el numero se partes recibidas
				print('\n'+'hash para descargar este archivo '+hashtemp+'\n')
				return diccionario
		else:
			print('parte recibida del cliente = '+str(r)) #muestra el numero de partes recibidas
			s.send_string(str(r)) #devuelve el numero se partes recibidas
			m=s.recv_multipart()	#recibes

def enviar(hashcliente,diccionario):
	nombrearchivo=diccionario[hashcliente]
	f = open(hashcliente, 'rb') #el archivo a enviar
	piece = f.read(10485760)   #tamano en bytes 10485760 = 10 mb 
	sizepiece=sys.getsizeof(piece)
	while sizepiece>10485760:
		s.send_multipart([nombrearchivo.encode('utf-8'),bytes(piece)])
		r=s.recv_string()
		print('parte enviada al cliente = '+r)
		piece = f.read(10485760)   #tamano en bytes 10485760 = 10 mb
		sizepiece=sys.getsizeof(piece)
	s.send_multipart([nombrearchivo.encode('utf-8'),bytes(piece)])
	f.close()
	
mibase={}

while True:
	m=s.recv_multipart()	#recibe
	if m[0].decode('utf-8')=='1':
		mibase=recibir(mibase,m)
	if m[0].decode('utf-8')=='2':
		enviar(m[1].decode('utf-8'),mibase)
