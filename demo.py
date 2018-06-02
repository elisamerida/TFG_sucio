from __future__ import absolute_import
from automation import TaskManager, CommandSequence
from six.moves import range

#Lectura del fichero
sites=[]
filename=''
f=open("URLs.txt", "r")

filename = f.readline()
filename = filename.replace(".txt", '')
filename = filename.replace("/home/elisamerida/Escritorio/Interfaz/",'')
linea = f.readline()
while linea != "":
	linea = linea.split("\t")[0]
	sites.append(linea)
	linea = f.readline()
f.close()

#Numero de navegadores que se van a utilizar
NUM_BROWSERS = 1

#Carga la configuracion del TaskManager y del navegador
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)
#Instanciamos la plataforma 
filename= filename.replace("\n", '')
#print('rastreo'+ filename + '.sqlite')
manager_params['database_name'] = 'rastreo'+ filename + '.sqlite'

manager = TaskManager.TaskManager(manager_params, browser_params)

#Se visitan los sitios del fichero
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)
    command_sequence.get(sleep=0, timeout=60)
    command_sequence.dump_profile_cookies(120)
    manager.execute_command_sequence(command_sequence, index='**')
#Cierra el navegador y espera a que los datos se terminen de cargar
manager.close()
