
import sys
import zmq
import os
import argparse
import json

def asignador(indice,hashf,nombrearchivo,dic,servers,numberservers):
	duplicado=consulta(indice,hashf)
	if duplicado == True:
		respuesta='Ya esta el archivo'
		socketlisten.send_multipart([hashf.encode('utf-8'),respuesta.encode('utf-8')])
	else:
		file = open('temptablahashbalanceador.json', 'wb') 
		file.write(dic)
		file.close()
		i=0
		with open('temptablahashbalanceador.json') as file:
			temphash = json.load(file)
		file.close()
		indice[hashf]={}
		for key in temphash:
			indice[hashf][key]="tcp://"+servers[i][0]
			i=i+1
			if i > numberservers:
				i=0
			servers[i][1]=int(servers[i][1])-1
		with open('temptablahashbalanceador.json', 'w') as file:
			json.dump(indice[hashf], file)
		file.close()
		file = open('temptablahashbalanceador.json', 'rb') 
		parte=file.read(10485760)   #tamano en bytes 10485760 = 10 mb 
		socketlisten.send_multipart([hashf.encode('utf-8'),bytes(parte)])
		file.close()

def buscador(indice,hashf):
	try:
		tempdic=indice[hashf]
		with open('templisthashsesforclient.json', 'w') as file:
			json.dump(tempdic, file, indent=4)
		file.close()
		file = open('templisthashsesforclient.json', 'rb')
		parte=file.read(10485760)   #tamano en bytes 10485760 = 10 mb
		socketlisten.send(bytes(parte))
		file.close()
		os.remove('templisthashsesforclient.json')
	except:
		codigoerror='0'
		print('error al buscar el hash en el indice'+'\n')
		socketlisten.send(codigoerror.encode('utf-8'))

def consulta(indice,hashf):
	if hashf in indice:
		return True
	else:
		return False
	

if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Balanceador.')
	parser.add_argument('portbalancer', help='# puerto por el que va a escuchar')
	args = parser.parse_args()

	context=zmq.Context()
	socketlisten=context.socket(zmq.REP)
	socketlisten.bind("tcp://*:"+args.portbalancer)
	print('Balanceador iniciado y escuchando por el puerto '+args.portbalancer)

	numberservers=-1
	servers=[]
	indice={}

	while True:
		print('Servidores , Capacidad ')
		print(servers)
		print('Numero de servidores ='+str(numberservers+1))
		print('Archivos en server = ')
		for key in indice:
			print(key)
		print('------- Escuchando ----------')
		mensaje=socketlisten.recv_multipart()    #recibe(codigo,hasharchivo,nombrearchivo,json con hashes)
		if mensaje[0].decode('utf-8')=='1':
			print('Asignador')
			asignador(indice,mensaje[1].decode('utf-8'),mensaje[2].decode('utf-8'),mensaje[3],servers,numberservers)
		if mensaje[0].decode('utf-8')=='2': #recibe(codigo,hash busqueda)
			print ('Buscando = '+mensaje[1].decode('utf-8'))
			buscador(indice,mensaje[1].decode('utf-8'))
		if mensaje[0].decode('utf-8')=='3': #recibe(codigo,partes disponibles,puerto del server)
			print ('Agregando Server')
			servers.append([mensaje[2].decode('utf-8'),mensaje[1].decode('utf-8')])
			numberservers=numberservers+1
			socketlisten.send_string("Servidor agregado correctamente")
