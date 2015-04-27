#!/usr/bin/python
import sys	# Para los argumentos
import re	# Para CheckeaServidor
###################
# Biblioteca HNMP #
###################
# http://pysnmp.sourceforge.net/
# http://pysnmp.sourceforge.net/examples/current/v3arch/oneliner/manager/cmdgen/get-v2c.html
# http://pysnmp.sourceforge.net/examples/current/v3arch/oneliner/manager/cmdgen/set-v2c-with-value-type-mib-lookup.html
from pysnmp.entity.rfc3413.oneliner import cmdgen

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
def lector(funcion):
	"Lee el archivo linea a linea y escribe los datos en el dispositivo"
	try:
		f=open(archivo, 'r')
		for line in f:
			a=line.split()
			if (len(a)>=2):
				if(a[0][0]=="#"):
					# print("Error: la linea es un comentario")
					pass
				else:
					funcion(a)
			else:
				# print("Error: la linea es incorrecta")
				pass
	except Exception as e:
		print("Error", e)
	finally:
		pass

def setter(a):
	"Escribe los datos en el dispositivo por SNMP"
	# TODO: setOID
	print("Valor Anterior de", a[0], "TODO: get", a[0])
	print("TODO: set", a[0], a[1])

def checker(a):
	"Comprueba los datos en el dispositivo por SNMP"
	# TODO: getOID
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
		# TODO: Conexion con el servidor
		print ("Conexion con el servidor")

		lineas=cuentaLineas(archivo)
		print(lineas, "lineas")
		# Solo comprobar
		if (check):
			lector(checker)
		# Asignar y comprobar
		else:
			lector(setter)
			lector(checker)
		# TODO: Fin->Bucle Idle
		print("Fin")

