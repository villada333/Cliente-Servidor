import zmq
import sys
import hashlib
import argparse
import os

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

def recibir(diccionarios1,hashf,nombrearchivo,parte,numeroparte):
	file = open('data/'+hashf,'wb') #aqui guardo el dato que llega
	file.write(parte)       #adjunta al archivo
	file.close()
	socketlisten.send_string(numeroparte) #devuelve el numero se partes recibidas
	print('parte recibida del cliente = '+numeroparte) #muestra el numero de partes recibidas
	diccionarios1[hashf]=nombrearchivo
	print('agregado a la base de datos'+'\n')
	return diccionarios1

def enviar(diccionarios1,hashf,numeroparte):
	nombrearchivo=diccionarios1[hashf]
	file = open('data/'+hashf, 'rb') #el archivo a enviar
	parte = file.read(10485760)   #tamano en bytes 10485760 = 10 mb
	print(nombrearchivo)
	socketlisten.send_multipart([bytes(parte),nombrearchivo.encode('utf-8')])
	print('parte enviada al cliente = '+str(numeroparte))
	file.close()

if __name__=='__main__':

	diccionarios1={}
	codigo='3'
	capacidad='1000'

	parser = argparse.ArgumentParser(description='Servidor.')
	parser.add_argument('ipserver', help='# puerto por el que va a escuchar')
	parser.add_argument('portserver', help='# puerto por el que va a escuchar')
	parser.add_argument('portbalancer', help='# puerto del balanceador')
	args = parser.parse_args()

	context=zmq.Context()
	socketlisten=context.socket(zmq.REP)
	socketlisten.bind('tcp://*:'+args.portserver)
	socketbalancer=context.socket(zmq.REQ)
	socketbalancer.connect("tcp://"+args.portbalancer)

	myipserver=args.ipserver+":"+args.portserver

	socketbalancer.send_multipart([codigo.encode('utf-8'),capacidad.encode('utf-8'),myipserver.encode('utf-8')])	#codigo 3 para agregar servidor a balanceador,numero de partes, puerto del server
	mensaje=socketbalancer.recv_string()
	print(mensaje)

	print('servidor iniciado y escuchando por el puerto '+args.portserver+' y conectado con el balanceador por '+args.portbalancer)

	while True:
		m=socketlisten.recv_multipart()                                                                                                                                    
		if m[0].decode('utf-8')=='1':   #recibe(codigo,hash,nombrearchivo,parte,numeroparte)
			try:
				diccionarios1=recibir(diccionarios1,m[1].decode('utf-8'),m[2].decode('utf-8'),m[3],m[4].decode('utf-8'))
			except Exception as e:
				raise e

		if m[0].decode('utf-8')=='2':   #recibe(codigo,hash,numeroparte)
			try:
				enviar(diccionarios1,m[1].decode('utf-8'),int(m[2].decode('utf-8')))
			except Exception as e:
				raise e
