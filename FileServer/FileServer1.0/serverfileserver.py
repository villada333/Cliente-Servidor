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
	with open(nombrearchivo, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha1.update(data)
	return sha1

def recibir(diccionario,hashf,nombrearchivo,parte,numeroparte):  
	file = open('tempserver'+hashf,'ab') #aqui guardo los datos que van llegando
	file.write(parte)	#adjunta al archivo
	file.close()
	s.send_string(numeroparte) #devuelve el numero se partes recibidas
	print('parte recibida del cliente = '+numeroparte) #muestra el numero de partes recibidas
	sizefile=sys.getsizeof(parte)	#determina el tamano para calcular el hash al final
	if sizefile<10485760: #si llega la ultima parte calcula el hash
		hashtemp=str(calcularhash('tempserver'+hashf).hexdigest())
		if hashf == hashtemp:
			print('\n'+'-------Hash Correcto-------')
			os.rename('tempserver'+hashf,hashf)
			print('\n'+'hash para descargar este archivo '+hashtemp+'\n')
			diccionario={hashtemp:nombrearchivo}
			print('agregado a la base de datos'+'\n')
			return diccionario
		else:
			print('hashes incorrectos')

def enviar(diccionario,hashf,numeroparte):
	nombrearchivo=diccionario[hashf]
	f = open(hashf, 'rb') #el archivo a enviar
	f.seek(10485760*numeroparte)   #tamano en bytes 10485760 = 10 mb
	piece = f.read(10485760)   #tamano en bytes 10485760 = 10 mb
	s.send_multipart([nombrearchivo.encode('utf-8'),bytes(piece)])
	sizepiece=sys.getsizeof(piece)
	print('parte enviada al cliente = '+str(numeroparte))
	f.close()
	


mibase={}


while True:
	m=s.recv_multipart()	

	if m[0].decode('utf-8')=='1':	#recibe(codigo,hash,nombrearchivo,parte,numeroparte)
		mibase=recibir(mibase,m[1].decode('utf-8'),m[2].decode('utf-8'),m[3],m[4].decode('utf-8'))

	if m[0].decode('utf-8')=='2':	#recibe(codigo,hash,numeroparte)
		enviar(mibase,m[1].decode('utf-8'),int(m[2].decode('utf-8')))

