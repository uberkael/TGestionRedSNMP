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

######
# Tk #
######
if versionPy < (3, 0):
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
def lector(funcion, prd, texto):
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
			if (prd):
				prd['value']=bprogreso
			a=line.split()
			if (len(a)>=2):
				if(a[0][0]=="#"):
					# print("Error: la linea es un comentario")
					pass
				else:
					if (not funcion(a)):
						cadena=a[0]+" "+a[1]+" CORRECTO"
						print(cadena)
						if(texto):
							texto.insert("end", cadena+"\n")
					else:
						cadena=a[0]+" "+a[1]+" ERROR"
						print(cadena)
						if(texto):
							texto.insert("end", cadena+"\n", "error")
			else:
				# print("Error: la linea es incorrecta")
				pass
	except Exception as e:
		cadena="Error de lectura "+str(e)
		print(cadena)
		if(texto):
			texto.insert("end", cadena+"\n", "error")
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

def funcionPrincipal(servidorGUI=False, checkGUI=False, prd=False, texto=False):
	"La funcion que realiza el trabajo, checkeaServidor()->lector()->setter()/checker()"
	global iteracion
	global servidor
	global check
	# Aumenta el numero de ejecuciones
	iteracion=iteracion+1
	cadena="Ejecutado: "+str(iteracion)
	print (cadena)
	if(texto):
		texto.insert("end", cadena+"\n", "importante")
	# Si hay variables del GUI, sobreescriben a las globales
	if(servidorGUI):
		servidor=servidorGUI
	# truco con valor trinario
	if(checkGUI==1):
		check=False
	elif (checkGUI==2):
		check=True
	# Trabajo
	if (checkeaServidor(servidor)):
		# TODO: Conexion con el servidor
		# Solo comprobar
		if (check):
			cadena="Comprobacion:"
			print (cadena)
			lector(checker, prd, texto)
		# Asignar y comprobar
		else:
			cadena="Configuracion:"
			print (cadena)
			lector(setter, prd, texto)
			cadena="Comprobacion:"
			print (cadena)
			lector(checker, prd, texto)
		informacion="Fin Iteracion"
	else:
		informacion="Error "+servidor+" no es una ip"
	return informacion

#######
# GUI #
#######
def GUITk():
	"Todo el entorno grafico del programa programado en Tk"
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
	menu_file.add_command(label='Open file...', command=selecionaArchivo)
	menu_file.add_separator() # ver abajo separador
	menu_file.add_command(label='Close to terminal', command=root.destroy)
	menu_file.add_command(label='Close', command=exit)

	# checkbutton
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
	prd.configure(value=100) # pone la barra a un valor
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
	## Boton ##
	boton=ttk.Button(flame, text="Configura", width=60, command=lambda: trabajaIdle(servidorGUI.get(), checkGUI.get(), prd, texto) ) # Crea un boton
	## Detalles Tk ##
	# Agrega a la ventana
	abel.grid()		# Agrega una etiqueta de texto
	campo.grid()	# Agrega campo de servidor
	boton.grid()	# Agrega boton
	prd.grid()		# Agrega barra de progreso
	texto.grid()	# Agrega consola de errores
	flame.grid()	# Agrega el frame
	# Agrega la tecla intro como le diera al boton
	root.bind('<Return>', lambda event: print (bool(checkGUI.get())) )
	# Comienza el dibujo
	root.mainloop() # Al final

#####################
# Funciones del GUI #
#####################
def selecionaArchivo():
	"Dialogo para seleccionar un archivo, File, New"
	global archivo # Accede a la variable global para cambiar el valor
	filename=filedialog.askopenfilename(filetypes=[('Archivos de Configuracion', '*.ini'), ('All Files', '*')])
	archivo=filename

def borraConsola(texto):
	"Borra el buffer de la consola"
	texto.delete("1.0", "end")
	pass

def trabajaIdle(servidorGUI, checkGUI, prd, texto):
	print(checkGUI)
	"La funcion que realiza el trabajo en el modo grafico"
	borraConsola(texto) # Borra el texto
	prd.stop() # Para la animacion de la barra de progreso
	prd['mode']='determinate'
	prd['value']=0 # Pone la barra de progreso a 0
	cadena=funcionPrincipal(servidorGUI, checkGUI, prd, texto)
	texto.insert("end", cadena+"\n", "importante")

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
	GUITk()
	# Bucle principal Idle
	while (True): # Solo para las interfaces de consola
		cadena=funcionConsola()
		print(cadena)



