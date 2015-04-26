#!/usr/bin/python
import sys

######################
# Variables globales #
######################
servidor="10.10.10.2"
archivo='configuracion.ini'
check=False

###################################
# Argumentos en linea de comandos #
###################################
# Si algun argumento es check, se hace un chequeo
# if (len(sys.argv)>1):
# 	for x in sys.argv:
# 		if ("check" in x.islower()):
# 			check=True
# Si hay segundo argumento es el servidor
if (len(sys.argv)==2):
	if sys.argv[1]=="check":
		check=True
	else:
		servidor=sys.argv[1]
# Si hay tres argumentos es el servidor y un archivo
if (len(sys.argv)==3):
	servidor=sys.argv[1]
	if sys.argv[2]=="check":
		check=True
	else:
		archivo=sys.argv[2]
if (len(sys.argv)>3):
	servidor=sys.argv[1]
	archivo=sys.argv[2]
	if sys.argv[2]=="check":
		check=True
	else:
		print("Uso:", sys.argv[0], "<servidor> <archivo> [<check>]")


###########################
# Definicion de funciones #
###########################
def setter():
	"Lee el archivo linea a linea y escribe los datos en el dispositivo"
	try:
		f=open(archivo, 'r')
		for line in f:
			a=line.split()
			if (len(a)>2):
				# TODO: setOID
				print("Valor Anterior de", a[0], "TODO: get", a[0])
				print("TODO: set", a[0], a[1])
	except Exception as e:
		print("Error", e)
	finally:
		pass

def checker():
	"Lee el archivo linea a linea y comprueba los datos en el dispositivo"
	try:
		f=open(archivo, 'r')
		for line in f:
			a=line.split()
			if (a):
				# TODO: getOID
				print("Valor buscado", a[0], "=", a[1])
				print("TODO: get", a[0], "y comprobacion")
				# if (a[1]==" get a[0] "):
					# print("Correcto")
	except Exception as e:
		print("Error", e)
	finally:
		pass

########################
# Funciones auxiliares #
########################
def CheckeaServidor():
	import re
	regexip="^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
	if re.match(regexip, servidor):
		print("Servidor correcto")
		return 1
	else:
		print ("Error ", servidor, " no es una ip")
		return 0

###################################
# Cominenza el programa principal #
###################################
if __name__=="__main__":

	if CheckeaServidor():
		# TODO: Carga las mibs
		print ("Carga las mibs")
		# TODO: Conexion con el servidor
		print ("Conexion con el servidor")

		# Solo comprobar
		if (check):
			checker()
		# Asignar y comprobar
		else:
			setter()
			checker()
		# TODO: Fin->Bucle Idle
		print("Fin")
