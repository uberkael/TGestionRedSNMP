#!/usr/bin/python
from __future__ import print_function # Python 2 Para print (1, 2) Debe estar al inicio
import sys	# Para los argumentos
import re	# Para checkeaServidor
import os	# Para averiguar el entorno
import signal

###################
# Biblioteca HNMP #
###################
# https://github.com/trehn/hnmp
from hnmp import SNMP

raspberrypi = False
###########################
# Ejecucion en raspberry pi
###########################
if (os.uname()[1] == "raspberrypi"):
	raspberrypi = True
	import RPi.GPIO as gpio
	import LircUnixSocketRead as lirc
	import threading
	gpio.setmode(gpio.BCM)
	pinesprogreso = [4,17,27,22,5]
	pinmenu = 18
	#pincheck = 23
	pinerror = 12
	gpio.setwarnings(False)
	gpio.setup(pinesprogreso,gpio.OUT,initial=False)
	gpio.setup(pinmenu,gpio.OUT,initial=False)
	#gpio.setup(pincheck,gpio.OUT,initial=False)
	gpio.setup(pinerror,gpio.OUT,initial=False)
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

######
# Tk #
######
if versionPy<(3, 0):
	from Tkinter import *				# Importa todos los objetos
	import ttk							# Importa los themes de Tk
	import tkFileDialog as filedialog 	# Importa los dialogos y selector
	import tkFont as font				# Importa fuentes para la consola de errores
else:
	from tkinter import *				# Importa todos los objetos
	from tkinter import ttk				# Importa los themes de Tk
	from tkinter import filedialog		# Importa los dialogos y selector
	from tkinter import font			# Importa fuentes para la consola de errores

######################
# Variables globales #
######################
servidorGUI = False #Variable de la entrada de texto del GUI
checkGUI = False #Variable del toggle button del GUI
ejecutando = False #Variable para evitar ejecucion simultanea de dos funciones principales
prd = False #Barra de progreso del modo grafico
texto = False #Caja de texto del modo grafico
servidor="10.10.10.2"
archivo='configuracion.ini'
check=False # check, solo comprueba
iteracion=0 # Lleva la cuenta de las maquinas
modoGrafico=("DISPLAY" in os.environ) or ("nt" in os.name) # Por si se ejecuta en modo consola

###################################
# Argumentos en linea de comandos #
###################################
tamArgs=len(sys.argv)
if (tamArgs==2):
	if ("check" in sys.argv[-1].lower()):
		check=True
	else:
		servidor=sys.argv[1]
# Si hay tres argumentos es el servidor y un archivo
if (tamArgs==3):
	servidor=sys.argv[1]
	if ("check" in sys.argv[-1].lower()):
		check=True
	else:
		archivo=sys.argv[2]
# Si hay mas de tres argumentos es el servidor y un archivo y check
if (tamArgs>3):
	servidor=sys.argv[1]
	archivo=sys.argv[2]
	if ("check" in sys.argv[3].lower()):
		check=True
	else: # Si el tercero no es check algo esta mal
		print("Uso:", sys.argv[0], "<servidor> <archivo> [<check>]")
		quit()

###########################
# Definicion de funciones #
###########################
def lector(snmp, funcion, prd, texto):
	"Lee el archivo linea a linea y llama a checker() o setter() en cada una"
	try:
		# Lineas y para barra de progreso
		if(raspberrypi):
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
			if (raspberrypi):
				barraLedActualiza(bprogreso)	
			if (prd):
				prd['value']=bprogreso # Nuevo valor de progreso
				prd.update_idletasks() # Actualiza la barra
			a=line.split()
			if (len(a)>=2):
				if(a[0][0]=="#"):
					# print("Error: la linea es un comentario")
					pass
				else:
					resultado =funcion(snmp,a)
					if (resultado == 0):
						cadena=a[0]+" "+a[1]+" CORRECTO"
						print(cadena)
						if(texto):
							texto.insert("end", cadena+"\n")
							texto.see("end") # Se asegura de ir al final
					elif(resultado == 1):
						cadena=a[0]+" "+a[1]+" ERROR"
						if(raspberrypi):
							gpio.output(pinerror,True)
						print(cadena)
						if(texto):
							texto.insert("end", cadena+"\n", "error")
							texto.see("end") # Se asegura de ir al final
						if(prd): # Barra de color no compatible con estilos del sistema
							prd['style']="red.Horizontal.TProgressbar"
						break # Sale del bucle
					elif(resultado == 2):
						pass #Considera el caso en el que la linea incluye un nocheck y por lo tanto no se comprueba
			else:
				# print("Error: la linea es incorrecta")
				pass
	except Exception as e:
		cadena="Error de lectura "+str(e)
		print(cadena)
		if(raspberrypi):
			gpio.output(pinerror,True)
		if(texto):
			texto.insert("end", cadena+"\n", "error")
			texto.see("end") # Se asegura de ir al final
		if(prd):
			prd['style']="red.Horizontal.TProgressbar"
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
	if ("nocheck" in a[-1]):
		# No chequea la tabla
		estado = 2 #Indica al lector que la fila no se ha checkeado
	else:
		# print("Valor buscado", a[0], "=", a[1])
		respuesta=str(snmp.get(a[0]))
		# print(respuesta)
		if (a[1]==respuesta):
			# print("Correcto")
			pass # sin errores
		else:
			# print("Error: GET ha devuelto otra cosa")
			estado=1 # errores
		pass
	return estado

