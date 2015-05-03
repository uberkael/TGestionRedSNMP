#!/usr/bin/python
from __future__ import print_function # Python 2 Para print (1, 2) Debe estar al inicio
import sys	# Para los argumentos
<<<<<<< HEAD
import re	# Para checkeaServidor
import os
=======
import re	# Para CheckeaServidor
###################
# Biblioteca HNMP #
###################
# http://pysnmp.sourceforge.net/
# http://pysnmp.sourceforge.net/examples/current/v3arch/oneliner/manager/cmdgen/get-v2c.html
# http://pysnmp.sourceforge.net/examples/current/v3arch/oneliner/manager/cmdgen/set-v2c-with-value-type-mib-lookup.html
from pysnmp.entity.rfc3413.oneliner import cmdgen
>>>>>>> pysnmp

###########################
# Ejecucion en raspberry pi
###########################
if (os.uname()[1] == "raspberrypi"):
	raspberrypi = True
if (raspberrypi):
	import RPi.GPIO as gpio
	import LircUnixSocketRead as lirc
	gpio.setmode(gpio.BCM)
	pinesprogreso = [4,17,27,22,5]
	pinmenu = 18
	pincheck = 23
	pinerror = 24
	gpio.setwarnings(False)
	gpio.setup(pinesprogreso,gpio.OUT,initial=False)
	gpio.setup(pinmenu,gpio.OUT,initial=False)
	gpio.setup(pincheck,gpio.OUT,initial=False)
	gpio.setup(pinerror,gpio.OUT,initial=False)
	lirc.iniciaSocket()
	KEY_ENTER = "KEY_OK"
	KEY_MENU = "KEY_WINDOWS"
	KEY_CHECK = "KEY_INFO"
	KEY_CHANGESERVERIP = "KEY_BACK"
	KEYS_NUMERIC_DOT = {"KEY_1":"1","KEY_2":"2","KEY_3":"3","KEY_4":"4", \
						"KEY_5":"5","KEY_6":"6","KEY_7":"7", \
						"KEY_8":"8","KEY_9":"9","KEY_0":"0","KEY_*":"."}
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
		barraLedReset()
		lineas=cuentaLineas(archivo)
		porcentaje=100.0/lineas
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
			barraLedActualiza(bprogreso)	
			a=line.split()
			if (len(a)==2):
				if(a[0][0]=="#"):
					print("Error: la linea es un comentario")
					pass
				else:
					if (not funcion(a)):
						cadena=a[0]+" "+a[1]+" CORRECTO"
						print(cadena)
					else:
						cadena=a[0]+" "+a[1]+" ERROR"
						print(cadena)
			elif ((len(a)==3) and (a[2]=="nocheck")): 
				#Contempla el caso en el que existe un identificador de no chequeo de ese oid en concreto
				#Para evitar problemas con las tablas creadas dinamicamente por el usuario mediante la modificacion
				#de la columna Status (por ejemplo en RMON), donde al establecer a CreateRequest, posteriormente cambiaria a 
				#underCreation por lo que provocaria un fallo al hacer el check
				if(a[0][0]=="#"):
					print("Error: la linea es un comentario")
				elif (funcion == setter):
					if (not funcion(a)):
						cadena=a[0]+" "+a[1]+" CORRECTO"
						print(cadena)
					else:
						cadena=a[0]+" "+a[1]+" ERROR"
						print(cadena)	
			else :	
				print("Error: la linea es incorrecta")
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
<<<<<<< HEAD
=======
	print("Valor buscado", a[0], "=", a[1])
	# if (a[1]==" get a[0] "):
	# print("Correcto")
	cmdGen = cmdgen.CommandGenerator()
	errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		cmdgen.CommunityData('public'),
		cmdgen.UdpTransportTarget((servidor, 161)),
		# '1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.6.0' TODO: Cambiar el bucle y ejecutar al final con toda la lista
		a[0]
		)
	# Check for errors and print out results
	if errorIndication:
		print(errorIndication)
		estado=1 # errores
	else:
		if errorStatus:
			print('%s at %s' % (
				errorStatus.prettyPrint(),
				errorIndex and varBinds[int(errorIndex)-1] or '?'
				)
			)
			estado=1 # errores
		else:
			for name, val in varBinds:
				print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
				print("Valor buscado", a[0], "=", a[1])
				if (a[1]==val.prettyPrint()):
					print("Correcto")
				else:
					print("Error: GET ha devuelto otra cosa")
					estado=1 # errores

>>>>>>> pysnmp
	return estado

def funcionPrincipal():
	"La funcion que realiza el trabajo, checkeaServidor()->lector()->setter()/checker()"
	global iteracion
	global servidor
	global check
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
# def funcionConsola():
# 	informacion="Conectar un nuevo dispositivo y pulsa Enter para configurarlo"
# 	global servidor
# 	if versionPy<(3, 0):	# Python2
# 		raw_input(informacion)
# 	else:
# 		input(informacion)
# 	return funcionPrincipal()
def funcionConsola():
	codigoIR = lirc.nuevoCodigo()
	if (codigoIR== KEY_ENTER):
		funcionPrincipal()
	elif (codigoIR == KEY_MENU):
		funcionMenu()
	return "Esperando"
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

###############################
# Funciones para raspberry pi #
###############################
def barraLedActualiza(progreso):
	indice = progreso / 20
	if(indice < 4.9): 
		indice = int(indice)
	else:
		indice = 5
	if(indice>0):
		gpio.output(pinesprogreso[0:indice],True)

def barraLedReset():
	gpio.output(pinesprogreso,False)

def funcionMenu():
	global check
	gpio.output(pinmenu,True)
	codigoIR = lirc.nuevoCodigo()
	if (codigoIR == KEY_CHECK):
		check = not check
	elif (codigoIR == KEY_CHANGESERVERIP):
		funcionCambiarIP()
	gpio.output(pinmenu,False)

def funcionCambiarIP():
	print("cambiando IP")
	nuevaIP = ""
	ipcorrecta = True
	codigoIR = lirc.nuevoCodigo()
	while( codigoIR in KEYS_NUMERIC_DOT):
		nuevaIP = nuevaIP+KEYS_NUMERIC_DOT[codigoIR]
		codigoIR = lirc.nuevoCodigo()
	ipcorrecta = checkeaServidor(nuevaIP)
	if(ipcorrecta == True):
		servidor = nuevaIP
		print(servidor)
	print("Ip cambiada")
###################################
# Comienza el programa principal #
###################################
if __name__=="__main__":
	# TODO: Carga las mibs
	# Bucle principal Idle
	while (True): # Solo para las interfaces de consola
		cadena=funcionConsola()
		print(cadena)



