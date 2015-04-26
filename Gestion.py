#!/usr/bin/python
import sys
from tkinter import *			# Importa todos los objetos
from tkinter import ttk			# Importa los themes de Tk
from tkinter import filedialog	# Importa los dialogos y selector

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
			if (len(a)==2):
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
	print("TODO: get", a[0], "y comprobacion")
	# if (a[1]==" get a[0] "):
		# print("Correcto")

#######
# GUI #
#######
def GUITk():
	global servidor # Accede a la variable global para cambiar el valor
	root = Tk()
	root.title("Configurador")
	## Contenedor ##
	flame=ttk.Frame(root, borderwidth=5, relief="sunken", width=600) # Crea un frame
	# "flat", "raised", "sunken", "solid", "ridge", or "groove".
	# flame.configure(width=600) # Ancho del frame (Se suele ajustar automaticamente)
	# flame.configure(height=400) # Alto del frame (Se suele ajustar automaticamente)
	## Creacion de un menu ##
	root.option_add('*tearOff', FALSE) # Evita que los menus sean solo una linea sin nada
	menubar=Menu(root)
	root['menu']=menubar
	# Agregando menus
	menu_file=Menu(menubar)
	menu_edit=Menu(menubar)
	menubar.add_cascade(menu=menu_file, label='File')
	menubar.add_cascade(menu=menu_edit, label='Edit')
	# TODO: Abrir archivo
	menu_file.add_command(label='Open file...', command=SelecionaArchivo)
	menu_file.add_separator() # ver abajo separador
	menu_file.add_command(label='Close', command=root.quit)
	## Campo del servidor ##
	abel=ttk.Label(flame, text='Servidor:')
	aux=servidor
	servidor=StringVar() # La variable en Tk tiene que ser un StringVar
	servidor.set(aux) # Sustituye la variable original servidor
	campo=ttk.Entry(flame, textvariable=servidor, width=14)
	campo.get() # Muestra el valor de la variable usada
	## Barra de progreso ##
	prd=ttk.Progressbar(flame, orient=HORIZONTAL, length=368, mode='determinate')
	prd.configure('maximum') # muestra el valor maximo (defecto 100)
	prd.configure(value=10) # pone la barra a un valor
	## Boton ##
	boton=ttk.Button(flame, text="Boton", width=60, command=lambda: TrabajaIdle(prd) ) # Crea un boton
	## TODO: Consola de errores ##
	## Detalles Tk ##
	# Agrega a la ventana
	abel.grid()		# Agrega una etiqueta de texto
	campo.grid()	# Agrega el campo de escribir
	boton.grid()	# Agrega el boton
	prd.grid()
	flame.grid()	# Agrega el frame
	# Comienza el dibujo
	root.mainloop() # Al final

########################
# Funciones auxiliares #
########################
def SelecionaArchivo():
	global archivo # Accede a la variable global para cambiar el valor
	filename=filedialog.askopenfilename(filetypes=[('Archivos de Configuracion', '*.ini'), ('All Files', '*')])
	archivo=filename

def TrabajaIdle(bprogreso):
	# TODO: Esto activa el estado de espera y configuracion continua
	print("TODO: Esto activa el estado de espera y configuracion continua")
	# Comprueba los datos introducidos
	print("TODO: Esto activa el estado de espera y configuracion continua")
	print("Lee el archivo:", archivo)
	print("conecta con el servidor:", servidor.get())
	# TODO: Cambia la barra segun el archivo
	if(bprogreso['value']>90):
		bprogreso['value']=0
	else:
		bprogreso['value']=bprogreso['value']+10
	CheckeaServidor(servidor.get())

def CheckeaServidor(servidor):
	import re
	regexip="^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
	if re.match(regexip, servidor):
		print("Servidor correcto")
		return 1
	else:
		print ("Error ", servidor, " no es una ip")
		return 0

###################################
# Comienza el programa principal #
###################################
if __name__=="__main__":
	GUITk()
	if CheckeaServidor(servidor.get()):
		print(archivo)
		# TODO: Carga las mibs
		print ("Carga las mibs")
		# TODO: Conexion con el servidor
		print ("Conexion con el servidor")

		# Solo comprobar
		if (check):
			lector(checker)
		# Asignar y comprobar
		else:
			lector(setter)
			lector(checker)
		# TODO: Fin->Bucle Idle
		print("Fin")

