#!/usr/bin/python
import sys
from snimpy.manager import Manager as M
from snimpy.manager import load

def setter(m):
	f = open(archivo, 'r')
	for line in f:
		a=line.split()
		if (a):
			#print(a)
			print("Valor Anterior de ", a[0], getattr(m, a[0], a[1]))
			setattr(m, a[0], a[1])

def checker(m):
	f = open(archivo, 'r')
	for line in f:
		a=line.split()
		if (a):
			print("Valor buscado",a[0] ," = ", a[1])
			if (a[1]==getattr(m, a[0])):
				print("Correcto")

ip="10.10.10.2"
archivo='configuracion.ini'
check=False

if (len(sys.argv)>1):
	for x in sys.argv:
		if ("check" in x.islower()):
		check=True

if (len(sys.argv)==2):
	ip=sys.argv[1]

if (len(sys.argv)>3):
	ip=sys.argv[1]
	archivo=sys.argv[2]

#load("SNMPv2-SMI.my")
#load(" SNMPv2-TC.my")
load("mibs/RFC1155-SMI.mib")
load("mibs/RFC-1212.mib")
load("mibs/rfc1213.mib")
#load("ejemplo.mib")
m = M(ip, community="public", version=1)
#print(m.sysUpTime)
#print(m.sysContact)
#m.sysContact = "Georg"
#print(getattr(m, "sysContact"))
#setattr(m, "sysContact", "Admin")
#print(getattr(m, "sysContact"))

if (check):
	checker(m)
else
	setter(m)
	checker(m)


