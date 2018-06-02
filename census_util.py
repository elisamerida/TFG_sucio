import difflib
import itertools
import urlparse
from tld import get_tld
from collections import defaultdict
import sqlite3 as lite


#Funcion que comprueba si todos los items son iguales
def all_same(items):
	return all(x==items[0] for x in items)


#Funcion que compruba si todos los items son de la misma longitud
def all_same_len(items):
	return all(len(x) == len(items[0]) for x in items)

#Funcion que comprueba si dos cookies son mas de <sim>% similares
#de acuerdo con el algoritmo Ratcliff-Obershelp
def ro_similar(seq1, seq2, sim=0.33):
	#mide la similaridad de las dos secuencias y devuelve si es mayor que 0.33
	return difflib.SequenceMatcher(a=seq1, b=seq2).ratio() >=sim

#Funcion que comprueba si todas las cookies de una lista
#son distintas por parejas
def all_dissimilar(items, sim= 0.33):
	#devuelve todas las parejas posibles hechas con items
	pairs = list(itertools.combinations(items, 2))
	return all(not ro_similar(x[0], x[1], sim) for x in pairs)

 #Funcion que extrae el dominio a partir de una url
def extract_domain (url):
	if type(url) == type(None):
		return None
	url = url if url.startswith("http") else "http://"+ url
	try:
 		#devuelve el top level domain dada una url
 		return get_tld(url)
 	except:
 		return urlparse.urlparse(url).netloc
 		
#Funcion que devuelve los elementos que son unicos en una lista
def unique(seq):
	#ojo, no se preserva el orden
	lista = {}.fromkeys(seq).keys()
	#print(type(lista))
	return lista

# Funcion que devuelve una lista en la que todas las claves del diccionario tienen mas de 1 valor

def prune_list_dict(list_dict):
    pruned_dict = defaultdict(list)
    for key in list_dict:
        if len(list_dict[key]) > 1:
            pruned_dict[key] = list_dict[key]
    return pruned_dict

# Funcion que ordena la tupla de la forma (x, count) en orden contrario

def sort_tuples(tuple_list):
    return sorted(tuple_list, key = lambda  arr: arr[1], reverse=True)

# Funcion que dada una lista de claves y un defaultdict de lista
#devuelve la union de dict[key] para todas las claves

def get_values_from_keys(keys, value_dict):
    values = set()
    for key in keys:
        values = values.union(set(value_dict[key]))
	return values


#Funcion que construye un mapa de dominios para 
#las primeras partes en las que fueron vistos.
#utiliza HTTP requests para construir el contenido

def build_domain_map(wpm_db):
	domain_to_fp_map = defaultdict(list)
	conn = lite.connect(wpm_db)
	cur = conn.cursor()

	for url, referrer, top_url \
		in cur.execute('SELECT DISTINCT url, referrer, top_level_url FROM http_requests'):
		url = extract_domain(url)
		referrer = extract_domain(referrer)
		top_url = extract_domain(top_url)

		if referrer != '' and url != None and referrer == top_url:
			domain_to_fp_map[url].append(top_url)

	for domain in domain_to_fp_map:
		domain_to_fp_map[domain] = unique(domain_to_fp_map[domain])

	return domain_to_fp_map
