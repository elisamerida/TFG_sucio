#MODULO QUE ESTUDIA HASTA DONDE SE HAN EXTENDIDO LOS IDS
import extraccion_id_cookies
import sqlite3 as lite
import census_util
from collections import defaultdict
import Queue
import re
import os

#MAPEA LOS IDS CON LAS PARTIES QUE DEFINITIVAMENTE LOS CONOCEN
#primero miramos las listas de los poseedores de la cookie, que conocen el id (visto en el diccionario)
#despues miramos en las http_responses y locations
#finalmente podemos mirar en las http_requests

def build_id_knowledge_dictionary(cookie_id_dict, cookie_db):
	id_knowledge_dict = defaultdict(list)
	conn = lite.connect(cookie_db)
	cur = conn.cursor()

	for domain, value in cur.execute('SELECT DISTINCT host, value FROM profile_cookies'):
		domain = domain if len(domain) == 0 or domain[0] != "." else domain[1:]  
        domain = census_util.extract_domain(domain)
      
        for cookie_id in cookie_id_dict:
			if cookie_id in value:
				id_knowledge_dict[cookie_id].append(domain)

	for url, referrer in cur.execute('SELECT DISTINCT url, referrer FROM http_requests'):
		short_url = census_util.extract_domain(url)
		short_referrer = census_util.extract_domain(referrer)

		for cookie_id in cookie_id_dict:
			if cookie_id in url:
				id_knowledge_dict[cookie_id].append(short_url)
			if cookie_id in referrer:
				id_knowledge_dict[cookie_id].append(short_referrer)
				id_knowledge_dict[cookie_id].append(short_url)

	for url, referrer, location in cur.execute('SELECT DISTINCT url, referrer, location FROM http_responses'):
		short_url = census_util.extract_domain(url)
		short_referrer = census_util.extract_domain(referrer)
        short_location = census_util.extract_domain(location)
        for cookie_id in cookie_id_dict:
			if cookie_id in url:
				id_knowledge_dict[cookie_id].append(short_url)
			if cookie_id in location:
				id_knowledge_dict[cookie_id].append(short_location)
				id_knowledge_dict[cookie_id].append(short_url)
			if cookie_id in referrer:
				id_knowledge_dict[cookie_id].append(short_referrer)
				id_knowledge_dict[cookie_id].append(short_url)
				if short_location != '':
					id_knowledge_dict[cookie_id].append(short_location)

	unique_domains = list()
	for cookie_id in id_knowledge_dict:
		unique_domains = census_util.unique(id_knowledge_dict[cookie_id])
		unique_domains.sort()
		id_knowledge_dict[cookie_id] = unique_domains
		# if '' in unique_domains:
		# 	unique_domains.remove('')
        
	
	return id_knowledge_dict

#MAPEA LOS DOMINIOS CON LA LISTA DE IDS QUE CONOCEMOS
#coge el diccionario producido por build_id_knowledge_dictionary y devuelve el inverso
# en particular, keys = dominios y valores= lista de ids conocidos por dicho dominio

def map_domains_to_known_ids(id_knowledge_dict):
	domain_knowledge_dict = defaultdict(list)

	for cookie_id in id_knowledge_dict:
		for domain in id_knowledge_dict[cookie_id]:
			domain_knowledge_dict[domain].append(cookie_id)

	for domain in domain_knowledge_dict:
		id_list = domain_knowledge_dict[domain]
		id_list.sort()
		domain_knowledge_dict[domain] = id_list

	return domain_knowledge_dict

#Busqueda en anchura , analisis de saltos
#para un dominio dado, devuelve una lista ordenada de sitios
#dentro de <hops> saltos en el grafico de sincronizacion

def build_hop_neighborhood(seed_domain, hop, domain_to_id, id_to_domain):
	domains_explored = set()
	search_queue = Queue.Queue()
	search_queue.put((seed_domain, 0))

	while not search_queue.empty():
		curr_domain, curr_depth = search_queue.get()

		if curr_depth > hop:
			break

		if curr_domain in domains_explored:
			continue

		domains_explored.add(curr_domain)

		if curr_depth == hop:
			continue

		for cookie_id in domain_to_id[curr_domain]: 
			for domain in id_to_domain[cookie_id]: 
				search_queue.put((domain, curr_depth+1)) 

	neighborhood = list(domains_explored)
	neighborhood.sort()
	return neighborhood
