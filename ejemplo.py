#!/usr/local/bin/jython
# -*- coding: utf-8 -*-


sites=[]
filename=''
f=open("URLs.txt", "r")
filename = f.readline()
filename = filename.replace(".txt", '')
filename = filename.replace("/home/elisamerida/Escritorio/Interfaz/",'')
linea = f.readline()
while linea != "":
	linea = linea.split("\t")[0]
	print(linea)
	sites.append(linea)
	linea = f.readline()
f.close()	
	
