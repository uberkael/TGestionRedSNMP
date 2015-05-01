#!/usr/bin/python
from __future__ import print_function # Python 2 Para print (1, 2) Debe estar al inicio
import sys	# Para los argumentos
import re	# Para CheckeaServidor
###################
# Biblioteca HNMP #
###################
# https://github.com/trehn/hnmp
from hnmp import SNMP

###########################
# Compatibilidad Python 2 #
###########################
versionPy=sys.version_info
if versionPy < (3, 0):
	from io import open # Para la lectura de fichero con opciones Python 3

######################
# Variables globales #
######################
servidor="10.10.10.2"
archivo='configuracion.ini'
check=False # check, solo comprueba

###################################
# Argumentos en linea de comandos #
###################################
if (len(sys.argv)==2):
	if (sys.argv[1].lower()=="check"):
		check=True
	else:
		servidor=sys.argv[1]
# Si hay tres argumentos es el servidor y un archivo
if (len(sys.argv)==3):
	servidor=sys.argv[1]
	if (sys.argv[2].lower()=="check"):
		check=True
	else:
		archivo=sys.argv[2]
# Si hay mas de tres argumentos es el servidor y un archivo y check
if (len(sys.argv)>3):
	servidor=sys.argv[1]
	archivo=sys.argv[2]
	if (sys.argv[3].lower()=="check"):
		check=True
	else: # Si el tercero no es check algo esta mal
		print("Uso:", sys.argv[0], "<servidor> <archivo> [<check>]")
		quit()

###########################
# Definicion de funciones #
###########################
def lector(snmp, funcion):
	"Lee el archivo linea a linea y llama a checker() o setter() en cada una"
	try:
		# Lineas y para barra de progreso
		lineas=cuentaLineas(archivo)
		porcentaje=100/lineas
		# Lectura del archivo
		f=open(archivo, 'r')
		progreso=0
		bprogreso=0
		for line in f:
			if versionPy < (3, 0):	# Python2 strings no unicode
				line=line.encode('ascii','ignore') # Si hay caracteres no ASCII
				line=str(line)
			progreso=progreso+1
			bprogreso=porcentaje*progreso
			a=line.split()
			if (len(a)>=2):
				if(a[0][0]=="#"):
					# print("Error: la linea es un comentario")
					pass
				else:
					if (not funcion(snmp,a)):
						print(a[0], a[1], "CORRECTO")
					else:
						print(a[0], a[1], "ERROR")
			else:
				# print("Error: la linea es incorrecta")
				pass
	except Exception as e:
		print("Error de lectura", e)
	finally:
		pass

def setter(snmp, a):
	"Escribe los datos en el dispositivo por SNMP"
	# respuesta=str(snmp.get(a[0]))
	# print("Valor Anterior de", a[0], respuesta)
	snmp.set(a[0], a[1])
	return 0 # no errores

def checker(snmp, a):
	"Comprueba los datos en el dispositivo por SNMP"
	estado=0 # no errores
	# print("Valor buscado", a[0], "=", a[1])
	respuesta=str(snmp.get(a[0]))
	# print(respuesta)
	if (a[1]==respuesta):
		# print("Correcto")
		pass # sin errores
	else:
		# print("Error: GET ha devuelto otra cosa")
		estado=1 # errores
	return estado

def funcionPrincipal(servidor):
	"La funcion que realiza el trabajo, checkeaServidor()->lector()->setter()/checker()"
	if checkeaServidor(servidor):
		# Conexion con el servidor
		snmp = SNMP(servidor, community="public")  # v2c
		# Solo comprobar
		if (check):
			lector(snmp, checker)
		# Asignar y comprobar
		else:
			lector(snmp, setter)
			lector(snmp, checker)
		informacion="Fin Iteracion"
	else:
		informacion="Error "+servidor+" no es una ip"
	return informacion

########################
# Funciones auxiliares #
########################
def funcionConsola():
	informacion="TODO: verificar que hay un nuevo dispositivo, pulsa intro"
	global servidor
	if versionPy < (3, 0):	# Python2
		raw_input(informacion)
	else:
		input(informacion)
	return funcionPrincipal(servidor)

def checkeaServidor(servidor):
	"Comprueba que la ip tiene buen formato"
	regexip="^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
	if re.match(regexip, servidor):
		return 1
	else:
		return 0

def geneRead(reader):
	"Funcion auxiliar de cuentaLineas()"
	b=reader(1024*1024)
	while b:
		yield b
		b=reader(1024*1024)

def cuentaLineas(archivo):
	"Lector rapido de numero de lineas http://stackoverflow.com/a/27518377/3052862"
	f=open(archivo, 'rb')
	f_gen=geneRead(f.raw.read)
	return sum(buf.count(b'\n') for buf in f_gen)

###################################
# Comienza el programa principal #
###################################
if __name__=="__main__":
		# Bucle principal Idle
		while (True): # Solo para las interfaces de consola
			print(funcionConsola())



