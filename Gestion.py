#!/usr/bin/python
import sys

######################
# Variables globales #
######################
ip="10.10.10.2"
archivo='configuracion.ini'
check=False

###################################
# Argumentos en linea de comandos #
###################################
# Si algun argumento es check, se hace un chequeo
if (len(sys.argv)>1):
	for x in sys.argv:
		if ("check" in x.islower()):
			check=True
# Si hay segundo argumento es la ip
if (len(sys.argv)==2):
	ip=sys.argv[1]
# Si hay tres argumentos es la ip y un archivo
if (len(sys.argv)>3):
	ip=sys.argv[1]
	archivo=sys.argv[2]

###########################
# Definicion de funciones #
###########################
def setter():
	"Lee el archivo linea a linea y escribe los datos en el dispositivo"
	f=open(archivo, 'r')
	for line in f:
		a=line.split()
		if (a):
			# TODO: setOID
			print("Valor Anterior de", a[0], "TODO: get", a[0])
			print("TODO: set", a[0], a[1])

def checker():
	"Lee el archivo linea a linea y comprueba los datos en el dispositivo"
	f=open(archivo, 'r')
	for line in f:
		a=line.split()
		if (a):
			# TODO: getOID
			print("Valor buscado", a[0], "=", a[1])
			print("TODO: get", a[0], "y comprobacion")
			# if (a[1]==" get a[0] "):
				# print("Correcto")

###################################
# Cominenza el programa principal #
###################################
if __name__=="__main__":
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
