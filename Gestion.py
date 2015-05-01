#!/usr/bin/python
from __future__ import print_function # Python 2 Para print (1, 2) Debe estar al inicio
import sys	# Para los argumentos
import re	# Para checkeaServidor

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
iteracion=0 # Lleva la cuenta de las maquinas

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
def lector(funcion):
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
					# print("Error: la linea es un comentario")
					pass
				else:
					if (not funcion(a)):
						cadena=a[0]+" "+a[1]+" CORRECTO"
						print(cadena)
					else:
						cadena=a[0]+" "+a[1]+" ERROR"
						print(cadena)
			else:
				# print("Error: la linea es incorrecta")
				pass
	except Exception as e:
		cadena="Error de lectura "+str(e)
		print(cadena)
	finally:
		pass

def setter(a):
	"Escribe los datos en el dispositivo por SNMP"
	# TODO: setOID
	return 0 # no errores

def checker(a):
	"Comprueba los datos en el dispositivo por SNMP"
	estado=0 # no errores
	# TODO: getOID
	return estado

def funcionPrincipal():
	"La funcion que realiza el trabajo, checkeaServidor()->lector()->setter()/checker()"
	global iteracion
	global servidor
	iteracion=iteracion+1
	cadena="Ejecutado: "+str(iteracion)
	print (cadena)
	if (checkeaServidor(servidor)):
		# TODO: Conexion con el servidor
		# Solo comprobar
		if (check):
			cadena="Comprobacion:"
			print (cadena)
			lector(checker)
		# Asignar y comprobar
		else:
			cadena="Configuracion:"
			print (cadena)
			lector(setter)
			cadena="Comprobacion:"
			print (cadena)
			lector(checker)
		informacion="Fin Iteracion"
	else:
		informacion="Error "+servidor+" no es una ip"
	return informacion

########################
# Funciones auxiliares #
########################
def funcionConsola():
	informacion="Conectar un nuevo dispositivo y pulsa Enter para configurarlo"
	global servidor
	if versionPy<(3, 0):	# Python2
		raw_input(informacion)
	else:
		input(informacion)
	return funcionPrincipal()

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
	# TODO: Carga las mibs
	# Bucle principal Idle
	while (True): # Solo para las interfaces de consola
		cadena=funcionConsola()
		print(cadena)