def funcionPrincipal():
	"La funcion que realiza el trabajo, checkeaServidor()->lector()->setter()/checker()"
	global servidorGUI
	global checkGUI
	global prd
	global texto
	global iteracion
	global servidor
	global check
	global ejecutando #Variable para evitar ejecucion simultanea de la funcion principal
	#al poder ser lanzada mediante la consola o el entorno grafico, o mediante los infrarrojos
	# Aumenta el numero de ejecuciones
	informacion = "Fin iteracion"
	if(ejecutando == False):
		ejecutando = True # Para evitar dobles ejecuciones
		iteracion=iteracion+1
		cadena="Ejecutado: "+str(iteracion)
		print (cadena)
		if(texto):
			texto.insert("end", cadena+"\n", "importante")
			texto.see("end") # Se asegura de ir al final
		# Si hay variables del GUI, sobreescriben a las globales
		if(servidorGUI):
			servidor=servidorGUI.get()
		if(checkGUI):
			# truco con valor trinario
			if(checkGUI.get()==1):
				check=False
			elif (checkGUI.get()==2):
				check=True
		if(raspberrypi):
			pinErrorReset()		
		# Trabajo
		if (checkeaServidor(servidor)):
			# Conexion con el servidor
			snmp=SNMP(servidor, community="public")  # v2c
			# Solo comprobar
			if (check):
				cadena="Comprobacion:"
				print (cadena)
				if(texto):
					texto.insert("end", cadena+"\n", "importante")
					texto.see("end") # Se asegura de ir al final
				lector(snmp, checker, prd, texto)
			# Asignar y comprobar
			else:
				cadena="Configuracion:"
				print (cadena)
				if(texto):
					texto.insert("end", cadena+"\n", "importante")
					texto.see("end") # Se asegura de ir al final
				lector(snmp, setter, prd, texto)
				cadena="Comprobacion:"
				print (cadena)
				if(texto):
					texto.insert("end", cadena+"\n", "importante")
					texto.see("end") # Se asegura de ir al final
				lector(snmp, checker, prd, texto)
			informacion="Fin Iteracion"
		else:
			informacion="Error "+servidor+" no es una ip"
		ejecutando = False #Permite una nueva ejecucion
	return informacion

#######
# GUI #
#######
def GUITk():
	"Todo el entorno grafico programado en Tk"
	global servidor # Accede a la variable global para cambiar el valor
	global checkGUI
	global servidorGUI
	global prd
	global texto
	root=Tk()
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
	# Abrir archivo
	menu_file.add_command(label='Open file...', command=selecionaArchivo)
	menu_file.add_separator() # ver abajo separador
	menu_file.add_command(label='Close to terminal', command=root.destroy)
	menu_file.add_command(label='Close', command=lambda: exitGUI(root))
	## checkbutton ##
	checkGUI=IntVar()
	checkGUI.set(check+1) # Truco valor trinario
	menu_edit.add_checkbutton(label='Solo Check', variable=checkGUI, onvalue=2, offvalue=1)
	## Campo del servidor ##
	abel=ttk.Label(flame, text='Servidor:')
	servidorGUI=StringVar() # La variable en Tk tiene que ser un StringVar
	servidorGUI.set(servidor) # Sustituye la variable original servidor
	campo=ttk.Entry(flame, textvariable=servidorGUI, width=14)
	## Barra de progreso ##
	prd=ttk.Progressbar(flame, orient=HORIZONTAL, length=368, mode='determinate')
	prd.configure('maximum') # muestra el valor maximo (defecto 100)
	prd.configure(value=1) # pone la barra a un valor
	prd['mode']='indeterminate'
	prd.start(15)
	## Consola de errores ##
	# una fuente de windows
	grombenawer=font.Font(family='Consolas', size=14, weight='bold') # 	from tkinter import font
	texto=Text(flame, wrap="word", background="black", foreground="green", font=grombenawer, selectbackground="black", selectforeground="green", undo=True)
	texto.tag_config("error", foreground="red")
	texto.tag_config("importante", foreground="yellow")
	informacion="Verificar que hay un nuevo dispositivo, pulsa intro"
	texto.insert("end", informacion+"\n") # Consola al inicio
	texto.see("end") # Se asegura de ir al final
	## Boton ##
	boton=ttk.Button(flame, text="Configura", width=60, command=lambda: trabajaIdle(servidorGUI.get(), checkGUI.get(), prd, texto) )
	## Scrollbar ##
	sbv=ttk.Scrollbar(flame, orient=VERTICAL, command=texto.yview)
	texto['yscrollcommand']=sbv.set
	## Estilo para la barra de color rojo, error
	s=ttk.Style()
	# s.theme_use('clam') # Barra de color no compatible con estilos del sistema
	s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
	## Detalles Tk ##
	# Agrega a la ventana
	abel.grid(column=0, row=0)	# Agrega una etiqueta de texto
	campo.grid(column=0, row=1)	# Agrega campo de servidor
	boton.grid(column=0, row=2)	# Agrega boton
	prd.grid(column=0, row=3)	# Agrega barra de progreso
	texto.grid(column=0, row=4)	# Agrega consola de errores
	sbv.grid(column=1, row=4, sticky=(N, S))
	flame.grid()	# Agrega el frame
	# Agrega la tecla intro como le diera al boton
	root.bind('<Return>', lambda event: trabajaIdle(servidorGUI.get(), checkGUI.get(), prd, texto) )
	# Comienza el dibujo
	root.mainloop() # Al final

