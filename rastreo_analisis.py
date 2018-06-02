import census_util
from collections import defaultdict
import sqlite3 as lite
import extraccion_id_cookies
import extract_id_knowledge 
import deteccion_cookie_syncing
import numpy

#Abrimos las dos bases de datos
f=open("bbdd.txt", "r")
filename1 = f.readline()
filename1 = filename1.replace(".txt", '')
filename1 = filename1.replace("/home/elisamerida/Escritorio/Interfaz/",'')
filename1 = filename1.replace("\n",'')
#print(filename1)
filename2 = f.readline()
filename2 = filename2.replace(".txt", '')
filename2 = filename2.replace("/home/elisamerida/Escritorio/Interfaz/",'')
filename2 = filename2.replace("\n",'')
#print(filename2)
f.close()

bbdd1 = '/home/elisamerida/Desktop/RastreoPruebas/rastreo'+filename1+'.sqlite'
conn1 = lite.connect(bbdd1)
bbdd2 = '/home/elisamerida/Desktop/RastreoPruebas/rastreo'+filename2+'.sqlite'
conn2 = lite.connect(bbdd2)
#print(bbdd1)
#print(bbdd2)

print "Extraemos las cookies persistentes de ambas bases de datos..."
cookies_bbdd1 = extraccion_id_cookies.extract_persistent_ids_from_dbs([bbdd1])
cookies_bbdd2 = extraccion_id_cookies.extract_persistent_ids_from_dbs([bbdd2])

print "Extraemos los identificadores comunes en varios rastreos..."
id_cookies = extraccion_id_cookies.extract_common_id_cookies([cookies_bbdd1, cookies_bbdd2])

print "Mapeo entre los dominios y aquellos que lo solicitan de forma directa..."
domain_to_fp_map1= census_util.build_domain_map(bbdd1)
domain_to_fp_map2 = census_util.build_domain_map(bbdd2)

print "Extraccion de los valores de los identificadores conocidos..."
known_ids1 = extraccion_id_cookies.extract_known_cookies_from_db(bbdd1, id_cookies)
known_ids2 = extraccion_id_cookies.extract_known_cookies_from_db(bbdd2, id_cookies)

#Borramos las cookies de rechazo

for key in known_ids1.keys():
	if(known_ids1[key] == '0' or known_ids1[key] == '00000000-0000-0000-0000-000000000000' \
	or known_ids1[key] == '0000000000000000' or known_ids1[key] == 'AAAAAAAAAAAAAAAAAAAAAA'):
		del known_ids1[key]

for key in known_ids2.keys():
	if(known_ids2[key] == '0' or known_ids2[key] == '00000000-0000-0000-0000-000000000000' \
	or known_ids2[key] == '0000000000000000' or known_ids2[key] == 'AAAAAAAAAAAAAAAAAAAAAA'):
		del known_ids2[key]

print "Contruyendo los mapas entre los identificadores y las cookies en las que aparecen..."
id_to_cookie_map1 = extraccion_id_cookies.map_ids_to_cookies(known_ids1)
id_to_cookie_map1_pruned = census_util.prune_list_dict(id_to_cookie_map1)
id_to_cookie_map2 = extraccion_id_cookies.map_ids_to_cookies(known_ids2)
id_to_cookie_map2_pruned = census_util.prune_list_dict(id_to_cookie_map2)

print "Construyendo los mapas entre los identificadores y los dominios que los conocen..."
id_to_domain_map1 = extract_id_knowledge.build_id_knowledge_dictionary(id_to_cookie_map1, bbdd1)
id_to_domain_map1_pruned = census_util.prune_list_dict(id_to_domain_map1)
id_to_domain_map2 = extract_id_knowledge.build_id_knowledge_dictionary(id_to_cookie_map2, bbdd2)
id_to_domain_map2_pruned = census_util.prune_list_dict(id_to_domain_map2)

