import extraccion_id_cookies
import extract_id_knowledge
import census_util
import sqlite3 as lite
import Queue
import re
import os

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

