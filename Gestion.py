#!/usr/bin/python
import sys
from snimpy.manager import Manager as M
from snimpy.manager import load

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
def lector():

def setter(m):
	"Lee el archivo linea a linea y escribe los datos en el dispositivo"
	f=open(archivo, 'r')
	for line in f:
		a=line.split()
		if (a):
			print("Valor Anterior de ", a[0], getattr(m, a[0], a[1]))
			setattr(m, a[0], a[1])

def checker(m):
	"Lee el archivo linea a linea y comprueba los datos en el dispositivo"
	f=open(archivo, 'r')
	for line in f:
		a=line.split()
		if (a):
			print("Valor buscado", a[0], "=", a[1])
			if (a[1]==getattr(m, a[0])):
				print("Correcto")

###################################
# Cominenza el programa principal #
###################################
if __name__=="__main__":
	# Carga las mibs
	load("mibs/RFC1155-SMI.mib")
	load("mibs/RFC-1212.mib")
	load("mibs/rfc1213.mib")
	# Conexion con el servidor
	m=M(ip, community="public", version=1)

	# Solo comprobar
	if (check):
		checker(m)
	# Asignar y comprobar
	else:
		setter(m)
		checker(m)