print "Construyendo los mapas los dominios y los identificadores que conocen..."
domain_to_id_map1= extract_id_knowledge.map_domains_to_known_ids(id_to_domain_map1_pruned)
domain_to_id_map1_pruned = census_util.prune_list_dict(domain_to_id_map1)
domain_to_id_map2= extract_id_knowledge.map_domains_to_known_ids(id_to_domain_map2_pruned)
domain_to_id_map2_pruned = census_util.prune_list_dict(domain_to_id_map2)

f = open("resultados.txt", "w")
f.write("===========================================================================================\n======================================BASE DE DATOS 1======================================\n===========================================================================================")
f.write("\n\n===========================================================================================")
f.write("\n ID y numero de dominios que lo conocen:\n")


print "==========================================================================================="
print "======================================BASE DE DATOS 1======================================"
print "==========================================================================================="

print "==========================================================================================="

print "\n ID y numero de dominios que lo conocen:"
id_to_domain_counts1 = census_util.sort_tuples([(key, len(id_to_domain_map1_pruned[key])) for key in id_to_domain_map1_pruned])
id_to_dm1 = list()
for x in id_to_domain_counts1:
	id_to_dm1.append(x[1])
	print str(x[0])+"\t"+str(x[1])
	f.write(str(x[0])+"\t"+str(x[1])+"\n")

f.write("\n===========================================================================================")
print "==========================================================================================="
f.write("\n Dominio y IDs que dicho dominio conoce:\n")
print "\n Dominio y IDs que dicho dominio conoce:"
domain_to_id_counts1 = census_util.sort_tuples([(key, len(domain_to_id_map1[key])) for key in domain_to_id_map1])
for x in domain_to_id_counts1:
	print str(x[0])+"\t"+str(x[1])
	f.write(str(x[0])+"\t"+str(x[1])+"\n")

f.write("\n===========================================================================================")
print "==========================================================================================="

f.write("\n Dominio y numero de visitas de del historial conocido:\n")
print "\n Dominio y numero de visitas de del historial conocido:"
dm_to_id1 = list()
for domain, count in domain_to_id_counts1:
	neigh1 = extract_id_knowledge.build_hop_neighborhood(domain, 1, domain_to_id_map1, id_to_domain_map1_pruned)
	depth1 = len(neigh1)
	num_doms1 = len(census_util.get_values_from_keys(neigh1, domain_to_fp_map1))

	neigh2 = extract_id_knowledge.build_hop_neighborhood(domain, 2, domain_to_id_map1, id_to_domain_map1_pruned)
	depth2 = len(neigh2)
	num_doms2 = len(census_util.get_values_from_keys(neigh2, domain_to_fp_map1))

	dm_to_id1.append(count)
	print str(domain) + "\t" + str(count) + "\t" + str(depth1) + "\t" + str(num_doms1) 
	print "\t" + str(depth2) + "\t" + str(num_doms2)
	f.write(str(domain) + "\t" + str(count) + "\t" + str(depth1) + "\t" + str(num_doms1)+"\t" + str(depth2) + "\t" + str(num_doms2)+"\n")

f.write("\n===========================================================================================")
print "==========================================================================================="
f.write("\n RESUMEN DE ESTADISTICAS:\n")
print "\n RESUMEN DE ESTADISTICAS:"
f.write("\nNUMERO DE IDS: " + str(len(id_to_cookie_map1)))
print "NUMERO DE IDS: " + str(len(id_to_cookie_map1))

f.write("\nNUMERO DE IDS COOKIES: " + str(len(known_ids1)))
print "NUMERO DE IDS COOKIES: " + str(len(known_ids1))

f.write("\nNUMERO DE IDS IMPLICADOS EN SINCRONIZACIONES: " + str(len(id_to_domain_map1)))
print "NUMERO DE IDS IMPLICADOS EN SINCRONIZACIONES: " + str(len(id_to_domain_map1))

