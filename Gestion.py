#!/usr/bin/python
import sys	# Para los argumentos
import re	# Para CheckeaServidor
#####################
# Biblioteca SNIMPY #
#####################
# http://snimpy.readthedocs.org/
from snimpy.manager import Manager as M
from snimpy.manager import load

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
def lector(m, funcion):
	"Lee el archivo linea a linea y escribe los datos en el dispositivo"
	try:
		f=open(archivo, 'r')
		for line in f:
			a=line.split()
			if (len(a)>=2):
				if(a[0][0]=="#"):
					# print("Error: la linea es un comentario")
				else:
					funcion(a, m)
			else:
				# print("Error: la linea es incorrecta")
	except Exception as e:
		print("Error", e)
	finally:
		pass

def setter(a, m):
	"Escribe los datos en el dispositivo por SNMP"
	print("Valor Anterior de ", a[0], getattr(m, a[0], a[1]))
	setattr(m, a[0], a[1])


def checker(a, m):
	"Comprueba los datos en el dispositivo por SNMP"
	estado=0 # no errores
	print("Valor buscado", a[0], "=", a[1])
	print(getattr(m, a[0]))
	if (a[1]==getattr(m, a[0])):
		print("Correcto")
	else:
		print("Error: GET ha devuelto otra cosa")
		estado=1 # errores
	return estado

########################
# Funciones auxiliares #
########################
def CheckeaServidor(servidor):
	"Comprueba que la ip tiene buen formato"
	regexip="^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
	if re.match(regexip, servidor):
		print("Servidor correcto")
		return 1
	else:
		print ("Error ", servidor, " no es una ip")
		return 0

def geneRead(reader):
	"Funcion auxiliar de cuentaLineas()"
	b = reader(1024 * 1024)
	while b:
		yield b
		b = reader(1024*1024)

def cuentaLineas(archivo):
	"Lector rapido de numero de lineas http://stackoverflow.com/a/27518377/3052862"
	f = open(archivo, 'rb')
	f_gen = geneRead(f.raw.read)
	return sum( buf.count(b'\n') for buf in f_gen )

###################################
# Comienza el programa principal #
###################################
if __name__=="__main__":

	if CheckeaServidor(servidor):
		# Carga las mibs
		load("mibs/RFC1155-SMI.mib")
		load("mibs/RFC-1212.mib")
		load("mibs/rfc1213.mib")
		# Conexion con el servidor
		m=M(ip, community="public", version=1)

		# Solo comprobar
		if (check):
			lector(m, checker)
		# Asignar y comprobar
		else:
			lector(m, setter)
			lector(m, checker)
		# TODO: Fin->Bucle Idle
		print("Fin")


