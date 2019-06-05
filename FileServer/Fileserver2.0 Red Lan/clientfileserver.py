
import zmq
import sys
import hashlib
import argparse
import os
import json


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

def hasparte(parte):
	sha1 = hashlib.sha1()
	sha1.update(parte)
	return sha1

def balanceador(nombrearchivo):	#recibe el nombre del archivo a tratar
	tempdic={}
	codigo='1'
	sha1 = hashlib.sha1()
	temphashfile=str(calcularhash(nombrearchivo).hexdigest())
	file = open(nombrearchivo, 'rb') #el archivo a enviar
	parte=file.read(10485760)   #tamano en bytes 10485760 = 10 mb 
	tamanoparte=sys.getsizeof(parte)
	while True:
		if tamanoparte < 10485760:
			break
		temphashpart=str(hasparte(parte).hexdigest())
		tempdic[temphashpart]='None'
		parte=file.read(10485760)   #tamano en bytes 10485760 = 10 mb 
		tamanoparte=sys.getsizeof(parte)
	file.close()
	with open('data/temptablahashcliente.json', 'w') as file:
		json.dump(tempdic, file, indent=4)
	file.close()
	file = open('data/temptablahashcliente.json', 'rb') 
	parte = file.read(10485760)   #tamano en bytes 10485760 = 10 mb 
	file.close()
	s=context.socket(zmq.REQ)
	s.connect("tcp://"+args.port)
	s.send_multipart([codigo.encode('utf-8'),temphashfile.encode('utf-8'),nombrearchivo.encode('utf-8'),bytes(parte)])
	mensaje=s.recv_multipart()
	s.close()
	if mensaje[1].decode('utf-8')=='Ya esta el archivo':
		print(mensaje[1].decode('utf-8'))
		return True
	else:
		file = open('data/temptablahashcliente.json', 'wb') 
		file.write(mensaje[1])
		file.close()
		os.rename('data/temptablahashcliente.json',temphashfile+nombrearchivo)
		return False


def enviar(nombrearchivo):
	codigo='1'
	sha1 = hashlib.sha1()
	temphashfile=str(calcularhash(nombrearchivo).hexdigest())
	i=0
	repetido=balanceador(nombrearchivo)
	if repetido == False:
		with open(temphashfile+nombrearchivo) as file:
			temptablahash = json.load(file)
		file.close()
		file = open(nombrearchivo, 'rb') #el archivo a enviar
		parte = file.read(10485760)   #tamano en bytes 10485760 = 10 mb 
		for key in temptablahash:
			s=context.socket(zmq.REQ)
			s.connect(temptablahash[key])
			print(temptablahash[key])
			s.send_multipart([codigo.encode('utf-8'),key.encode('utf-8'),nombrearchivo.encode('utf-8'),bytes(parte),str(i).encode('utf-8')]) #envia(codigo,hash,nombrearchivo,parte,numeroparte)
			mensaje=s.recv_string()
			parte = file.read(10485760)   #tamano en bytes 10485760 = 10 mb
			print('parte '+mensaje+' enviada al servidor '+temptablahash[key])
			i=i+1
			s.close()
		file.close()
		print("---CORRECTAMENTE ENVIADO---"+'\n')
		print('El hash de '+nombrearchivo+' para recuperarlo es '+temphashfile)


def recibir(nombrearchivo): #recibe(nombre,parte)
	codigo='2'
	s=context.socket(zmq.REQ)
	s.connect("tcp://"+args.port)
	s.send_multipart([codigo.encode('utf-8'),nombrearchivo.encode('utf-8')])
	mensaje=s.recv()
	s.close()
	if mensaje.decode('utf-8')=='0':
		print('hash no encontrado')
	else:
		file = open('milistadepartesenservers.json', 'wb') 
		file.write(mensaje)
		file.close()
		i=0 #contador de partes
		with open('milistadepartesenservers.json') as file:
			temptablahash = json.load(file)
		file.close()
		file = open('desc-'+nombrearchivo, 'wb') #el archivo a enviar
		for key in temptablahash:
			s=context.socket(zmq.REQ)
			s.connect(temptablahash[key])
			s.send_multipart([codigo.encode('utf-8'),key.encode('utf-8'),str(i).encode('utf-8')]) #envia(codigo,hash,nombrearchivo,parte,numeroparte)
			mensaje=s.recv_multipart()
			file.write(mensaje[0])
			print('parte '+str(i)+' recibida del servidor '+temptablahash[key])
			i=i+1
			s.close()
		file.close()
		os.rename('desc-'+nombrearchivo,'descargado-'+mensaje[1].decode('utf-8'))
		print('\n'+'archivo recibido correctamente')


def buscarhash(codigo,hash):
	s.send_multipart([codigo.encode('utf-8'),hash.encode('utf-8')])
	mensaje=s.recv()


if __name__=='__main__':
		parser = argparse.ArgumentParser(description='Cliente.')
		parser.add_argument('port', help='# puerto al que se va a conectar')
		args = parser.parse_args()
		context=zmq.Context()
		print('Cliente iniciado \n')

		while True:
			print('\n1)Subir Archivo \n2)Descargar archivo \nopcion = ')
			opcion=input()
			if opcion == '1':
				try:
					print('Nombre del archivo a enviar = ')
					nombre=input()
					print(nombre)
					enviar(nombre)
				except:
					print(nombre+' no corresponde a un archivo en el directorio')
			else:
				print('nombre del hash para recibir = ')
				nombre=input()
				recibir(nombre)
		

