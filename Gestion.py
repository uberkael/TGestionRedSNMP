#!/usr/bin/python
from __future__ import print_function # Python 2 Para print (1, 2) Debe estar al inicio
import sys	# Para los argumentos
import re	# Para CheckeaServidor
#####################
# Biblioteca SNIMPY #
#####################
# http://snimpy.readthedocs.org/
from snimpy.manager import Manager as M
from snimpy.manager import load

###########################
# Compatibilidad Python 2 #
###########################
versionPy=sys.version_info
if versionPy<(3, 0):
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
		print("Uso:", sys.argv[0], "<servidor><archivo> [<check>]")
		quit()

###########################
# Definicion de funciones #
###########################
def lector(m, funcion):
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
			if versionPy<(3, 0):	# Python2 strings no unicode
				line=line.encode('ascii', 'ignore') # Si hay caracteres no ASCII
				line=str(line)
			progreso=progreso+1
			bprogreso=porcentaje*progreso
			a=line.split()
			if (len(a)>=2):
				if(a[0][0]=="#"):
					print("Error: la linea es un comentario")
				else:
					if (not funcion(a, m)):
						cadena=a[0]+" "+a[1]+" CORRECTO"
						print(cadena)
					else:
						cadena=a[0]+" "+a[1]+" ERROR"
						print(cadena)
			else:
				print("Error: la linea es incorrecta")
	except Exception as e:
		cadena="Error de lectura "+str(e)
		print(cadena)
	finally:
		pass

def setter(a, m):
	"Escribe los datos en el dispositivo por SNMP"
	# respuesta=str(getattr(m, a[0]))
	# print("Valor Anterior de ", a[0], respuesta)
	setattr(m, a[0], a[1])
	return 0 # no errores

def checker(a, m):
	"Comprueba los datos en el dispositivo por SNMP"
	estado=0 # no errores
	# print("Valor buscado", a[0], "=", a[1])
	respuesta=str(getattr(m, a[0]))
	print(respuesta)
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
		m=M(ip, community="public", version=1)
		# Solo comprobar
		if (check):
			lector(m, checker)
		# Asignar y comprobar
		else:
			lector(m, setter)
			lector(m, checker)
		informacion="Fin Iteracion"
	else:
		informacion="Error "+servidor+" no es una ip"
	return informacion

########################
# Funciones auxiliares #
########################
def funcionConsola():
	informacion="Verificar que hay un nuevo dispositivo, pulsa Enter"
	global servidor
	if versionPy<(3, 0):	# Python2
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
	# Carga las mibs
	load("mibs/RFC1155-SMI.mib")
	load("mibs/RFC-1212.mib")
	load("mibs/rfc1213.mib")
	bucleactivo= False
	# TODO: Carga las mibs
	# Bucle principal Idle
	while (True): # Solo para las interfaces de consola
		cadena=funcionConsola()
		print(cadena)



