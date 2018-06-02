#Este modulo se utilizara para extraer los identificadores
#persistentes de las cookies usando un metodo de dos rastreos
import census_util
from collections import defaultdict
import sqlite3 as lite


#FUNCION AUXILIAR PARA EXTRAER IDS PERSISTENTES DE BBDD
#intenta separar la cadena de texto que es el valor de una cookie
#en pares parametro-valor y los anade a un diccionario
#se basa en delimitadores conocidos
def add_inner_cookie_parameters(cookie_dict, domain, name, value):
	#Delimitadores comunes dentro de las cookies
	delimiters = [":", "&"]

	for delimiter in delimiters:
		parts = value.split(delimiter)

		for part in parts:
			params= part.split("=")

			if (len(params) == 2 and params[0] != '' and params[1] != ''):
				cookie_dict[(domain, name + "#" + params[0])].append(params[1])


#FUNCION PARA EXTRAER COOKIES PERSISTENTES DE VARIAS BASES DE DATOS
# devuelve un diccionario donde las claves son tuplas de la forma
#claves = (domain, nombre)
#y los valores son los correspondientes a dicha cookie
#estas cookies no deben ser transitorias, deben persistir al menos
#<num_days = 30> dias

def extract_persistent_ids_from_dbs(cookie_dbs, num_days=30):
	for cookie_db in cookie_dbs:
		conn=lite.connect(cookie_db)
		curr=conn.cursor()
		cookie_dict = defaultdict(list)

		for domain, name, value, access, expiry \
			in curr.execute('SELECT host, name, value, accessed, expiry FROM profile_cookies'):
			domain = domain if len(domain) == 0 or domain[0] != "." else domain[1:]

			if (domain == '' or name == '' or value == ''):
				continue

			if ((float(expiry) - (float(access)/1000000))/60/60/24 < num_days):
				continue

			cookie_dict[(domain, name)].append(value)
			add_inner_cookie_parameters(cookie_dict, domain, name, value)

	final_cookie_dict = {}
	for cookie in cookie_dict:
		if census_util.all_same(cookie_dict[cookie]):
			final_cookie_dict[cookie] = cookie_dict[cookie][0]

	conn.close()
	return final_cookie_dict

#FUNCION PARA EXTRAER POSIBLES IDS DE VARIAS BASES DE DATOS
#se considera que una cadena de texto es id si
#1.tienen la misma longitud
#2. la cookie aparece en al menos dos rastreos diferentes
#3. tiene al menos <short_cutoff> caracterectes pero no mas de <long_cutoff> caracteres
#4. una pareja de ids no puede ser mas similar que un <sim>%
#5. los ids deben permanecer constantes a lo largo de un rastreo
#devuelve un diccionario con los dominios como clave y los nombres de las cookies como una lista de valores
#el input debe ser de la forma [profile_1, profile_2]

def extract_common_id_cookies(cookie_id_dicts, short_cutoff=6, long_cutoff=100, sim=0.33):
	id_dict = defaultdict(list)

	for cookie_id_dict in cookie_id_dicts:
		for cookie in cookie_id_dict:
			id_dict[cookie].append(cookie_id_dict[cookie])

	final_cookie_id_dict = defaultdict(list)

	for cookie in id_dict:
		if len(id_dict[cookie]) <= 1 \
			or len(id_dict[cookie][0])<short_cutoff \
			or len(id_dict[cookie][0])>long_cutoff \
			or not census_util.all_same_len(id_dict[cookie]) \
			or not census_util.all_dissimilar(id_dict[cookie], sim):
			continue

		final_cookie_id_dict[cookie[0]].append(cookie[1])

	return final_cookie_id_dict

#FUNCION PARA MAPEAR LOS IDS DE COOKIES CON SU VALOR DE ID REAL EXTRAIDO DE UNA INSTANCIA DE UNA BASE DE DATOS
#dado un diccionario de ids persistentes cruzarlo con los datos de una bbdd
#y devolver un diccionario con los ids persistentes y sus valores unicos que parecen en la bbdd (si aparecen)

def extract_known_cookies_from_db(db_name, cookie_id_dict):
	conn=lite.connect(db_name)
	cur = conn.cursor()

	found_cookies={}
	for domain, name, value \
			in cur.execute('SELECT host, name, value FROM profile_cookies'):
		domain = domain if len(domain) == 0 or domain[0] != "." else domain[1:]

		if (domain == '' or name == '' or value == ''):
			continue

		if domain in cookie_id_dict and name in cookie_id_dict[domain]:
			found_cookies[(domain, name)] = value

			if "=" in value:
				for delimiter in ["&", ":"]:
					parts = value.split(delimiter)
					for part in parts:
						params = part.split("=")
						if len(params)==2 and name +"#" +params[0] in cookie_id_dict[domain] \
							and params[0] !='' and params[1] !='':
							found_cookies[(domain, name+"#"+params[0])] = params[1]
	conn.close()
	return found_cookies

#FUNCION QUE MAPEA LOS IDS CON LAS COOKIES EN LAS QUE APARECEN
#lee de un diccionario sacado con extract_known_cookies_from_db
#construir un nuevo diccionario donde cada clave es un d unico 
#y cada valor es una lista de cookies que tienen ese valor

def map_ids_to_cookies(known_cookies):
	id_dict = defaultdict(list)

	for cookie in known_cookies:
		id_dict[known_cookies[cookie]].append(cookie)

	return id_dict