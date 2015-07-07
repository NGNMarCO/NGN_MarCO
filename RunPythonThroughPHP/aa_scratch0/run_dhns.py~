
def bom_init_dhn(dhn_gamma):
	import sys
	import networkx as nx
	import matplotlib.pyplot as plt
	import math
	import random
	from heapq import heappop, heappush
	def set_new_attribute_to_nodes(graph,attribute,value):
		for n in graph.nodes_iter():
			nx.set_node_attributes(graph, attribute, {n: value})
	def find_nodes_by_attribute(graph,attribute,value):
			nodes = list()
			for n in graph.nodes_iter():
				try:
					if (graph.node[n][attribute] == value):
						nodes.append(n)
				except:
					pass
			if len(nodes) > 1:
				return nodes
			else:
				return False
	def find_edges_by_attribute(graph,attribute,value):
		edges = list()
		for u,v,d in graph.edges(data=True):
			try:
				if d[attribute]==value:
					edges.append((u,v,d))
			except:
				pass
		if len(edges) > 1:
			return edges
		else:
			return False
	def restore_attributes(graph):
		for u,v,d in graph.edges(data=True):
			try:
				if d['building_i'] != -1:
					if (graph.degree(u) > 1 and graph.degree(v) > 1):
						d['population'] = -1
						d['building_i'] = -1
			except:
				pass
	def change_length_attr(graph):
		for u,v,d in graph.edges(data=True):
			nx.set_edge_attributes(graph, 'weight', {(u,v): d['length']})
	def find_building_edges(graph):
		edges = list()
		for u,v,d in graph.edges(data=True):
			try:
				#print d['BUILDING_I']
				if d['building_i'] != -1:
					edges.append((u,v,d))
			except:
				pass
		if len(edges) > 1:
			return edges
		else:
			return False
	def find_building_edges_and_update_nodes(graph):
		building_edges = find_building_edges(graph)
		for u,v,d in building_edges:
			degreeofu = graph.degree(u)
			degreeofv = graph.degree(v)
			if degreeofv == 1:
				#graph.node[v]['population'] = d['population']
				#graph.node[v].values().append({'population': d['population']})
				nx.set_node_attributes(graph, 'population', {v: d['population']})
				nx.set_node_attributes(graph, 'building_i', {v: d['building_i']})
				nx.set_node_attributes(graph, 'block_id', {v: d['block_id']})
			elif degreeofu == 1:
				#if degreeofu ==1:
				#graph.node[u]['population'] = d['population']
				#graph.node[u].values().append({'population': d['population']})
				nx.set_node_attributes(graph, 'population', {u: d['population']})
				nx.set_node_attributes(graph, 'building_i', {u: d['building_i']})
				nx.set_node_attributes(graph, 'block_id', {u: d['block_id']})
		return len(building_edges)
	larissa =  nx.DiGraph.to_undirected(nx.read_shp('/home/bluesman/Dropbox/NGNMarcostuff/LarissasPython/aa_scratch/networkcreationclean.py/revision10/forNetX/axons_larissa_with_buildings6_sub0.shp'))#forNetX
	#print "graph directed? "+str(nx.is_directed(larissa))
	#print "graph connected? "+str(nx.is_connected(larissa))
	#print "number of isolated nodes: "+str(len(nx.isolates(larissa)))
	set_new_attribute_to_nodes(larissa,'population',-1.0)
	set_new_attribute_to_nodes(larissa,'building_i',-1)
	set_new_attribute_to_nodes(larissa,'block_id',-1)
	#set_new_attribute_to_nodes(larissa,'rev',0)
	#set_new_attribute_to_nodes(larissa,'prob_index',0.0)
	change_length_attr(larissa)
	num = find_building_edges_and_update_nodes(larissa)
	#print len(find_building_edges(larissa))
	restore_attributes(larissa)
	#print len(find_building_edges(larissa))
	check = [nod for nod in larissa.degree() if larissa.degree(nod) > 1 and larissa.node[nod]['population'] != -1]
	#print len(check)
	#for node in check:
	#	print larissa.node[node]['building_i']
	#sys.exit(1)
	#print str(len(check))+ " einai me degree >1 kai building node"
	d = nx.connected_component_subgraphs(larissa)
	#print str(len(d))+ " einai ta subgraphs"
	#print str(len(larissa.selfloop_edges(data=True)))+" einai ta self loop edges"
	G = larissa
	population_to_int(G)
	#
	#def bom_init_dhn(G,gamma,dhn_gamma):
	g_gamma = cluster_to_subready(G,gamma)
	#dhn_gamma = find_dhn(G,g_gamma)
	ggg_gamma, node100, cost100 = netwrk_cost_dummy2_not(G,g_gamma,dhn_gamma)
	return [dhn_gamma,costs_tr(ggg_gamma),bom_grans(ggg_gamma,node100)]


bom_init_dhn(dhn_gamma)



