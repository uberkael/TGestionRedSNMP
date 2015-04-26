#!/usr/bin/python
import sys	# Para los argumentos
import re	# Para CheckeaServidor
###################
# Biblioteca HNMP #
###################
# https://github.com/trehn/hnmp
from hnmp import SNMP

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
def lector(snmp, funcion):
	"Lee el archivo linea a linea y escribe los datos en el dispositivo"
	try:
		f=open(archivo, 'r')
		for line in f:
			a=line.split()
			if (len(a)==2):
				if(a[0][0]=="#"):
					# print("Error: la linea es un comentario")
					pass
				else:
					funcion(snmp, a)
			else:
				# print("Error: la linea es incorrecta")
				pass
	except Exception as e:
		print("Error", e)
	finally:
		pass

def setter(snmp, a):
	"Escribe los datos en el dispositivo por SNMP"
	print("Valor Anterior de", a[0], snmp.get(a[0]))
	snmp.set(a[0], a[1])

def checker(snmp, a):
	"Comprueba los datos en el dispositivo por SNMP"
	estado=0 # no errores
	print("Valor buscado", a[0], "=", a[1])
	print(snmp.get(a[0]))
	if (a[1]==snmp.get(a[0])):
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
		# TODO: Carga las mibs
		print ("Carga las mibs")
		# Conexion con el servidor
		snmp = SNMP(servidor, community="public")  # v2c

		lineas=cuentaLineas(archivo)
		# Solo comprobar
		if (check):
			lector(snmp, checker)
		# Asignar y comprobar
		else:
			lector(snmp, setter)
			lector(snmp, checker)
		# TODO: Fin->Bucle Idle
		print("Fin")

