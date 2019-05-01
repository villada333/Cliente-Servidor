# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:44:57 2019

@author: villa
"""
import zmq
import sys
import hashlib
import os

context=zmq.Context()
s=context.socket(zmq.REQ)
s.connect("tcp://localhost:5556")

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

def enviar(nombre):
	f = open(nombre, 'rb') #el archivo a enviar
	mihash=str(calcularhash(nombre).hexdigest())
	print("SHA1: "+mihash)
	piece = f.read(10485760)   #tamano en bytes 10485760 = 10 mb 
	sizepiece=sys.getsizeof(piece)
	codigo='1'
	while sizepiece>0:
		if not piece:
			print('el hash para descargar es = '+mihash+'\n')
			break
		s.send_multipart([codigo.encode('utf-8'),mihash.encode('utf-8'),nombre.encode('utf-8'),bytes(piece)]) #1 para enviar
		r=s.recv_string()
		piece = f.read(10485760)   #tamano en bytes 10485760 = 10 mb
		sizepiece=sys.getsizeof(piece)
		print('parte enviada al servidor = '+r)
		
	f.close()
	print('\n'+"---CORRECTAMENTE ENVIADO---"+'\n')

def recibir(codigo,hashserver): #recibe(nombre,parte)
	r=0 #contador de partes
	f = open('recibido','wb') #aqui guardo los datos que van llegando
	s.send_multipart([codigo.encode('utf-8'),hashserver.encode('utf-8')])
	m=s.recv_multipart()
	while True:
		f.write(m[1])	#adjunta al archivo
		sizepiece=sys.getsizeof(m[1])
		if sizepiece<10485760: 
			f.close()
			os.rename('recibido','descargado-'+m[0].decode('utf-8'))
			r=0 #reinicio el contador para el proximo envio
			break		
		else:
			r=r+1	#aumenta el contador
			print('parte recibida del servidor = '+str(r)) #muestra el numero de partes recibidas
			s.send_string(str(r)) #devuelve el numero se partes recibidas
			m=s.recv_multipart()	#recibe




nombre1='imagen.png'
nombre2='midiccionario.txt'
nombre3='cancion2.mp3'
codigo='0'

nombre='cancion.mp3'
hashserver='03c79f368cba886b28253a03763f046c0499c04b'	#hash cancion


hashserver1='7cff3c67339173959e98266a1b405ebb85fcd944'
hashserver2='81f7601a5c12771be1d2c188b4a213bc9c16e28c'
hashserver3='9dd16ab8904fbcb07d73900157e641d02777cf83'

enviar(nombre2)

recibir('2',hashserver2)#pedir (2,hash)


	
