import socket

#Identificador del objeto socket
client = None
cierre = False
#Crea el socket y lo conecta a /var/run/lirc/lircd
def iniciaSocket():
	global client
	if (client == None):
		client = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
		client.setblocking(0)
 		client.connect("/var/run/lirc/lircd")

def cierraSocket():
	global client
	if (client != None):
		cierre = True
		client.close()
		client = None

#Recibe una linea del socket, la divide en los cuatro campos que
#la forman y devuelve los dos campos intermedios
def recibirLinea():
	global client
	global cierre
	linea = ""
	numrepeticion = "" 
	boton = ""
	while(cierre==False and (linea == "")or (linea == None) and client):
		try:
			linea = client.recv(1024)
			if(linea != ""):
				lineasplit = linea.split()
				numrepeticion = lineasplit[1]
				boton = lineasplit[2]
		except socket.error, e:
			pass
		except Exception as e:
			cierre = True
	return [numrepeticion, boton]

#Emplea la funcion recibirLinea para leer los botones pulsados
#pero ignora aquellos que han sido pulsados repetidamente en un
#corto espacio de tiempo (evita asi la captura de dobles pulsaciones no intencionadas
#provocadas por la velocidad de repeticion del mando)
def nuevoCodigo() :	
	repetido = True
	while (repetido == True):
		numrepeticion, boton = recibirLinea()
		if( (numrepeticion == "00")or(numrepeticion == "")):
			 repetido = False

	return boton