#####################
# Funciones del GUI #
#####################
def selecionaArchivo():
	"Dialogo para seleccionar un archivo, File, New"
	global archivo # Accede a la variable global para cambiar el valor
	filename=filedialog.askopenfilename(initialfile="configuracion.ini", filetypes=[('Archivos de Configuracion', '*.ini'), ('All Files', '*')])
	if(filename):
		archivo=filename

def borraConsola(texto):
	"Borra el buffer de la consola"
	texto.delete("1.0", "end")
	pass

def trabajaIdle(servidorGUI, checkGUI, prd, texto):
	"La funcion que realiza el trabajo en el modo grafico"
	borraConsola(texto) # Borra el texto
	prd.stop() # Para la animacion de la barra de progreso
	prd['style']=""
	prd['mode']='determinate'
	prd['value']=0 # Pone la barra de progreso a 0
	prd.update_idletasks() # Actualiza la barra
	cadena=funcionPrincipal()
	texto.insert("end", cadena+"\n", "importante")
	texto.see("end") # Se asegura de ir al final

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
	informacion="Conecta un nuevo dispositivo y pulsa <Enter> para configurarlo\n"
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

def pinErrorReset():
	gpio.output(pinerror,False)	

def funcionMenu():
	global check
	global checkGUI
	print("MENU")
	gpio.output(pinmenu,True)
	codigoIR = lirc.nuevoCodigo()
	if (codigoIR == KEY_CHECK):
		check = not check
		if(check):
			print("Solo check")
		else:
			print("Configuracion y check")
		if (checkGUI):
			checkGUI.set(check+1)
	elif (codigoIR == KEY_CHANGESERVERIP):
		funcionCambiarIP()
	gpio.output(pinmenu,False)

def funcionCambiarIP():
	global servidor
	global servidorGUI
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
		if (servidorGUI):
			servidorGUI.set(nuevaIP)
		print("Nueva IP: "+servidor)

def funcionGestionInfrarrojos():
	global servidor
	global checkGUI
	global prd
	global texto
	fin = False
	while(not fin):
		codigoIR = lirc.nuevoCodigo()
		print(codigoIR)
		if (codigoIR== KEY_ENTER):
			if(texto):
				borraConsola(texto) # Borra el texto
				prd.stop() # Para la animacion de la barra de progreso
				prd['style']=""
				prd['mode']='determinate'
				prd['value']=0 # Pone la barra de progreso a 0
				prd.update_idletasks() # Actualiza la barra
			cadena=funcionPrincipal()
			print(cadena)
			if(texto):
				texto.insert("end", cadena+"\n", "importante")
				texto.see("end") # Se asegura de ir al final
		elif (codigoIR == KEY_MENU):
			funcionMenu()
		elif (codigoIR == ""):
			fin = True

#funcionCierreParaGUI
def exitGUI(root):			
	root.destroy()
	signal_handler(None,None)

#Manejador de signal para detectar ctrl-C
def signal_handler(signal, frame):
	global raspberrypi
	#Restaurar los valores predeterminados
	if(raspberrypi == True):
		lirc.cierraSocket()
		gpio.cleanup()
	#Salir del programa
	sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)
###################################
# Comienza el programa principal #
###################################
if __name__=="__main__":
	# TODO: Carga las mibs
	if(raspberrypi):
		lirc.iniciaSocket()
		t = threading.Thread(target = funcionGestionInfrarrojos)
		t.start()
	if (modoGrafico): # Si esta en modo grafico carga Tk
		GUITk()
	servidorGUI=False
	checkGUI=False
	prd = False
	texto = False
	# Bucle principal Idle
	while (True): # Solo para las interfaces de consola
		cadena=funcionConsola()
		print(cadena)