f.write("\nNUMERO DE IDS COOKIES IMPLICADOS EN SINCRONIZACIONES: "+ str(sum([len(id_to_cookie_map1[key]) for key in id_to_domain_map1])))
print "NUMERO DE IDS COOKIES IMPLICADOS EN SINCRONIZACIONES: " 
print str(sum([len(id_to_cookie_map1[key]) for key in id_to_domain_map1]))

f.write("\nNUMERO DE DOMINIOS IMPLICADOS EN SINCRONIZACIONES " + str(len(domain_to_id_map1)))
print "NUMERO DE DOMINIOS IMPLICADOS EN SINCRONIZACIONES " + str(len(domain_to_id_map1))

if(len(id_to_dm1)==0):
	id_to_dm1.append(0)
print "DOMINIOS POR CADA ID: \n " + "Minimo="+str(min(id_to_dm1)) + " |  Media="  
print str(numpy.mean(id_to_dm1)) + ' |  Mediana=' + str(numpy.median(id_to_dm1)) + " |  Maximo=" + str(max(id_to_dm1))
f.write("\nDOMINIOS POR CADA ID: \n " + "Minimo="+str(min(id_to_dm1)) + " |  Media="+str(numpy.mean(id_to_dm1)) + ' |  Mediana=' + str(numpy.median(id_to_dm1)) + " |  Maximo=" + str(max(id_to_dm1)))

if(len(dm_to_id1)==0):
	dm_to_id1.append(0)
print "ID POR CADA DOMINIO: \n " + "Minimo="+str(min(dm_to_id1)) + " |  Media="  
print str(numpy.mean(dm_to_id1)) + ' |  Mediana=' + str(numpy.median(dm_to_id1)) + " |  Maximo=" + str(max(dm_to_id1))
f.write("\nID POR CADA DOMINIO: \n " + "Minimo="+str(min(dm_to_id1)) + " |  Media="+str(numpy.mean(dm_to_id1)) + ' |  Mediana=' + str(numpy.median(dm_to_id1)) + " |  Maximo=" + str(max(dm_to_id1)) )


f.write("\n===========================================================================================\n======================================BASE DE DATOS 2======================================\n===========================================================================================")
f.write("\n\n===========================================================================================")
f.write("\n ID y numero de dominios que lo conocen:\n")

print "==========================================================================================="
print "======================================BASE DE DATOS 2======================================"
print "==========================================================================================="

print "==========================================================================================="
print "\n ID y numero de dominios que lo conocen:"
id_to_domain_counts2 = census_util.sort_tuples([(key, len(id_to_domain_map2_pruned[key])) for key in id_to_domain_map2_pruned])
id_to_dm2 = list()
for x in id_to_domain_counts1:
	id_to_dm2.append(x[1])
	print str(x[0])+"\t"+str(x[1])
	f.write(str(x[0])+"\t"+str(x[1])+"\n")

#print len(id_to_domain_counts2)
f.write("\n===========================================================================================")
print "==========================================================================================="
f.write("\n Dominio y IDs que dicho dominio conoce:\n")
print "\n Dominio y IDs que dicho dominio conoce:"
domain_to_id_counts2 = census_util.sort_tuples([(key, len(domain_to_id_map2[key])) for key in domain_to_id_map2])
for x in domain_to_id_counts2:
	print str(x[0])+"\t"+str(x[1])
	f.write(str(x[0])+"\t"+str(x[1])+"\n")
#print len(domain_to_id_counts2)
f.write("\n===========================================================================================")
print "==========================================================================================="
f.write("\n Dominio y numero de visitas de del historial conocido:\n")
print "\n Dominio y numero de visitas de del historial conocido:"
dm_to_id2 = list()
for domain, count in domain_to_id_counts2:
	neigh3 = extract_id_knowledge.build_hop_neighborhood(domain, 1, domain_to_id_map2, id_to_domain_map2_pruned)
	depth3 = len(neigh3)
	num_doms3 = len(census_util.get_values_from_keys(neigh3, domain_to_fp_map2))

	neigh4 = extract_id_knowledge.build_hop_neighborhood(domain, 2, domain_to_id_map2, id_to_domain_map2_pruned)
	depth4 = len(neigh4)
	num_doms4 = len(census_util.get_values_from_keys(neigh4, domain_to_fp_map2))

	dm_to_id2.append(count)
	f.write(str(domain) + "\t" + str(count) + "\t" + str(depth3) + "\t" + str(num_doms3)+"\t" + str(depth4) + "\t" + str(num_doms4))
	print str(domain) + "\t" + str(count) + "\t" + str(depth3) + "\t" + str(num_doms3) 
	print "\t" + str(depth4) + "\t" + str(num_doms4)

f.write("\n===========================================================================================")
print "==========================================================================================="
print "\n RESUMEN DE ESTADISTICAS:"
f.write("\n RESUMEN DE ESTADISTICAS:\n")
#NUMERO DE IDENTIFICADORES (PUEDE HABER IDENTIFICADORES QUE APARECEN EN VARIAS COOKIES)

f.write("\nNUMERO DE IDS: " + str(len(id_to_cookie_map2)))
print "NUMERO DE IDS: " + str(len(id_to_cookie_map2))
#NUMERO DE COOKIES EXTRAIDAS DE LA BASE DE DATOS
f.write("\nNUMERO DE IDS COOKIES: " + str(len(known_ids2)))
print "NUMERO DE IDS COOKIES: " + str(len(known_ids2))

f.write("\nNUMERO DE IDS IMPLICADOS EN SINCRONIZACIONES: " + str(len(id_to_domain_map2)))
print "NUMERO DE IDS IMPLICADOS EN SINCRONIZACIONES: " + str(len(id_to_domain_map2))

f.write("\nNUMERO DE IDS COOKIES IMPLICADOS EN SINCRONIZACIONES: " + str(sum([len(id_to_cookie_map2[key]) for key in id_to_domain_map2])))
print "NUMERO DE IDS COOKIES IMPLICADOS EN SINCRONIZACIONES: " + str(sum([len(id_to_cookie_map2[key]) for key in id_to_domain_map2]))

f.write("\nNUMERO DE DOMINIOS IMPLICADOS EN SINCRONIZACIONES " + str(len(domain_to_id_map2)))
print "NUMERO DE DOMINIOS IMPLICADOS EN SINCRONIZACIONES " + str(len(domain_to_id_map2))

if(len(id_to_dm2)==0):
	id_to_dm2.append(0)
print "DOMINIOS POR CADA ID: \n " + "Minimo="+str(min(id_to_dm2)) + " |  Media="  + str(numpy.mean(id_to_dm2)) + ' |  Mediana=' + str(numpy.median(id_to_dm2)) + " |  Maximo=" + str(max(id_to_dm2))
f.write("\nDOMINIOS POR CADA ID: \n " + "Minimo="+str(min(id_to_dm2)) + " |  Media="  + str(numpy.mean(id_to_dm2)) + ' |  Mediana=' + str(numpy.median(id_to_dm2)) + " |  Maximo=" + str(max(id_to_dm2)))

if(len(dm_to_id2)==0):
	dm_to_id2.append(0)
print "ID POR CADA DOMINIO: \n " + "Minimo="+str(min(dm_to_id2)) + " |  Media="  + str(numpy.mean(dm_to_id2)) + ' |  Mediana=' + str(numpy.median(dm_to_id2)) + " |  Maximo=" + str(max(dm_to_id2))
f.write("\nID POR CADA DOMINIO: \n " + "Minimo="+str(min(dm_to_id2)) + " |  Media="  + str(numpy.mean(dm_to_id2)) + ' |  Mediana=' + str(numpy.median(dm_to_id2)) + " |  Maximo=" + str(max(dm_to_id2)))
f.close()