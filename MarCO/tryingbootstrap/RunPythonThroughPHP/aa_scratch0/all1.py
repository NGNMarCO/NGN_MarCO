
#!/usr/bin/python


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
set_new_attribute_to_nodes(larissa,'rev',0)
set_new_attribute_to_nodes(larissa,'prob_index',0.0)
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

##############################################################################


# Distance function

def adistance(x,y):
	import math # 'math' needed for 'sqrt'
	sq1 = (x[0] - y[0])**2
	sq2 = (x[1] - y[1])**2
	return math.sqrt(sq1 + sq2)


#create 3vectors of G.nodes() 
def graph_n_vec(GG):
	G = GG
	nn_list = G.nodes()[:]
	n_vec = []
	for i in range(len(nn_list)):
		n_vec.append(list(nn_list[i]))
		n_vec[i].append(G.node[nn_list[i]]['population'])
	return n_vec


##clear the previous list (NO null nodes)
def graph_c_vec(GG):
	G = GG
	n_vec = graph_n_vec(G)[:]
	c_vec = []
	for i in range(len(n_vec)):
		if n_vec[i][2] != -1:
			c_vec.append(n_vec[i])
	return c_vec

#ceiling-flooring the population of a graph G
def population_to_int(GG):
	G = GG
	import math
	for n in G.nodes():
		if math.floor(G.node[n]['population']) == 0:
			G.node[n]['population'] = int(1)
		else:
			if G.node[n]['population'] - math.floor(G.node[n]['population']) <= 0.5:
				G.node[n]['population'] = int(math.floor(G.node[n]['population']))
			else:
				G.node[n]['population'] = int(math.ceil(G.node[n]['population']))


population_to_int(G)

#sumofmass for G ;)
def sumofmass(L):
	"""
	Returns the sum of masses of the points of a list.
	Each point p is of the form p = (x,y,|p|), where x,y are its coordinates
	and |p| is the "mass" of it.
	"""
	som = 0
	if len(L) == 0:
		som = 0
	elif len(L)>=1:
		for i in range(len(L)):
			if L[i][2] != -1: #not the null nodes
				som = float(som + L[i][2])
			else:
				som = som + 0
	return som



def sumofmass0(G,L):
	"""
	Returns the sum of masses of the points of a list of nodes of a graph G.
	"""
	som = 0
	if len(L) == 0:
		som = 0
	elif len(L)>=1:
		for i in L:
			if G.node[i]["population"] != -1: #not the null nodes
				som = float(som + G.node[i]["population"])
			else:
				som = som + 0
	return som




#change the lmnts of a list from 2 to 3 dims
def change_dims(G,LL):
	listn = []
	for i in LL:
		n = (i[0],i[1])
		listn.append([i[0],i[1],G.node[n]['population']])
	return listn



#returns the closest em node to point. using in com ;)
def point_to_node(xx,L):
	x = xx
	PP = L[:]
	dd_l = []
	ssorted_d_l = []
	for j in range(len(PP)):
		dd_l.append([PP[j],adistance(xx,PP[j])])
	from operator import itemgetter, attrgetter
	ssorted_d_l = sorted(dd_l, key=itemgetter(1))
	if ssorted_d_l != []:
		rs = ssorted_d_l[0][0]
	else:
		rs = (0,0)
	return rs




#centerofmass for G
def centerofmass2(LL):
	"""
	Returns the coordinates of the center of mass of a list of points.
	Each point p is of the form p = (x,y,|p|), where x,y are its coordinates
	and |p| is the "mass" of it.
	"""
	comx = 0
	comy = 0
	com = (0,0)
	if len(LL) == 0:
		com = (0,0)
	elif len(LL)==1:
		if LL[0][2] != -1:
			com = (LL[0][0],LL[0][1])
		else:
			com = (0,0)
	elif len(LL) > 1:
		for i in range(len(LL)):
			if LL[i][2] != -1: #not the null nodes
				comx = float(comx + LL[i][0]*LL[i][2])
				comy = float(comy + LL[i][1]*LL[i][2])
		com = (float(comx/sumofmass(LL)),float(comy/sumofmass(LL)))
	ll = []
	xx = com
	dd_l = []
	ssorted_d_l = []
	iinl = []
	for j in range(len(LL)):
		dd_l.append([LL[j],adistance(xx,LL[j])])
	from operator import itemgetter, attrgetter
	if len(dd_l) != 0:
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
		com = (ssorted_d_l[0][0][0],ssorted_d_l[0][0][1])
	p = point_to_node(com,LL)
	return (p[0],p[1])


#centerofmass for G
def centerofmass0(G,LLL):
	"""
	Returns the coordinates of the center of mass of a list of points.
	Each point p is of the form p = (x,y,|p|), where x,y are its coordinates
	and |p| is the "mass" of it.
	"""
	LL = change_dims(G,LLL)[:]
	comx = 0
	comy = 0
	com = (0,0)
	if len(LL) == 0:
		com = (0,0)
	elif len(LL)==1:
		if LL[0][2] != -1:
			com = (LL[0][0],LL[0][1])
		else:
			com = (0,0)
	elif len(LL) > 1:
		for i in range(len(LL)):
			if LL[i][2] != -1: #not the null nodes
				comx = float(comx + LL[i][0]*LL[i][2])
				comy = float(comy + LL[i][1]*LL[i][2])
		com = (float(comx/sumofmass(LL)),float(comy/sumofmass(LL)))
	ll = []
	xx = com
	dd_l = []
	ssorted_d_l = []
	iinl = []
	for j in range(len(LL)):
		dd_l.append([LL[j],adistance(xx,LL[j])])
	from operator import itemgetter, attrgetter
	if len(dd_l) != 0:
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
		com = (ssorted_d_l[0][0][0],ssorted_d_l[0][0][1])
	p = point_to_node(com,LL)
	return (p[0],p[1])


#computes the center of a list of points regarding their coordinates 
#and NOT the mass of them!
def centerofmass(LL):
	"""
	Returns the coordinates of the center of a list of points.
	Each point p is of the form p = (x,y), where x,y are its coordinates
	"""
	comx = 0
	comy = 0
	com = (0,0)
	if len(LL) == 0:
		com = (0,0)
	else: 
		for i in range(len(LL)):
			comx = float(comx + LL[i][0])
			comy = float(comy + LL[i][1])
			com = (float(comx/len(LL)),float(comy/len(LL)))
	p = point_to_node(com,LL)
	return (p[0],p[1])


#return the com of a list of points, that belongs to a graph G 
#the points may or may not belong to G
def centerofmass_n(G,LL):
	"""
	Returns the coordinates of the center of a list of points.
	Each point p is of the form p = (x,y), where x,y are its coordinates
	"""
	comx = 0
	comy = 0
	com = (0,0)
	if len(LL) == 0:
		com = (0,0)
	else: 
		for i in range(len(LL)):
			comx = float(comx + LL[i][0])
			comy = float(comy + LL[i][1])
			com = (float(comx/len(LL)),float(comy/len(LL)))
	c_vec = graph_c_vec(G)[:]
	p = point_to_node(com,c_vec)
	return (p[0],p[1])


#sum of mass of a graph
def sumofmass_graph(GG):
	c_vec = []
	c_vec = graph_c_vec(GG)[:]
	return sumofmass(c_vec)


#center of mass of a graph \in Graph
def centerofmass_graph(GG):
	G = GG
	n_vec = []
	n_vec = graph_n_vec(G)[:]
	p = point_to_node(centerofmass0(G,n_vec),n_vec)
	return (p[0],p[1])


def centerofmass_graph0(GG):
	G = GG
	c_vec = []
	c_vec = graph_c_vec(G)[:]
	p = point_to_node(centerofmass0(G,c_vec),c_vec)
	return (p[0],p[1])


#random nodes of the Graph as initial points for clustering
def ran_points(PP,kk):
	k = kk
	s = PP[:]
	l = []
	l_points = []
	for i in s:
		l.append((i[0],i[1]))
	for j in range(k):
		r = random.choice(l)
		l_points.append(r)
		l.remove(r)
	return l_points


#creates equidistance-points on a circle
def cycpoints(cp,R,np):
	import math
	p0 = cp[:]
	r = R
	n = np
	pL = []
	num = 2*math.pi/n
	x0 = p0[0] #initial point is the center
	y0 = p0[1]
	import math
	for i in range(n):
		x = x0 + r*math.cos(i*num)
		y = y0 + r*math.sin(i*num)
		a = (x,y)
		pL.append(a)
	return pL


#given a point x returns the min. & max. distance of it from a set of points
#and the corresponding points
def minmaxp(PP,x):
	d_l = []
	sorted_d_l = []
	for j in range(len(PP)):
		d_l.append([PP[j],adistance(x,PP[j])])
	from operator import itemgetter, attrgetter
	sorted_d_l = sorted(d_l, key=itemgetter(1))
	if len(sorted_d_l) >1:
		return (sorted_d_l[0], sorted_d_l[len(sorted_d_l)-1])
	else:
		return (sorted_d_l[0], sorted_d_l[0])


#creates random initial coms for clustering (max distance from comP)
#in the circle of center the comP and radius the max distance from it
def rancom_points(PP,k):
	init_L = []
	cpoints = cycpoints(centerofmass(PP),minmaxp(PP,centerofmass(PP))[1][1],k)
	for i in range(len(cpoints)):
		x = cpoints[i] #choose a point from the circle
		d_l = []
		sorted_d_l = []
		inl = []
		for j in range(len(PP)):
			d_l.append([PP[j],adistance(x,PP[j])])
		from operator import itemgetter, attrgetter
		sorted_d_l = sorted(d_l, key=itemgetter(1))
		init_L.append(sorted_d_l[0][0])
	i_l = []
	for i in init_L:
		x = (i[0],i[1])
		i_l.append(x)
	init_L = i_l[:]
	ll = []
	for xx in init_L:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(PP)):
			dd_l.append([PP[j],adistance(xx,PP[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	init_l = ll[:]
	return init_L


#creates random initial coms for clustering (1/2(min + max) distance from comP)
#the circle of center is the comP and the radius is the max distance from it
def rancom_points_half(PP,k):
	init_L = []
	cpoints = cycpoints(centerofmass(PP), 0.5*(minmaxp(PP,centerofmass(PP))[1][1]+minmaxp(PP,centerofmass(PP))[0][1]),k)
	for i in range(len(cpoints)):
		x = cpoints[i] #choose a point from the circle
		d_l = []
		sorted_d_l = []
		inl = []
		for j in range(len(PP)):
			d_l.append([PP[j],adistance(x,PP[j])])
		from operator import itemgetter, attrgetter
		sorted_d_l = sorted(d_l, key=itemgetter(1))
		init_L.append(sorted_d_l[0][0])
	i_l = []
	for i in init_L:
		x = (i[0],i[1])
		i_l.append(x)
	init_L = i_l[:]
	ll = []
	for xx in init_L:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(PP)):
			dd_l.append([PP[j],adistance(xx,PP[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	init_l = ll[:]
	return init_L


#creates random initial coms for clustering (1/10(min + max) distance from comP)
#the circle of center is the comP and the radius is the max distance from it
def rancom_points_tenth(PP,k):
	init_L = []
	cpoints = cycpoints(centerofmass(PP), 0.1*(minmaxp(PP,centerofmass(PP))[1][1]+minmaxp(PP,centerofmass(PP))[0][1]),k)
	for i in range(len(cpoints)):
		x = cpoints[i] #choose a point from the circle
		d_l = []
		sorted_d_l = []
		inl = []
		for j in range(len(PP)):
			d_l.append([PP[j],adistance(x,PP[j])])
		from operator import itemgetter, attrgetter
		sorted_d_l = sorted(d_l, key=itemgetter(1))
		init_L.append(sorted_d_l[0][0])
	i_l = []
	for i in init_L:
		x = (i[0],i[1])
		i_l.append(x)
	init_L = i_l[:]
	ll = []
	for xx in init_L:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(PP)):
			dd_l.append([PP[j],adistance(xx,PP[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	init_l = ll[:]
	return init_L


#creates random initial coms for clustering (1/20(min + max) distance from comP)
#the circle of center is the comP and the radius is the max distance from it
def rancom_points_20th(PP,k):
	init_L = []
	cpoints = cycpoints(centerofmass(PP), 0.05*(minmaxp(PP,centerofmass(PP))[1][1]+minmaxp(PP,centerofmass(PP))[0][1]),k)
	for i in range(len(cpoints)):
		x = cpoints[i] #choose a point from the circle
		d_l = []
		sorted_d_l = []
		inl = []
		for j in range(len(PP)):
			d_l.append([PP[j],adistance(x,PP[j])])
		from operator import itemgetter, attrgetter
		sorted_d_l = sorted(d_l, key=itemgetter(1))
		init_L.append(sorted_d_l[0][0])
	i_l = []
	for i in init_L:
		x = (i[0],i[1])
		i_l.append(x)
	init_L = i_l[:]
	ll = []
	for xx in init_L:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(PP)):
			dd_l.append([PP[j],adistance(xx,PP[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	init_l = ll[:]
	return init_L


###############################################################################

#MUST for em
def acluster2(Q,ccc,ki):
	S = Q[:]
	com_l = ccc
	k = ki
	clusters = []
	distance_l = []
	min_ind = 0
	x_l = []
	D_l = []
	cl = []
	for i in range(k): #creates k-clusters
		cl.insert(0,[])
	for j in range(len(S)):
		x = S[j] #choose a point from S
		dis_l = []
		min_dis_l = []
		for i in range(k): #list of distances of x from coms
			dis_l.append([adistance(x,com_l[i]), i])
		from operator import itemgetter, attrgetter
		min_dis_l = min(dis_l, key=itemgetter(0))
		cl[min_dis_l[1]].append(x)
	clusters = cl
	comall0 = []
	for i in range(k):
		comall0.append((point_to_node(centerofmass(clusters[i]),S)[0],point_to_node(centerofmass(clusters[i]),S)[1]))
	ll = []
	for xx in comall0:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(S)):
			dd_l.append([S[j],adistance(xx,S[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	comall0 = ll[:]
	return([comall0, clusters, x_l])


#MUST for em
#ak-com clustering
def akcom0(Q0,ccc0,ki0,it0):
	C = acluster2(Q0,ccc0,ki0)
	Ca = [0]
	Cb = [1]
	for i in range(it0-1):
		if Ca != Cb:
			C = acluster2(Q0,C[0],ki0)
			Ca = Cb
			Cb = C[0]
		else:
			break
	return([C,i])

###############################################################################

#MUST for em
def acluster2_com(Q,ccc,ki):
	S = Q[:]
	com_l = ccc
	k = ki
	clusters = []
	distance_l = []
	min_ind = 0
	x_l = []
	D_l = []
	cl = []
	for i in range(k): #creates k-clusters
		cl.insert(0,[])
	for j in range(len(S)):
		x = S[j] #choose a point from S
		dis_l = []
		min_dis_l = []
		for i in range(k): #list of distances of x from coms
			dis_l.append([adistance(x,com_l[i]), i])
		from operator import itemgetter, attrgetter
		min_dis_l = min(dis_l, key=itemgetter(0))
		if x not in cl[min_dis_l[1]]:
			cl[min_dis_l[1]].append(x)
			com_l[min_dis_l[1]] = (point_to_node(centerofmass0(g,cl[min_dis_l[1]]),S)[0],point_to_node(centerofmass0(g,cl[min_dis_l[1]]),S)[1])
	clusters = cl
	comall0 = []
	for i in range(k):
		comall0.append((point_to_node(centerofmass0(g,cl[i]),S)[0],point_to_node(centerofmass0(g,cl[i]),S)[1]))
	ll = []
	for xx in comall0:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(S)):
			dd_l.append([S[j],adistance(xx,S[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	comall0 = ll[:]
	return([comall0, clusters, x_l])


#MUST for em
#ak-com clustering
def akcom0_com(Q0,ccc0,ki0,it0):
	C = acluster2_com(Q0,ccc0,ki0)
	Ca = [0]
	Cb = [1]
	for i in range(it0-1):
		if Ca != Cb:
			C = acluster2(Q0,C[0],ki0)
			Ca = Cb
			Cb = C[0]
		else:
			break
	return([C,i])

###############################################################################

#MUST for em
#do not accept node to a cluster if cluster mass > c_mass
def acluster2n(G,Q,ccc,ki):
	S = Q[:]
	com_l = ccc
	k = ki
	c_mass = sumofmass_graph(G)/k #this is the new
	clusters = []
	distance_l = []
	min_ind = 0
	x_l = []
	D_l = []
	cl = []
	for i in range(k): #creates k-clusters
		cl.insert(0,[])
	#
	for j in range(len(S)):
		x = S[j] #choose a point from S
		dis_l = []
		min_dis_l = []
		for i in range(k): #list of distances of x from coms
			dis_l.append([adistance(x,com_l[i]), i])
		from operator import itemgetter, attrgetter
		min_dis_l = min(dis_l, key=itemgetter(0))
		sorted_dis_l = sorted(dis_l)
		jj = 0
		de = 1
		while jj < k and de == 1:
			if sumofmass(cl[sorted_dis_l[jj][1]]) <= c_mass: #checks if the som of cl is ok to accept the point
				cl[sorted_dis_l[jj][1]].append(x)
				de = 0
			else:
				jj = jj + 1
	#
	clusters = cl
	comall0 = []
	for i in range(k):
		#comall0.append((point_to_node(centerofmass(clusters[i]),S)[0],point_to_node(centerofmass(clusters[i]),S)[1]))
		comall0.append((point_to_node(centerofmass(clusters[i]),S)[0],point_to_node(centerofmass(clusters[i]),S)[1]))
	ll = []
	for xx in comall0:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(S)):
			dd_l.append([S[j],adistance(xx,S[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	comall0 = ll[:]
	return([comall0, clusters, x_l])


#MUST for em
#ak-com clustering
def akcom0_n(G,Q0,ccc0,ki0,it0):
	C = acluster2n(G,Q0,ccc0,ki0)
	Ca = [0]
	Cb = [1]
	for i in range(it0-1):
		if Ca != Cb:
			C = acluster2n(Q0,C[0],ki0)
			Ca = Cb
			Cb = C[0]
		else:
			break
	return([C,i])

###############################################################################

#ccc = [(364366.535257, 4388007.722015), (364049.40164999996, 4388186.605506), (364066.85834599996, 4387831.357523)][:]


#for sp
def acluster22(Q,ccc,ki):
	S = Q[:]
	com_l = ccc
	k = ki
	clusters = []
	distance_l = []
	min_ind = 0
	x_l = []
	D_l = []
	cl = []
	for i in range(k): #creates k-clusters
		cl.insert(0,[])
	for j in range(len(S)):
		y = S[j] #choose a point from S
		x = (y[0],y[1])
		dis_l = []
		min_dis_l = []
		for i in range(k): #list of distances of x from coms
			#dis_l.append([nx.shortest_path_length(G, source=x, target=com_l[i]), i])
			dis_l.append([nx.dijkstra_path_length(G, source=x, target=com_l[i]), i])
		from operator import itemgetter, attrgetter
		min_dis_l = min(dis_l, key=itemgetter(0))
		cl[min_dis_l[1]].append(y)
	clusters = cl[:]
	comall0 = []
	for i in range(k):
		comall0.append((point_to_node(centerofmass(clusters[i]),S)[0],point_to_node(centerofmass(clusters[i]),S)[1]))
	ll = []
	for xx in comall0:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(S)):
			dd_l.append([S[j],adistance(xx,S[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append( (ssorted_d_l[0][0][0],ssorted_d_l[0][0][1]) )
	comall0 = ll[:]
	return([comall0, clusters, x_l])


#for sp
def akcom00(QQ,ccc0,ki0,it0):
	C = acluster22(QQ,ccc0,ki0)
	Ca = [0]
	Cb = [1]
	for i in range(it0-1):
		if Ca != Cb:
			C = acluster22(QQ,C[0],ki0)
			Ca = Cb
			Cb = C[0]
		else:
			break
	return([C,i])

###############################################################################


#MUST for em
def acluster22_com(Q,ccc,ki):
	S = Q[:]
	com_l = ccc
	k = ki
	clusters = []
	distance_l = []
	min_ind = 0
	x_l = []
	D_l = []
	cl = []
	for i in range(k): #creates k-clusters
		cl.insert(0,[])
	for j in range(len(S)):
		x = S[j] #choose a point from S
		dis_l = []
		min_dis_l = []
		for i in range(k): #list of distances of x from coms
			dis_l.append([nx.dijkstra_path_length(G, source=x, target=com_l[i]), i])
		from operator import itemgetter, attrgetter
		min_dis_l = min(dis_l, key=itemgetter(0))
		if x not in cl[min_dis_l[1]]:
			cl[min_dis_l[1]].append(x)
			com_l[min_dis_l[1]] = (point_to_node(centerofmass0(g,cl[min_dis_l[1]]),S)[0],point_to_node(centerofmass0(g,cl[min_dis_l[1]]),S)[1])
	clusters = cl
	comall0 = []
	for i in range(k):
		comall0.append((point_to_node(centerofmass0(g,cl[i]),S)[0],point_to_node(centerofmass0(g,cl[i]),S)[1]))
	ll = []
	for xx in comall0:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(S)):
			dd_l.append([S[j],adistance(xx,S[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append(ssorted_d_l[0][0])
	comall0 = ll[:]
	return([comall0, clusters, x_l])


#MUST for em
#ak-com clustering
def akcom00_com(Q0,ccc0,ki0,it0):
	C = acluster2_com(Q0,ccc0,ki0)
	Ca = [0]
	Cb = [1]
	for i in range(it0-1):
		if Ca != Cb:
			C = acluster2(Q0,C[0],ki0)
			Ca = Cb
			Cb = C[0]
		else:
			break
	return([C,i])

###############################################################################


#for sp
def acluster22_n(Q,ccc,ki):
	S = Q[:]
	com_l = ccc
	k = ki
	c_mass = sumofmass_graph(g)/k #this is the new
	clusters = []
	distance_l = []
	min_ind = 0
	x_l = []
	D_l = []
	cl = []
	for i in range(k): #creates k-clusters
		cl.insert(0,[])
	#
	for j in range(len(S)):
		y = S[j] #choose a point from S
		x = (y[0],y[1])
		dis_l = []
		min_dis_l = []
		for i in range(k): #list of distances of x from coms
			dis_l.append([nx.dijkstra_path_length(G, source=x, target=com_l[i]), i])
		from operator import itemgetter, attrgetter
		min_dis_l = min(dis_l, key=itemgetter(0))
		sorted_dis_l = sorted(dis_l)
		jj = 0
		de = 1
		while jj < k and de == 1:
			if sumofmass(cl[sorted_dis_l[jj][1]]) <= c_mass: #checks if the som of cl is ok to accept the point
				cl[sorted_dis_l[jj][1]].append(y)
				de = 0
			else:
				jj = jj + 1
	#
	clusters = cl[:]
	comall0 = []
	for i in range(k):
		comall0.append((point_to_node(centerofmass(clusters[i]),S)[0],point_to_node(centerofmass(clusters[i]),S)[1]))
	ll = []
	for xx in comall0:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(S)):
			dd_l.append([S[j],adistance(xx,S[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append( (ssorted_d_l[0][0][0],ssorted_d_l[0][0][1]) )
	comall0 = ll[:]
	return([comall0, clusters, x_l])


#for sp
def akcom00_n(QQ,ccc0,ki0,it0):
	C = acluster22_n(QQ,ccc0,ki0)
	Ca = [0]
	Cb = [1]
	for i in range(it0-1):
		if Ca != Cb:
			C = acluster22_n(QQ,C[0],ki0)
			Ca = Cb
			Cb = C[0]
		else:
			break
	return([C,i])

###############################################################################


#for sp
#add G and change centerofmass to 0
def acluster222(G,Q,ccc,ki):
	S = Q[:]
	com_l = ccc
	k = ki
	clusters = []
	distance_l = []
	min_ind = 0
	x_l = []
	D_l = []
	cl = []
	for i in range(k): #creates k-clusters
		cl.insert(0,[])
	for j in range(len(S)):
		y = S[j] #choose a point from S
		x = (y[0],y[1])
		dis_l = []
		min_dis_l = []
		for i in range(k): #list of distances of x from coms
			#dis_l.append([nx.shortest_path_length(G, source=x, target=com_l[i]), i])
			dis_l.append([nx.dijkstra_path_length(G, source=x, target=com_l[i]), i])
		from operator import itemgetter, attrgetter
		min_dis_l = min(dis_l, key=itemgetter(0))
		cl[min_dis_l[1]].append(y)
	clusters = cl[:]
	comall0 = []
	for i in range(k):
		comall0.append((point_to_node(centerofmass0(G,clusters[i]),S)[0],point_to_node(centerofmass0(G,clusters[i]),S)[1]))
	ll = []
	for xx in comall0:
		dd_l = []
		ssorted_d_l = []
		iinl = []
		for j in range(len(S)):
			dd_l.append([S[j],adistance(xx,S[j])])
		from operator import itemgetter, attrgetter
		ssorted_d_l = sorted(dd_l, key=itemgetter(1))
		ll.append( (ssorted_d_l[0][0][0],ssorted_d_l[0][0][1]) )
	comall0 = ll[:]
	return([comall0, clusters, x_l])


#for sp
#same as above
def akcom000(G,QQ,ccc0,ki0,it0):
	C = acluster22(G,QQ,ccc0,ki0)
	Ca = [0]
	Cb = [1]
	for i in range(it0-1):
		if Ca != Cb:
			C = acluster22(QQ,C[0],ki0)
			Ca = Cb
			Cb = C[0]
		else:
			break
	return([C,i])

###############################################################################


#returns all shortest paths from xx to a list of nodes LL of the graph GG
def asp_sub(GG,LL,xx):
	G = GG
	L = LL[:]
	x = xx
	dis_l = []
	sorted_dis_l = []
	cs = L[:]
	ccs = [] #change to (,)
	for j in cs:
		ccs.append((j[0],j[1]))
	cs = ccs[:]
	Gsub = G.subgraph(cs)
	s=nx.single_source_dijkstra_path_length(G, (x[0],x[1]))
	for v in list(s):
		if v in Gsub.nodes():
			dis_l.append([v[0],v[1],s.get(v)])
	from operator import itemgetter, attrgetter
	sorted_dis_l = sorted(dis_l, key=itemgetter(2))[:]
	return sorted_dis_l


#given the initial input graph G and after clustering, creates the subgraph g
#that corresponds to a cluster. so it is ready for the Cost functions!
def cluster_to_subgraph(GG,cluster):
	G = GG
	cl = cluster[:]
	l = []
	for i in cl: #3ades-2ades
		l.append((i[0],i[1]))
	comP = point_to_node(centerofmass0(G,cl),l) #finds comP
	#returns all the nodes 
	l_null = []
	s = []
	for node in l:
		s = nx.dijkstra_path(G,comP,node)[:]
		if comP in s:
			s.remove(comP)
		if node in s:
			s.remove(node)
		for n in s:
			if n not in l_null:
				l_null.append(n)
		s = []
	cluster_nodes = l[:]
	for i in l_null:
		cluster_nodes.append(i)
	g = G.subgraph(cluster_nodes)
	return [g,comP]


#given the initial input graph G and after clustering, creates the subgraph g
#that corresponds to a cluster. so it is ready for the Cost functions!
def cluster_to_subgraph_f(GG,cluster,comP):
	G = GG
	cl = cluster[:]
	l = []
	for i in cl: #3ades-2ades
		l.append((i[0],i[1]))
	#comP = point_to_node(centerofmass(cl),l) #finds comP
	#returns all the nodes 
	l_null = []
	s = []
	for node in l:
		s = nx.dijkstra_path(G,comP,node)[:]
		if comP in s:
			s.remove(comP)
		if node in s:
			s.remove(node)
		for n in s:
			if n not in l_null:
				l_null.append(n)
		s = []
	cluster_nodes = l[:]
	for i in l_null:
		cluster_nodes.append(i)
	g = G.subgraph(cluster_nodes)
	return [g,comP]


#give the attributes to subtrees
def att_to_subtrees(gg,qq):
	q = qq[:]
	sub_list = []
	for i in range(len(q)):
		graph = q[i]
		for ee in graph.edges():
			if (ee[0],ee[1]) in gg:
				graph.add_edge(ee[0],ee[1], weight = gg.edge[ee[0]][ee[1]]['weight'])
			if (ee[1],ee[0]) in gg:
				graph.add_edge(ee[0],ee[1], weight = gg.edge[ee[1]][ee[0]]['weight'])
			#graph.add_edge(ee[0],ee[1], efficiency = gg.edge[ee[0]][ee[1]]['efficiency'])
		for n in graph.nodes():
			graph.node[n] = G.node[n]
		sub_list.append(graph)
	return sub_list


#give the attributes to subtrees
def att_to_subtrees_efficiency(G,qq,gg):
	q = qq[:]
	sub_list = []
	for i in range(len(q)):
		graph = q[i]
		for ee in graph.edges():
			if (ee[0],ee[1]) in G:
				graph.add_edge(ee[0],ee[1], weight = G.edge[ee[0]][ee[1]]['weight'])
				graph.add_edge(ee[0],ee[1], efficiency = gg.edge[ee[0]][ee[1]]['efficiency'])
			if (ee[1],ee[0]) in G:
				graph.add_edge(ee[0],ee[1], weight = G.edge[ee[1]][ee[0]]['weight'])
				graph.add_edge(ee[0],ee[1], efficiency = gg.edge[ee[1]][ee[0]]['efficiency'])
		for n in graph.nodes():
			graph.node[n] = G.node[n]
		sub_list.append(graph)
	return sub_list


def aprims_mst(G, weight = 'weight', data = True):
	"""Edges in a minimum spanning forest of an undirected 
	"""
	if G.is_directed():
		raise nx.NetworkXError(
			"Mimimum spanning tree not defined for directed graphs.")
	nodes = G.nodes()
	e = []
	while nodes:
		u = nodes.pop(0)
		frontier = []
		visited = [u]
		for u, v in G.edges(u):
			heappush(frontier, (G[u][v].get(weight, 1), u, v))
		while frontier:
			W, u, v = heappop(frontier)
			if v in visited:
				continue
			visited.append(v)
			nodes.remove(v)
			e.append((u,v))
			for v, w  in G.edges(v):
				if not w in visited:
					heappush(frontier, (G[v][w].get(weight, 1), v, w))
	return e


#length of aprims_mst of a graph G;)
def alength_prims_mst(G):
	alpha = aprims_mst(G,'weight')
	s = 0
	for e in alpha:
		s = s + G[alpha[0][0]][alpha[0][1]]['weight']
	return s


#returns the total length of a graph G
def alength_graph(GG):
	G = GG
	s = 0
	alpha = G.edges()[:]
	for e in alpha:
		s = s + G[alpha[0][0]][alpha[0][1]]['weight']
	return s


def a_graph_efficiency(Gke,i_node,nu):
	G = Gke
	alpha = aprims_mst(G,'weight') #our spanning tree
	# define the mst graph
	GG=nx.Graph()
	#GG.add_edges_from(alpha)
	GG.add_nodes_from(G.nodes())
	#get node attributes info
	nx.set_node_attributes(GG,'population', nx.get_node_attributes(G,'population'))
	GG.add_edges_from(alpha)
	#give the weights
	for e in GG.edges():
		if e in G.edges():
			GG.add_edge(e[0],e[1],weight = G.edge[e[0]][e[1]]['weight'])
		if (e[1],e[0]) in G.edges():
			GG.add_edge(e[0],e[1],weight = G.edge[e[1]][e[0]]['weight'])
	#take all the sps from chosen init_node = 'O'
	init_node = i_node
	#to xreiazomaste k gia to cable cost!
	l = []
	for i in GG.nodes():
		if i != init_node:
			if nu == 0: #avoid null nodes!
				if GG.node[i]['population'] != -1: #avoid null nodes! (we can change it later and put 'population' =-1 and for the sum of loads if 'population' == -1 then 0 will be added to the sum)
					nL_ON = [] #first the nodes
					list_ON = nx.dijkstra_path(GG,init_node,i)[:]
					#now the edges of the path
					for ii in range(len(list_ON)-1):
						nL_ON.append((list_ON[ii],list_ON[ii+1]))
					l.append(nL_ON)
			if nu == 1: #accept all nodes!
				nL_ON = [] #first the nodes
				list_ON = nx.dijkstra_path(GG,init_node,i)[:]
				#now the edges of the path
				for ii in range(len(list_ON)-1):
					nL_ON.append((list_ON[ii],list_ON[ii+1]))
				l.append(nL_ON)
	#dimiourgoume lista pou periexei ola ta main paths! apo ton init_node
	list_all = []
	for k in range(len(GG.edges(init_node))):
		list_init = []
		for i in range(len(l)):
			for j in range(len(l[i])):
				if l[i][j][0] == init_node and l[i][j][1] == GG.edges(init_node)[k][1]:
					list_init.append(l[i])
		list_all.append(list_init)
	#sorted list_init
	lista_all = []
	for j in range(len(list_all)):
		lista_all.append(sorted(list_all[j]))
	#Given an INIT NODE 
	# ALL IN ONE STROKE!!!!!
	g= GG.nodes()
	g.remove(init_node)
	for iiii in g:
		#find subtrees of root
		root = iiii
		#search in main paths for root and returns the subtree of it
		#saves also the weight of its previous edge #! 
		root_list = []
		leafs_list = []
		previous_w = float(0)
		for i in range(len(lista_all)):
			for j in range(len(lista_all[i])):
				for k in range(len(lista_all[i][j])):
					if lista_all[i][j][k][0] == root:
						root_edge = lista_all[i][j][k-1] #i akmi tis opoias ypologizoume to edge_efficiency
						r_edge = root_edge #we use it later to define the efficiency
						for ii in range(lista_all[i][j].index(lista_all[i][j][k]),len(lista_all[i][j])):
							if lista_all[i][j][ii] not in root_list:
								root_list.append(lista_all[i][j][ii])
						previous_w = GG[lista_all[i][j][k-1][0]][lista_all[i][j][k-1][1]]['weight']
					if lista_all[i][j][len(lista_all[i][j])-1][1] == root: #leaf case
						root_edge_leaf = lista_all[i][j][len(lista_all[i][j])-1]
						leafs_list.append(root_edge_leaf)
		#to give the weight_info to an edge, we take the end node of it and compute the weight_of its subtree
		#and then add it to the weight of it
		#weight and load of the subtree (here weight is the distance between two consecutive nodes)
		subtree_w = float(0)
		load = float(0)
		load_list = []
		if root_list == []: #leaf case
			subtree_w = 0
			previous_w = GG[root_edge_leaf[0]][root_edge_leaf[1]]['weight']
			if GG.node[root_edge_leaf[0]]['population'] == -1: #dealing with null_nodes
				load = float(0 + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
			else:
				load = float(GG.node[root_edge_leaf[0]]['population'] + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
		else:
			for i in range(len(root_list)):
				try:
					subtree_w = subtree_w + GG[root_list[i][0]][root_list[i][1]]['weight']
				except:
					print root_list[i]
				if root_list[i][0] not in load_list:
					if GG.node[root_list[i][0]]['population'] != -1:
						load = load + GG.node[root_list[i][0]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][0])
				if root_list[i][1] not in load_list:
					if GG.node[root_list[i][1]]['population'] != -1:
						load = load + GG.node[root_list[i][1]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][1])
		total_w = previous_w + subtree_w
		total_load = load
		#edge_efficiency = total_load / total_w #people/meters
		if total_load != 0 :
			edge_efficiency = float(total_w) / total_load #meters/people
		else:
			edge_efficiency = 0
		#gives to the edge the edge_efficiency!!!
		GG[r_edge[0]][r_edge[1]]['efficiency'] = edge_efficiency
	null_list = []
	for jk in GG.nodes(): #creates a list with null nodes
		if GG.node[jk]['population'] == -1:
			null_list.append(jk)
	return [lista_all,GG,leafs_list,null_list]

#lista_all has all the paths from init node!!!
#leafs_list has all the leafs of the tree
#null_list has all the null_nodes



def a_graph_efficiency000(Gke,i_node,nu):
	G = Gke
	alpha = aprims_mst(G,'weight') #our spanning tree
	# define the mst graph
	GG=nx.Graph()
	#GG.add_edges_from(alpha)
	GG.add_nodes_from(G.nodes())
	#get node attributes info
	nx.set_node_attributes(GG,'population', nx.get_node_attributes(G,'population'))
	GG.add_edges_from(alpha)
	#give the weights
	for e in GG.edges():
		if e in G.edges():
			GG.add_edge(e[0],e[1],weight = G.edge[e[0]][e[1]]['weight'])
	#take all the sps from chosen init_node = 'O'
	init_node = i_node
	#to xreiazomaste k gia to cable cost!
	l = []
	for i in GG.nodes():
		if nu == 0: #avoid null nodes!
			if GG.node[i]['population'] != -1: #avoid null nodes! (we can change it later and put 'population' =-1 and for the sum of loads if 'population' == -1 then 0 will be added to the sum)
				nL_ON = [] #first the nodes
				list_ON = nx.dijkstra_path(GG,init_node,i)[:]
				#now the edges of the path
				for ii in range(len(list_ON)-1):
					nL_ON.append((list_ON[ii],list_ON[ii+1]))
				l.append(nL_ON)
		if nu == 1: #accept all nodes!
			nL_ON = [] #first the nodes
			list_ON = nx.dijkstra_path(GG,init_node,i)[:]
			#now the edges of the path
			for ii in range(len(list_ON)-1):
				nL_ON.append((list_ON[ii],list_ON[ii+1]))
			l.append(nL_ON)
	#dimiourgoume lista pou periexei ola ta main paths! apo ton init_node
	list_all = []
	for k in range(len(GG.edges(init_node))):
		list_init = []
		for i in range(len(l)):
			for j in range(len(l[i])):
				if l[i][j][0] == init_node and l[i][j][1] == GG.edges(init_node)[k][1]:
					list_init.append(l[i])
		list_all.append(list_init)
	#sorted list_init
	lista_all = []
	for j in range(len(list_all)):
		lista_all.append(sorted(list_all[j]))
	#Given an INIT NODE 
	# ALL IN ONE STROKE!!!!!
	g= GG.nodes()
	g.remove(init_node)
	for iiii in g:
		#find subtrees of root
		root = iiii
		#search in main paths for root and returns the subtree of it
		#saves also the weight of its previous edge #! 
		root_list = []
		leafs_list = []
		previous_w = float(0)
		for i in range(len(lista_all)):
			for j in range(len(lista_all[i])):
				for k in range(len(lista_all[i][j])):
					if lista_all[i][j][k][0] == root:
						root_edge = lista_all[i][j][k-1] #i akmi tis opoias ypologizoume to edge_efficiency
						r_edge = root_edge #we use it later to define the efficiency
						for ii in range(lista_all[i][j].index(lista_all[i][j][k]),len(lista_all[i][j])):
							if lista_all[i][j][ii] not in root_list:
								root_list.append(lista_all[i][j][ii])
						previous_w = GG[lista_all[i][j][k-1][0]][lista_all[i][j][k-1][1]]['weight']
					if lista_all[i][j][len(lista_all[i][j])-1][1] == root: #leaf case
						root_edge_leaf = lista_all[i][j][len(lista_all[i][j])-1]
						leafs_list.append(root_edge_leaf)
		#to give the weight_info to an edge, we take the end node of it and compute the weight_of its subtree
		#and then add it to the weight of it
		#weight and load of the subtree (here weight is the distance between two consecutive nodes)
		subtree_w = float(0)
		load = float(0)
		load_list = []
		if root_list == []: #leaf case
			subtree_w = 0
			previous_w = GG[root_edge_leaf[0]][root_edge_leaf[1]]['weight']
			if GG.node[root_edge_leaf[0]]['population'] == -1: #dealing with null_nodes
				load = float(0 + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
			else:
				load = float(GG.node[root_edge_leaf[0]]['population'] + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
		else:
			for i in range(len(root_list)):
				subtree_w = subtree_w + GG[root_list[i][0]][root_list[i][1]]['weight']
				if root_list[i][0] not in load_list:
					if GG.node[root_list[i][0]]['population'] != -1:
						load = load + GG.node[root_list[i][0]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][0])
				if root_list[i][1] not in load_list:
					if GG.node[root_list[i][1]]['population'] != -1:
						load = load + GG.node[root_list[i][1]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][1])
		total_w = previous_w + subtree_w
		total_load = load
		#edge_efficiency = total_load / total_w #people/meters
		edge_efficiency = float(total_w) / total_load #meters/people
		#gives to the edge the edge_efficiency!!!
		GG.edge[r_edge[0]][r_edge[1]]['efficiency'] = edge_efficiency
	null_list = []
	for jk in GG.nodes(): #creates a list with null nodes
		if GG.node[jk]['population'] == -1:
			null_list.append(jk)
	return [lista_all,GG,leafs_list,null_list]



#this also does the efficiency
def a_graph_efficiency0(Gmain,Gke,i_node,nu):
	G = Gke
	alpha = aprims_mst(G,'weight') #our spanning tree
	# define the mst graph
	GG=nx.Graph()
	#GG.add_edges_from(alpha)
	GG.add_nodes_from(G.nodes())
	#get node attributes info
	nx.set_node_attributes(GG,'population', nx.get_node_attributes(G,'population'))
	GG.add_edges_from(alpha)
	#give the weights
	for e in GG.edges():
		if e in G.edges():
			GG.add_edge(e[0],e[1],weight = G.edge[e[0]][e[1]]['weight'])
	#take all the sps from chosen init_node = 'O'
	init_node = i_node
	#to xreiazomaste k gia to cable cost!
	l = []
	for i in GG.nodes():
		if nu == 0: #avoid null nodes!
			if GG.node[i]['population'] != -1: #avoid null nodes! (we can change it later and put 'population' =-1 and for the sum of loads if 'population' == -1 then 0 will be added to the sum)
				nL_ON = [] #first the nodes
				list_ON = nx.dijkstra_path(Gmain,init_node,i)[:]
				#now the edges of the path
				for ii in range(len(list_ON)-1):
					nL_ON.append((list_ON[ii],list_ON[ii+1]))
				l.append(nL_ON)
		if nu == 1: #accept all nodes!
			nL_ON = [] #first the nodes
			list_ON = nx.dijkstra_path(Gmain,init_node,i)[:]
			#now the edges of the path
			for ii in range(len(list_ON)-1):
				nL_ON.append((list_ON[ii],list_ON[ii+1]))
			l.append(nL_ON)
	#dimiourgoume lista pou periexei ola ta main paths! apo ton init_node
	list_all = []
	for k in range(len(GG.edges(init_node))):
		list_init = []
		for i in range(len(l)):
			for j in range(len(l[i])):
				if l[i][j][0] == init_node and l[i][j][1] == GG.edges(init_node)[k][1]:
					list_init.append(l[i])
		list_all.append(list_init)
	#sorted list_init
	lista_all = []
	for j in range(len(list_all)):
		lista_all.append(sorted(list_all[j]))
	#Given an INIT NODE 
	# ALL IN ONE STROKE!!!!!
	g= GG.nodes()
	g.remove(init_node)
	root_edge_leaf = 0
	for iiii in g:
		#find subtrees of root
		root = iiii
		#search in main paths for root and returns the subtree of it
		#saves also the weight of its previous edge #! 
		root_list = []
		leafs_list = []
		previous_w = float(0)
		for i in range(len(lista_all)):
			for j in range(len(lista_all[i])):
				for k in range(len(lista_all[i][j])):
					if lista_all[i][j][k][0] == root:
						root_edge = lista_all[i][j][k-1] #i akmi tis opoias ypologizoume to edge_efficiency
						r_edge = root_edge #we use it later to define the efficiency
						for ii in range(lista_all[i][j].index(lista_all[i][j][k]),len(lista_all[i][j])):
							if lista_all[i][j][ii] not in root_list:
								root_list.append(lista_all[i][j][ii])
						if (lista_all[i][j][k-1][0], lista_all[i][j][k-1][1]) in GG.edges():
							previous_w = GG[lista_all[i][j][k-1][0]][lista_all[i][j][k-1][1]]['weight']
					if lista_all[i][j][len(lista_all[i][j])-1][1] == root: #leaf case
						root_edge_leaf = lista_all[i][j][len(lista_all[i][j])-1]
						leafs_list.append(root_edge_leaf)
		#to give the weight_info to an edge, we take the end node of it and compute the weight_of its subtree
		#and then add it to the weight of it
		#weight and load of the subtree (here weight is the distance between two consecutive nodes)
		subtree_w = float(0)
		load = float(0)
		load_list = []
		if root_list == []: #leaf case
			subtree_w = 0
			if (root_edge_leaf[0],root_edge_leaf[1]) in GG.edges():
				previous_w = GG[root_edge_leaf[0]][root_edge_leaf[1]]['weight']
			if GG.node[root_edge_leaf[0]]['population'] == -1: #dealing with null_nodes
				load = float(0 + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
			else:
				load = float(GG.node[root_edge_leaf[0]]['population'] + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
		else:
			for i in range(len(root_list)):
				subtree_w = subtree_w + GG[root_list[i][0]][root_list[i][1]]['weight']
				if root_list[i][0] not in load_list:
					if GG.node[root_list[i][0]]['population'] != -1:
						load = load + GG.node[root_list[i][0]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][0])
				if root_list[i][1] not in load_list:
					if GG.node[root_list[i][1]]['population'] != -1:
						load = load + GG.node[root_list[i][1]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][1])
		total_w = previous_w + subtree_w
		total_load = load
		#edge_efficiency = total_load / total_w #people/meters
		if total_load != 0:
			edge_efficiency = float(total_w) / total_load #meters/people
		#gives to the edge the edge_efficiency!!!
		GG.edge[r_edge[0]][r_edge[1]]['efficiency'] = edge_efficiency
	null_list = []
	for jk in G.nodes(): #creates a list with null nodes
		if G.node[jk]['population'] == -1:
			null_list.append(jk)
	return [lista_all,GG,leafs_list,null_list]

#lista_all has all the paths from init node!!!
#leafs_list has all the leafs of the tree
#null_list has all the null_nodes




#without efficiency
def a_graph_efficiency8(Gmain,Gke,GG,i_node):
	G = Gke
	#alpha = mst[:]
	# define the mst graph
	#GG=nx.Graph()
	##GG.add_edges_from(alpha)
	#GG.add_nodes_from(G.nodes())
	##get node attributes info
	#nx.set_node_attributes(GG,'population', nx.get_node_attributes(G,'population'))
	#GG.add_edges_from(alpha)
	#give the weights
	#for e in GG.edges():
	#	if e in G.edges():
	#		GG.add_edge(e[0],e[1],weight = G.edge[e[0]][e[1]]['weight'])
	#take all the sps from chosen init_node = 'O'
	init_node = i_node
	#to xreiazomaste k gia to cable cost!
	l = []
	for i in GG.nodes():
		nL_ON = [] #first the nodes
		list_ON = []
		if init_node != i:
			list_ON = nx.dijkstra_path(Gmain,init_node,i)[:]
		#now the edges of the path
		for ii in range(len(list_ON)-1):
			nL_ON.append((list_ON[ii],list_ON[ii+1]))
		l.append(nL_ON)
	#dimiourgoume lista pou periexei ola ta main paths! apo ton init_node
	list_all = []
	for k in range(len(GG.edges(init_node))):
		list_init = []
		for i in range(len(l)):
			for j in range(len(l[i])):
				if l[i][j][0] == init_node and l[i][j][1] == GG.edges(init_node)[k][1]:
					list_init.append(l[i])
		list_all.append(list_init)
	#sorted list_init
	lista_all = []
	for j in range(len(list_all)):
		lista_all.append(sorted(list_all[j]))
	#Given an INIT NODE 
	# ALL IN ONE STROKE!!!!!
	g= GG.nodes()
	g.remove(init_node)
	for iiii in g:
		#find subtrees of root
		root = iiii
		#search in main paths for root and returns the subtree of it
		#saves also the weight of its previous edge #! 
		root_list = []
		leafs_list = []
		previous_w = float(0)
		for i in range(len(lista_all)):
			for j in range(len(lista_all[i])):
				for k in range(len(lista_all[i][j])):
					if lista_all[i][j][k][0] == root:
						root_edge = lista_all[i][j][k-1] #i akmi tis opoias ypologizoume to edge_efficiency
						r_edge = root_edge #we use it later to define the efficiency
						for ii in range(lista_all[i][j].index(lista_all[i][j][k]),len(lista_all[i][j])):
							if lista_all[i][j][ii] not in root_list:
								root_list.append(lista_all[i][j][ii])
						if (lista_all[i][j][k-1][0], lista_all[i][j][k-1][1]) in GG.edges():
							previous_w = GG[lista_all[i][j][k-1][0]][lista_all[i][j][k-1][1]]['weight']
					if lista_all[i][j][len(lista_all[i][j])-1][1] == root: #leaf case
						root_edge_leaf = lista_all[i][j][len(lista_all[i][j])-1]
						leafs_list.append(root_edge_leaf)
	null_list = []
	for jk in GG.nodes(): #creates a list with null nodes
		if GG.node[jk]['population'] == -1:
			null_list.append(jk)
	return [lista_all,GG,leafs_list,null_list]


#l, gg, leafs, null_l = a_graph_efficiency8(G,G,g_dhn,comP_dhns)

#V_one_min
#after clustering it starts to fill in clusters 1 by 1 not closer to max (min->full)
def a_emCOa_2nd_G(GG,k_init,about_coms,about_minmax,num_it):
	"""
	1st var: Set of Points to be Clustered
				1 := All Mean Points of Larissa
				0 := cluster0 points
	2nd var: #Clusters
	3rd var: n \in {1,2,3,4}. corresponds to which function we will use to 
				initialize tha coms for the em-clustering
				1 := rancom_points
				2 := rancom_points_half
				3 := rancom_points_tenth
				4 := rancom_points_20th
	4th var: 1 := fill in em_clustering from minimum som
				2 := fill in em_clustering from maximum som
	5th var: # iterations of clustering to stabilize the coms 
	"""
	G = GG
	#create the two initial sets of Points. The one has Points with 0 mass
	X_minus = []
	X_plus = []
	i = 0 #seperates the input Points to 2 sets.
	P_init0 = graph_c_vec(G)[:] #P_init0 = graph_c_vec(g)[:]
	while i < len(P_init0):
		if P_init0[i][2] == 0:
			X_minus.append(P_init0[i])
			i = i + 1
		else:
			X_plus.append(P_init0[i])
			i = i +1
	P_init = X_plus[:]
	P0 = P_init[:]
	k0 = k_init
	NumClusters = 0
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	P00 = P_init[:] #Points, input for clustering
	kk = k_init  # #Clusters, input for clustering
	Cmin = [0]
	comP = centerofmass0(G,P_init) #comP = centerofmass0(g,P_init)
	while len(Call) != k0:
		#clustering
		if about_coms == -1:
			alphagco = a_emsp_b(g,kk,0)[:] 
			cls = alphagco[:]
			error_nodes_list = normalize_error_nodes(G,g,alphagco)[:]
			cls0 = norm_error_nodes(G,g,cls,error_nodes_list)
			plist = []
			for c in cls0:
				plist.append(centerofmass(c))
			C = akcom0(P00,plist,kk,num_it)
		if about_coms == 0:
			C = akcom0(P00,ran_points(P00,kk),kk,num_it)
		if about_coms == 1:
			C = akcom0(P00,rancom_points(P00,kk),kk,num_it)
		if about_coms == 2:
			C = akcom0(P00,rancom_points_half(P00,kk),kk,num_it)
		if about_coms == 3:
			C = akcom0(P00,rancom_points_tenth(P00,kk),kk,num_it)
		if about_coms == 4:
			C = akcom0(P00,rancom_points_20th(P00,kk),kk,num_it)
		k = kk
		cl_sorted = [] #creates empty sorted clusters
		for i in range(k): #creates k-clusters
			cl_sorted.insert(0,[])
		for i in range(k): #initializing cl_sorted
			cl_sorted[i] = C[0][1][i]
		CS = cl_sorted
		CS_sorted = []
		for i in range(k):
			dis_l = []
			for j in range(len(CS[i])):
				x = CS[i][j] #choose a point from S
				dis_l.append([x,adistance(x,C[0][0][i])])
				from operator import itemgetter, attrgetter
				sorted_dis_l = sorted(dis_l, key=itemgetter(1))
			CS_sorted.append(sorted_dis_l)
		#creates a list with the lmnts according to the load of coms
		C_w = []
		for i in range(k):
			x_out = []
			C_weighted = []
			for j in range(len(CS_sorted[i])):
				x = CS_sorted[i][j]
				if sumofmass(C_weighted) + x[0][2] <= cluster_plith_max:
					C_weighted.append(x[0])
			C_w.append(C_weighted)
		#checks if there are clusters with som < max_plith
		Cmin = []
		for i in range(k):
			if sumofmass(C_w[i]) < max_plith:
				Cmin.append(C_w[i])
		if len(Cmin) == 0:
			for i in range(len(C_w)):
				Call.append(C_w[i])
			break
		else:
			#the set of lmnts of clusters with som < max_plith
			#put Cmins in a row ... depending on their som
			dis_Cmin = []
			for i in range(len(Cmin)):
				dis_Cmin.append([sumofmass(Cmin[i]),Cmin[i]])
			from operator import itemgetter, attrgetter
			sorted_Cmin = sorted(dis_Cmin, key=itemgetter(0))
			#create the list with the clusters from minimum som to maximum
			#so the filling up will start from clusters with minimum som
			if about_minmax == 1:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
			##the previous list but from maximum som to minimum
			if about_minmax == 2:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
				Llist = []
				for i in range(len(Cminn)):
					Llist.append(Cminn[len(Cminn)-i-1])
				Cminn = Llist[:]
			#filling clusters with max em distance from comP
			if about_minmax == 0:
				Cminn = []
				aman1 = []
				for i in range(len(sorted_Cmin)):
					aman1.append(sorted_Cmin[i][1]) 
				###################################################################
				alphagco = []
				for cl in aman1:
					cl_list = []
					for i in cl:
						cl_list.append([i[0],i[1]])
					alphagco.append(cl_list)
				cls = alphagco[:]
				#error_nodes_list = normalize_error_nodes(G,g,alphagco)[:] #0
				#cls0 = norm_error_nodes(G,g,cls,error_nodes_list) 
				###################################################################
				coms_list = []
				for c in cls:
					coms_list.append(centerofmass(c))
				sp_list = []
				for i in coms_list:
					#sp_list.append([i,nx.dijkstra_path_length(G, centerofmass_graph0(G), i) ])
					sp_list.append([i,adistance(centerofmass_graph0(G), i) ])
				from operator import itemgetter, attrgetter
				sorted_sp_list = sorted(sp_list, key=itemgetter(1))
				cls0 = cls[coms_list.index(sorted_sp_list[len(cls)-1][0])]
				#creates nodes from cluster
				l_nodes = [] 
				#for i in aman1[0]: #we take each time the 1st cluster of em-clustering
				for i in cls0:
					l_nodes.append((i[0],i[1],G.node[(i[0],i[1])]['population']))
				Cminn.append(l_nodes)
			###
			Cminset = Cminn[0]
			#update P0 according to new Cminset
			for i in range(len(Cminset)):
				if Cminset[i] in P0: 
					P0.remove(Cminset[i])
			##fill in the clusters with som < cluster_plith_max
			Cmin00 = Cminn[0]
			coms_l_C_w  = centerofmass0(G,Cmin00)
			dis_l_xw = []
			i = 0
			listt = []
			while i < len(P0):
				xw = P0[i] #choose a point from P0[i]
				dis_l_xw.append([adistance(xw,coms_l_C_w), xw])
				i = i+1
			from operator import itemgetter, attrgetter
			dis_l_xw_sorted = sorted(dis_l_xw, key=itemgetter(0))
			for i in range(len(dis_l_xw_sorted)):
				xw = dis_l_xw_sorted[i][1]
				if sumofmass(Cmin00) + xw[2] <= cluster_plith_max:
					Cmin00.append(xw) #upgrade Cmin00
					P0.remove(xw) #upgrade P0 
					coms_l_C_w = centerofmass0(G,Cmin00)
				else:
					break
			Call.append(Cmin00)
			NumClusters = NumClusters + 1
			if NumClusters == k0-1:
				Call.append(P0)
				break
			P00 = P0[:] #update P00 for the next clustering
			kk = k - 1
	coms_l_Call = [] #update the coms
	for i in range(len(Call)): 
		coms_l_Call.append(centerofmass0(G,Call[i]))
	i = 0
	dis_l_X_minus = []
	dis_l_X_minus_sorted = []
	while i < len(X_minus):
		xw = X_minus[i] #choose a point from X_minus[i]
		for j in range(len(coms_l_Call)):
			dis_l_X_minus.append([adistance(xw,coms_l_Call[j]), j])
		from operator import itemgetter, attrgetter
		dis_l_X_minus_sorted = sorted(dis_l_X_minus, key=itemgetter(0))
		Call[dis_l_X_minus_sorted[0][1]].append(xw)
		dis_l_X_minus = []
		dis_l_X_minus_sorted = []
		i = i + 1
	coms_l_Call = [] 
	i = 0
	for i in range(len(Call)):
		coms_l_Call.append(centerofmass0(G,Call[i]))
	import os 
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 1, 391.995))
	return [Call,coms_l_Call,max_plith]

##############################################################################

#V_one_min
#after clustering it starts to fill in clusters 1 by 1 not closer to max (min->full)
def a_emCOa_2nd_Gg(G,g,k_init,about_coms,about_minmax,num_it):
	"""
	1st var: Set of Points to be Clustered
				1 := All Mean Points of Larissa
				0 := cluster0 points
	2nd var: #Clusters
	3rd var: n \in {1,2,3,4}. corresponds to which function we will use to 
				initialize tha coms for the em-clustering
				1 := rancom_points
				2 := rancom_points_half
				3 := rancom_points_tenth
				4 := rancom_points_20th
	4th var: 1 := fill in em_clustering from minimum som
				2 := fill in em_clustering from maximum som
	5th var: # iterations of clustering to stabilize the coms 
	"""
	#create the two initial sets of Points. The one has Points with 0 mass
	X_minus = []
	X_plus = []
	i = 0 #seperates the input Points to 2 sets.
	P_init0 = graph_c_vec(g)[:] 
	while i < len(P_init0):
		if P_init0[i][2] == 0:
			X_minus.append(P_init0[i])
			i = i + 1
		else:
			X_plus.append(P_init0[i])
			i = i +1
	P_init = X_plus[:]
	P0 = P_init[:]
	k0 = k_init
	NumClusters = 0
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	P00 = P_init[:] #Points, input for clustering
	kk = k_init  # #Clusters, input for clustering
	Cmin = [0]
	comP = centerofmass0(g,P_init) #comP = centerofmass0(g,P_init)
	while len(Call) != k0:
		#clustering
		if about_coms == -1:
			alphagco = a_emsp_b(g,kk,1)[:] 
			#alphagco = a_emsp_b_inb(G,kk)[:] #some probles to fix
			cls = alphagco[:]
			error_nodes_list = normalize_error_nodes(G,g,alphagco)[:]
			cls0 = norm_error_nodes(G,g,cls,error_nodes_list)
			plist = []
			for c in cls0:
				plist.append(centerofmass(c))
			C = akcom0(P00,plist,kk,num_it)
		if about_coms == 0:
			C = akcom0(P00,ran_points(P00,kk),kk,num_it)
		if about_coms == 1:
			C = akcom0(P00,rancom_points(P00,kk),kk,num_it)
		if about_coms == 2:
			C = akcom0(P00,rancom_points_half(P00,kk),kk,num_it)
		if about_coms == 3:
			C = akcom0(P00,rancom_points_tenth(P00,kk),kk,num_it)
		if about_coms == 4:
			C = akcom0(P00,rancom_points_20th(P00,kk),kk,num_it)
		k = kk
		cl_sorted = [] #creates empty sorted clusters
		for i in range(k): #creates k-clusters
			cl_sorted.insert(0,[])
		for i in range(k): #initializing cl_sorted
			cl_sorted[i] = C[0][1][i]
		CS = cl_sorted
		CS_sorted = []
		for i in range(k):
			dis_l = []
			for j in range(len(CS[i])):
				x = CS[i][j] #choose a point from S
				dis_l.append([x,adistance(x,C[0][0][i])])
				from operator import itemgetter, attrgetter
				sorted_dis_l = sorted(dis_l, key=itemgetter(1))
			CS_sorted.append(sorted_dis_l)
		#creates a list with the lmnts according to the load of coms
		C_w = []
		for i in range(k):
			x_out = []
			C_weighted = []
			for j in range(len(CS_sorted[i])):
				x = CS_sorted[i][j]
				if sumofmass(C_weighted) + x[0][2] <= cluster_plith_max:
					C_weighted.append(x[0])
			C_w.append(C_weighted)
		#checks if there are clusters with som < max_plith
		Cmin = []
		for i in range(k):
			if sumofmass(C_w[i]) < max_plith:
				Cmin.append(C_w[i])
		if len(Cmin) == 0:
			for i in range(len(C_w)):
				Call.append(C_w[i])
			break
		else:
			#the set of lmnts of clusters with som < max_plith
			#put Cmins in a row ... depending on their som
			dis_Cmin = []
			for i in range(len(Cmin)):
				dis_Cmin.append([sumofmass(Cmin[i]),Cmin[i]])
			from operator import itemgetter, attrgetter
			sorted_Cmin = sorted(dis_Cmin, key=itemgetter(0))
			#create the list with the clusters from minimum som to maximum
			#so the filling up will start from clusters with minimum som
			if about_minmax == 1:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
			##the previous list but from maximum som to minimum
			if about_minmax == 2:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
				Llist = []
				for i in range(len(Cminn)):
					Llist.append(Cminn[len(Cminn)-i-1])
				Cminn = Llist[:]
			#filling clusters with max em distance from comP
			if about_minmax == 0:
				Cminn = []
				aman1 = []
				for i in range(len(sorted_Cmin)):
					aman1.append(sorted_Cmin[i][1]) 
				###################################################################
				alphagco = []
				for cl in aman1:
					cl_list = []
					for i in cl:
						cl_list.append([i[0],i[1]])
					alphagco.append(cl_list)
				cls = alphagco[:]
				#error_nodes_list = normalize_error_nodes(G,g,alphagco)[:] #0
				#cls0 = norm_error_nodes(G,g,cls,error_nodes_list) 
				###################################################################
				coms_list = []
				for c in cls:
					coms_list.append(centerofmass(c))
				sp_list = []
				for i in coms_list:
					#sp_list.append([i,nx.dijkstra_path_length(G, centerofmass_graph0(G), i) ])
					sp_list.append([i,adistance(centerofmass_graph0(g), i) ])
				from operator import itemgetter, attrgetter
				sorted_sp_list = sorted(sp_list, key=itemgetter(1))
				cls0 = cls[coms_list.index(sorted_sp_list[len(cls)-1][0])]
				#creates nodes from cluster
				l_nodes = [] 
				#for i in aman1[0]: #we take each time the 1st cluster of em-clustering
				for i in cls0:
					l_nodes.append((i[0],i[1],g.node[(i[0],i[1])]['population'])) #g instead of G
				Cminn.append(l_nodes)
			###
			Cminset = Cminn[0]
			#update P0 according to new Cminset
			for i in range(len(Cminset)):
				if Cminset[i] in P0: 
					P0.remove(Cminset[i])
			##fill in the clusters with som < cluster_plith_max
			Cmin00 = Cminn[0]
			coms_l_C_w  = centerofmass0(g,Cmin00)
			dis_l_xw = []
			i = 0
			listt = []
			while i < len(P0):
				xw = P0[i] #choose a point from P0[i]
				dis_l_xw.append([adistance(xw,coms_l_C_w), xw])
				i = i+1
			from operator import itemgetter, attrgetter
			dis_l_xw_sorted = sorted(dis_l_xw, key=itemgetter(0))
			for i in range(len(dis_l_xw_sorted)):
				xw = dis_l_xw_sorted[i][1]
				if sumofmass(Cmin00) + xw[2] <= cluster_plith_max:
					Cmin00.append(xw) #upgrade Cmin00
					P0.remove(xw) #upgrade P0 
					coms_l_C_w = centerofmass0(g,Cmin00)
				else:
					break
			Call.append(Cmin00)
			NumClusters = NumClusters + 1
			if NumClusters == k0-1:
				Call.append(P0)
				break
			P00 = P0[:] #update P00 for the next clustering
			kk = k - 1
	coms_l_Call = [] #update the coms
	for i in range(len(Call)): 
		coms_l_Call.append(centerofmass0(g,Call[i]))
	i = 0
	dis_l_X_minus = []
	dis_l_X_minus_sorted = []
	while i < len(X_minus):
		xw = X_minus[i] #choose a point from X_minus[i]
		for j in range(len(coms_l_Call)):
			dis_l_X_minus.append([adistance(xw,coms_l_Call[j]), j])
		from operator import itemgetter, attrgetter
		dis_l_X_minus_sorted = sorted(dis_l_X_minus, key=itemgetter(0))
		Call[dis_l_X_minus_sorted[0][1]].append(xw)
		dis_l_X_minus = []
		dis_l_X_minus_sorted = []
		i = i + 1
	coms_l_Call = [] 
	i = 0
	for i in range(len(Call)):
		coms_l_Call.append(centerofmass0(g,Call[i]))
	import os 
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 1, 391.995))
	return [Call,coms_l_Call,max_plith]


##############################################################################


def a_COa_2ndV2(GG,k_init,about_coms,about_minmax,num_it):
	"""
	1st var: Set of Points to be Clustered
				1 := All Mean Points of Larissa
				0 := cluster0 points
	2nd var: #Clusters
	3rd var: n \in {1,2,3,4}. corresponds to which function we will use to 
				initialize tha coms for the em-clustering
				1 := rancom_points
				2 := rancom_points_half
				3 := rancom_points_tenth
				4 := rancom_points_20th
	4th var: 1 := fill in  from minimum som
				2 := fill in  from maximum som
	5th var: # iterations of clustering to stabilize the coms 
	"""
	G = GG
	#create the two initial sets of Points. The one has Points with 0 mass
	X_minus = []
	X_plus = []
	i = 0 #seperates the input Points to 2 sets. 
	P_init0 = graph_c_vec(G)[:]
	while i < len(P_init0):
		if P_init0[i][2] == 0:
			X_minus.append(P_init0[i])
			i = i + 1
		else:
			X_plus.append(P_init0[i])
			i = i +1
	P_init = X_plus[:] #29720
	#P_init_subG = G.subgraph(P_init) #subgraph of G
	P0 = P_init[:]
	#P0_subG = P_init_subG
	k0 = k_init
	NumClusters = 0
	#finds the max_plith per cluster
	#P_plith = sumofmass(P_init) #global
	P_plith = sumofmass(P_init0) #som of v_vec
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	P00 = P_init[:] #Points, input for clustering
	kk = k_init  # #Clusters, input for clustering
	Cmin = [0]
	comP = (point_to_node(centerofmass0(G,P_init),P00)[0],point_to_node(centerofmass0(G,P_init),P00)[1])
	while len(Call) != k0:
		#clustering
		if about_coms == 0:
			C = akcom00(P00,ran_points(P00,kk),kk,num_it)
		if about_coms == 1:
			C = akcom0(P00,rancom_points(P00,kk),kk,num_it)
		if about_coms == 2:
			C = akcom0(P00,rancom_points_half(P00,kk),kk,num_it)
		if about_coms == 3:
			C = akcom0(P00,rancom_points_tenth(P00,kk),kk,num_it)
		if about_coms == 4:
			C = akcom0(P00,rancom_points_20th(P00,kk),kk,num_it)
		k = kk
		cl_sorted = [] #creates empty sorted clusters
		for i in range(k): #creates k-clusters
			cl_sorted.insert(0,[])
		for i in range(k): #initializing cl_sorted
			cl_sorted[i] = C[0][1][i]
		CS = cl_sorted
		CS_sorted = []
		for i in range(k):
			dis_l = []
			sorted_dis_l = []
			cs = CS[i][:]
			ccs = [] #change to (,)
			for j in cs:
				ccs.append((j[0],j[1]))
			#cs = ccs[:]
			Gsub = G.subgraph(ccs)
			s=[]
			s=nx.single_source_dijkstra_path_length(G, (C[0][0][i][0],C[0][0][i][1]))
			for v in list(s):
				if v in Gsub.nodes():
					dis_l.append([v[0],v[1],s.get(v)])
			from operator import itemgetter, attrgetter
			sorted_dis_l = sorted(dis_l, key=itemgetter(2))[:]
			CS_sorted.append(sorted_dis_l)
		#creates a list with the lmnts according to the load of coms
		C_w = []
		for i in range(k):
			x_out = []
			C_weighted = []
			for j in range(len(CS_sorted[i])):
				y = (CS_sorted[i][j][0],CS_sorted[i][j][1])
				x = [y[0],y[1],G.node[(y[0],y[1])]['population']]
				if sumofmass(C_weighted) + x[2] <= cluster_plith_max:
					C_weighted.append(x)
			C_w.append(C_weighted)
		#checks if there are clusters with som < max_plith
		Cmin = []
		for i in range(k):
			if sumofmass(C_w[i]) < max_plith:
				Cmin.append(C_w[i])
		if len(Cmin) == 0:
			for i in range(len(C_w)):
				Call.append(C_w[i])
			break
		else:
			#the set of lmnts of clusters with som < max_plith
			#put Cmins in a row ... depending on their som
			dis_Cmin = []
			for i in range(len(Cmin)):
				dis_Cmin.append([sumofmass(Cmin[i]),Cmin[i]])
			from operator import itemgetter, attrgetter
			sorted_Cmin = sorted(dis_Cmin, key=itemgetter(0))
			#create the list with the clusters from minimum som to maximum
			#so the filling up will start from clusters with minimum som
			if about_minmax == 1:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
			##the previous list but from maximum som to minimum
			if about_minmax == 2:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
				Llist = []
				for i in range(len(Cminn)):
					Llist.append(Cminn[len(Cminn)-i-1])
				Cminn = Llist[:]
			Cminset = Cminn[0][:]
			#update P0 according to new Cminset
			for i in range(len(Cminset)):
				if Cminset[i] in P0: 
					P0.remove(Cminset[i])
			##fill in the clusters with som < cluster_plith_max
			Cmin00 = Cminn[0][:]
			coms_l_C_w  = centerofmass(Cmin00)
			dis_l_xw = []
			ccs = [] #change to (,)
			for j in P0:
				ccs.append((j[0],j[1]))
			#cs = ccs[:]
			Gsub = G.subgraph(ccs)
			s=[]
			s=nx.single_source_dijkstra_path_length(G, coms_l_C_w)
			for v in list(s):
				if v in Gsub.nodes():
					dis_l_xw.append([v[0],v[1],s.get(v)]) #
			from operator import itemgetter, attrgetter
			dis_l_xw_sorted = sorted(dis_l_xw, key=itemgetter(2))[:]
			for i in range(len(dis_l_xw_sorted)):
				y = (dis_l_xw_sorted[i][0],dis_l_xw_sorted[i][1])
				xw = [y[0],y[1],G.node[(y[0],y[1])]['population']]
				if sumofmass(Cmin00) + xw[2] <= cluster_plith_max:
					Cmin00.append(xw) #upgrade Cmin00
					if xw in P0: 
						P0.remove(xw) #upgrade P0 
					coms_l_C_w = centerofmass(Cmin00)
				else:
					break
			Call.append(Cmin00)
			NumClusters = NumClusters + 1
			if NumClusters == k0-1:
				Call.append(P0)
				break
			P00 = P0[:] #update P00 for the next clustering
			kk = k - 1
	coms_l_Call = [] #update the coms
	for i in range(len(Call)): 
		coms_l_Call.append(centerofmass(Call[i]))
	iii = 0
	dis_l_X_minus = []
	dis_l_X_minus_sorted = []
	while iii < len(X_minus):
		y = X_minus[iii] #choose a point from X_minus[i]
		xw = (y[0],y[1])
		for j in range(len(coms_l_Call)):
			dis_l_X_minus.append([nx.dijkstra_path_length(G, source=xw, target=coms_l_Call[j]), j])
		from operator import itemgetter, attrgetter
		dis_l_X_minus_sorted = sorted(dis_l_X_minus, key=itemgetter(0))
		Call[dis_l_X_minus_sorted[0][1]].append(xw)
		dis_l_X_minus = []
		dis_l_X_minus_sorted = []
		iii = iii + 1
	#coms_l_Call = [] 
	#i = 0
	#for i in range(len(Call)):
	#	coms_l_Call.append(centerofmass(Call[i]))
	import os 
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 5, 391.995))
	return [Call,coms_l_Call]

#aman = a_COa_2ndV2(G, 2, 4, 1, 50)

#V_one_min 
# 1230m51.069s for 6 clusters to 1
#after clustering it starts to fill in clusters 1 by 1 not closer to max (min->full)
def a_COa_2ndV2_Gex1(GG,k_init,about_coms,about_minmax,num_it):
	"""
	1st var: Set of Points to be Clustered
				1 := All Mean Points of Larissa
				0 := cluster0 points
	2nd var: #Clusters
	3rd var: n \in {1,2,3,4}. corresponds to which function we will use to 
				initialize tha coms for the em-clustering
				1 := rancom_points
				2 := rancom_points_half
				3 := rancom_points_tenth
				4 := rancom_points_20th
	4th var: 1 := fill in  from minimum som
				2 := fill in  from maximum som
	5th var: # iterations of clustering to stabilize the coms 
	"""
	G = GG
	#create the two initial sets of Points. The one has Points with 0 mass
	X_minus = []
	X_plus = []
	i = 0 #seperates the input Points to 2 sets. 
	P_init0 = graph_c_vec(G)[:]
	while i < len(P_init0):
		if P_init0[i][2] == 0:
			X_minus.append(P_init0[i])
			i = i + 1
		else:
			X_plus.append(P_init0[i])
			i = i +1
	P_init = X_plus[:] #29720
	#P_init_subG = G.subgraph(P_init) #subgraph of G
	P0 = P_init[:]
	#P0_subG = P_init_subG
	k0 = k_init
	NumClusters = 0
	#finds the max_plith per cluster
	#P_plith = sumofmass(P_init) #global
	P_plith = sumofmass(P_init0) #som of v_vec
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	P00 = P_init[:] #Points, input for clustering
	kk = k_init  # #Clusters, input for clustering
	Cmin = [0]
	comP = (point_to_node(centerofmass0(G,P_init),P00)[0],point_to_node(centerofmass0(G,P_init),P00)[1])
	while len(Call) != k0:
		#clustering
		if about_coms == 0:
			C = akcom00(P00,ran_points(P00,kk),kk,num_it)
		if about_coms == 1:
			C = akcom0(P00,rancom_points(P00,kk),kk,num_it)
		if about_coms == 2:
			C = akcom0(P00,rancom_points_half(P00,kk),kk,num_it)
		if about_coms == 3:
			C = akcom0(P00,rancom_points_tenth(P00,kk),kk,num_it)
		if about_coms == 4:
			C = akcom0(P00,rancom_points_20th(P00,kk),kk,num_it)
		k = kk
		cl_sorted = [] #creates empty sorted clusters
		for i in range(k): #creates k-clusters
			cl_sorted.insert(0,[])
		for i in range(k): #initializing cl_sorted
			cl_sorted[i] = C[0][1][i]
		CS = cl_sorted
		CS_sorted = []
		for i in range(k):
			dis_l = []
			sorted_dis_l = []
			cs = CS[i][:]
			ccs = [] #change to (,)
			for j in cs:
				ccs.append((j[0],j[1]))
			#cs = ccs[:]
			Gsub = G.subgraph(ccs)
			s=[]
			s=nx.single_source_dijkstra_path_length(G, (C[0][0][i][0],C[0][0][i][1]))
			for v in list(s):
				if v in Gsub.nodes():
					dis_l.append([v[0],v[1],s.get(v)])
			from operator import itemgetter, attrgetter
			sorted_dis_l = sorted(dis_l, key=itemgetter(2))[:]
			CS_sorted.append(sorted_dis_l)
		#creates a list with the lmnts according to the load of coms
		C_w = []
		for i in range(k):
			x_out = []
			C_weighted = []
			for j in range(len(CS_sorted[i])):
				y = (CS_sorted[i][j][0],CS_sorted[i][j][1])
				x = [y[0],y[1],G.node[(y[0],y[1])]['population']]
				if sumofmass(C_weighted) + x[2] <= cluster_plith_max:
					C_weighted.append(x)
			C_w.append(C_weighted)
		#checks if there are clusters with som < max_plith
		Cmin = []
		for i in range(k):
			if sumofmass(C_w[i]) < max_plith:
				Cmin.append(C_w[i])
		if len(Cmin) == 0:
			for i in range(len(C_w)):
				Call.append(C_w[i])
			break
		else:
			#the set of lmnts of clusters with som < max_plith
			#put Cmins in a row ... depending on their som
			dis_Cmin = []
			for i in range(len(Cmin)):
				dis_Cmin.append([sumofmass(Cmin[i]),Cmin[i]])
			from operator import itemgetter, attrgetter
			sorted_Cmin = sorted(dis_Cmin, key=itemgetter(0))
			#create the list with the clusters from minimum som to maximum
			#so the filling up will start from clusters with minimum som
			if about_minmax == 1:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
			##the previous list but from maximum som to minimum
			if about_minmax == 2:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
				Llist = []
				for i in range(len(Cminn)):
					Llist.append(Cminn[len(Cminn)-i-1])
				Cminn = Llist[:]
			Cminset = Cminn[0][:]
			#update P0 according to new Cminset
			for i in range(len(Cminset)):
				if Cminset[i] in P0: 
					P0.remove(Cminset[i])
			##fill in the clusters with som < cluster_plith_max
			Cmin00 = Cminn[0][:]
			coms_l_C_w  = centerofmass(Cmin00)
			dis_l_xw = []
			ccs = [] #change to (,)
			for j in P0:
				ccs.append((j[0],j[1]))
			#cs = ccs[:]
			Gsub = G.subgraph(ccs)
			s=[]
			s=nx.single_source_dijkstra_path_length(G, coms_l_C_w)
			for v in list(s):
				if v in Gsub.nodes():
					dis_l_xw.append([v[0],v[1],s.get(v)]) #
			from operator import itemgetter, attrgetter
			dis_l_xw_sorted = sorted(dis_l_xw, key=itemgetter(2))[:]
			for i in range(len(dis_l_xw_sorted)):
				y = (dis_l_xw_sorted[i][0],dis_l_xw_sorted[i][1])
				xw = [y[0],y[1],G.node[(y[0],y[1])]['population']]
				if sumofmass(Cmin00) + xw[2] <= cluster_plith_max:
					Cmin00.append(xw) #upgrade Cmin00
					if xw in P0: 
						P0.remove(xw) #upgrade P0 
					coms_l_C_w = centerofmass(Cmin00)
				else:
					break
			Call.append(Cmin00)
			NumClusters = NumClusters + 1
			if NumClusters == k0-1:
				Call.append(P0)
				break
			P00 = P0[:] #update P00 for the next clustering
			kk = k - 1
	coms_l_Call = [] #update the coms
	for i in range(len(Call)): 
		coms_l_Call.append(centerofmass(Call[i]))
	iii = 0
	dis_l_X_minus = []
	dis_l_X_minus_sorted = []
	while iii < len(X_minus):
		y = X_minus[iii] #choose a point from X_minus[i]
		xw = (y[0],y[1])
		for j in range(len(coms_l_Call)):
			dis_l_X_minus.append([nx.dijkstra_path_length(G, source=xw, target=coms_l_Call[j]), j])
		from operator import itemgetter, attrgetter
		dis_l_X_minus_sorted = sorted(dis_l_X_minus, key=itemgetter(0))
		Call[dis_l_X_minus_sorted[0][1]].append(xw)
		dis_l_X_minus = []
		dis_l_X_minus_sorted = []
		iii = iii + 1
	#coms_l_Call = [] 
	#i = 0
	#for i in range(len(Call)):
	#	coms_l_Call.append(centerofmass(Call[i]))
	import os 
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 5, 391.995))
	return [Call,coms_l_Call]


def mst_to_graph(GG,listt):
	G = GG
	g=nx.Graph() #g is the mst graph
	alpha = listt[:]
	g.add_edges_from(alpha)
	#get node attributes info
	nx.set_node_attributes(g,'population', nx.get_node_attributes(G,'population'))
	#give the weights
	for e in g.edges():
		g.add_edge(e[0],e[1],weight = G.edge[e[0]][e[1]]['weight'])
		#g.add_edge(e[0],e[1], Wkt = G.edge[e[0]][e[1]]['Wkt'])
	return g

###############################################################################








###############################################################################

#makes All the main paths of init_node, directed graphs
#actually creates a tree with root the init_node and the main paths are its 
#subtrees
def a_di_main_paths(DDD,L):
	G = DDD
	l = L[:]
	subtrees = []
	lll = []
	subgraphs = []
	for i in range(len(l)): #computes the subtrees
		sub = []
		for j in range(len(l[i])):
			path = l[i][j][:]
			for k in range(len(path)):
				e = path[k][:]
				if e not in sub:
					sub.append(e)
		subtrees.append(sub)
	list_node = [] # to define the K.graph we want the nodes of it
	for jj in range(len(subtrees)):
		path = subtrees[jj][:]
		list_node = []
		for k in range(len(path)):
			e = path[k][:]
			if e[0] not in list_node:
				list_node.append(e[0])
			if e[1] not in list_node:
				list_node.append(e[1])
		lll.append(list_node) #define the main paths as directed subgraphs 
	for k in range(len(lll)):
		K = nx.DiGraph()
		K.add_nodes_from(lll[k])
		K.add_edges_from(subtrees[k])
		for n in K.nodes():
			K.node[n]['population'] = G.node[n]['population']
		for ee in K.edges():
			if (ee[0],ee[1]) in G.edges():
				K[ee[0]][ee[1]]['weight'] = G.edge[ee[0]][ee[1]]['weight']
			if (ee[1],ee[0]) in G.edges():
				K[ee[0]][ee[1]]['weight'] = G.edge[ee[1]][ee[0]]['weight']
		subgraphs.append(K)
	return subgraphs


#D = sub_list[2]


#returns the path of two nodes as a directed graph
#input is one of the subtrees
def path(DD,s_node,e_node):
	l = []
	for path in nx.all_simple_paths(DD, s_node, e_node):
		l = path
	e_list = []
	for i in range(len(l)-1):
		e_list.append((l[i],l[i+1]))
	d = nx.DiGraph()
	d.add_nodes_from(l)
	d.add_edges_from(e_list)
	graph = d
	for ee in graph.edges():
		if (ee[0],ee[1]) in DD.edges():
			graph[ee[0]][ee[1]]['weight'] = DD[ee[0]][ee[1]]['weight']
		if (ee[1],ee[0]) in DD.edges():
			graph[ee[0]][ee[1]]['weight'] = DD[ee[1]][ee[0]]['weight']
		#graph.add_edge(ee[0],ee[1], efficiency = D.edge[ee[0]][ee[1]]['efficiency'])
	for n in graph.nodes():
		graph.node[n] = DD.node[n]
	return [d,l,e_list]

def depth_node(DD,s_node,e_node):
	l = len(path(DD,s_node,e_node)[1])-1
	return l

#computes the length of the path from path()
def path_length(DD,snn,enn):
	dd = DD
	sn = snn
	en = enn
	graph,nodess,edgess = path(dd,sn,en)
	lt = 0
	for i in range(len(nodess)-1):
		if (nodess[i], nodess[i+1]) in graph.edges():
			lt = lt + graph[nodess[i]][nodess[i+1]]['weight']
	return float(lt)


#given a number and a list returns the next greater lmnt of the list, of that number
#number Must be not greater than the max lmnt of the list
def cap(mm,bb): 
	m = mm
	list_b = bb[:]
	d = 0
	for i in range(len(bb)):
		if m == bb[i]:
			return m
		else:
			d = bb[i]-m
			if d > 0:
				return bb[i]


#output is the number of kind of cables/tubes/subducts/ducts we need to use
def cap_gran(mm,bb):
	m = mm
	list_b = bb[:]
	mx = max(list_b)
	list_gran = []
	for iii in range(len(list_b)): #initializes list_gran := /
		list_gran.append(0)
	alpha = m/mx
	list_gran[list_b.index(mx)] = alpha
	beta = m%mx
	if len(list_b) > 1:
		mx_1 = list_b[list_b.index(mx) -1] #checks if beta is between last and previous lmnts of list
		if beta > mx_1:
			list_gran[list_b.index(mx)] = list_gran[list_b.index(mx)] + 1
		else:
			if beta != 0:
				list_gran[list_b.index(cap(beta,list_b))] = 1
			else:
				list_gran[list_b.index(cap(beta,list_b))] = 0
		return list_gran
	else:
		if beta == 0:
			return list_gran
		else:
			list_gran[0] = list_gran[0] + 1
			return list_gran


#from fibers/cables we go to cables/subducts. to compute this since here we have
#that cable/subduct 1/1 we have to add the lnts of cap_grans list
#to see how many subducts we want for the node we examine

#compute the cost of a given node according to gran tables
#not the cost actually, but what kind of gran we will use for it!
def cap_gran_cost(DD,cost_node):
	D = DD
	c_node = cost_node
	load_p = D.node[c_node]['population']
	#computing
	#the input list of the next cap_gran is the sum of the previous output of it
	cap_gran_list = []
	res_gran_list = []
	m = load_p #init time
	for i in range(len(cap_list)):
		b_list = cap_list[i][:] #one gran at the time
		res_gran_list = cap_gran(m,b_list)[:] #output of cap_gran
		cap_gran_list.append(res_gran_list) #append it to final gran list
		res_gran = 0 #compute the sum of lmnts of the res_gran_list in order to have them as input to the next cap_list lmnt
		for j in range(len(res_gran_list)):
			res_gran = res_gran + res_gran_list[j]
		m = res_gran
	return cap_gran_list


###
#cap_gran_cost(D,D.successors('d')[0])[2]

#G.node[nulln]['sucgload'] = 714

#returns a list with the NOT null nodes of a null node
def null_suc(DD,null_node):
	D = DD
	n_node = null_node
	D_suc = []
	d = D.successors(n_node)
	for i in range(len(d)):
		if D.node[d[i]]['population'] != -1:
			D_suc.append(d[i])
	return D_suc

#returns a list with the Null nodes of a null node
def null_suc_null(DD,null_node):
	D = DD
	n_node = null_node
	D_suc = []
	d = D.successors(n_node)
	for i in range(len(d)):
		if D.node[d[i]]['population'] == -1:
			D_suc.append(d[i])
	return D_suc


#initialize the 'sucggload' of null nodes
def init_null(DD):
	D = DD
	for n in D.nodes():
		if D.node[n]['population'] == -1:
			D.node[n]['sucggload'] = [0,0]

#for all leaf nodes we run the above algo. The sum of the 3rd lmnt 
#(depending on the kind network) of the cap_gran_list is info that null nodes
# must have. 
def cap_gran_null(DD,null_node):
	D = DD
	nulln = null_node
	n = 0
	n_list = []
	for i in range(len(cap_list[2])):#initialize n_list
		n_list.append(0)
	not_null_nodes = null_suc(D,nulln)[:]
	for jj in range(len(cap_list[2])): 
		summ=0
		for j in not_null_nodes:
			summ = summ + cap_gran_cost(D,j)[2][jj]
			n_list[jj] = summ
	D.node[nulln]['sucgload'] = n_list[:]


def all_cap_gran_null(DD): #cap_gran_null' s
	D = DD
	for n in D.nodes():
		if D.node[n]['population']==-1:
				cap_gran_null(D,n)
###



def cap_gran_null_null(DD,null_node): 
	D = DD
	nulln = null_node
	n = 0
	n_list = []
	for i in range(len(cap_list[2])):#initialize n_list
		n_list.append(0)
	null_nodes = null_suc_null(D,nulln)[:]
	for jj in range(len(cap_list[2])): 
		summ=0
		for j in null_nodes: #
			summ = summ + D.node[j]['sucgload'][jj] + D.node[nulln]['sucgload'][jj]
			n_list[jj] = summ
	D.node[nulln]['sucggload'] = n_list[:]



#we need it to the following
def reverse_numeric(x, y):
	return y - x



#arrange lmnts of a list from max->min (multiplicity = 1)
def arrange_list(listt):
	a = listt[:]
	n = 0
	l = []
	for i in a:
		n = i
		if n not in l:
			l.append(i)
	return sorted(l,cmp=reverse_numeric)


def depth_nodes_list(D,dhn):
	nl = []
	D_nodes_list = D.nodes()[:]
	D_nodes_list.remove(dhn)
	for n in D_nodes_list: #create a list with null nodes depending on their depth
		if D.node[n]['population'] == -1:
			nl.append([n,depth_node(D,dhn,n)])
	from operator import itemgetter, attrgetter
	sorted_nl = sorted(nl, key=itemgetter(1))
	nl = sorted_nl[:]
	nl0 = []
	k = len(nl) - 1
	while k > -1:
		nl0.append(nl[k])
		k = k -1
	l = []
	for lmnt in nl0:
		l.append(lmnt[0])
	return l




def cap_gran_null_null000(D,dhn):
	d_list = depth_nodes_list(D,dhn)[:]
	for n in d_list:
		n_list = []
		for i in range(len(cap_list[2])):#initialize n_list
			n_list.append(0)
		l_suc_null = len(null_suc_null(D,n))
		if l_suc_null != 0:
			summ=0
			for jj in range(len(cap_list[2])): 
				summ = summ + l_suc_null
				n_list[jj] = cap_gran(summ,cap_list[2])[jj]
		D.node[n]['suc2gload'] = n_list[:]


def cap_gran_null_null_null000(D):
	for n in D.nodes():
		if D.node[n]['population'] == -1:
			n_list = []
			for i in range(len(cap_list[2])):#initialize n_list
				n_list.append(0)
			#l_suc_null = len(null_suc_null(D,n))
			#if l_suc_null != 0:
			summ=0
			for jj in range(len(cap_list[2])): 
				n_list[jj] = D.node[n]['sucgload'][jj] + D.node[n]['suc2gload'][jj]
			D.node[n]['sucggload'] = n_list[:]


###
def cap_gran_null_null_new(DD,null_node,dh): #thes to root node
	D = DD
	nulln = null_node
	root = dh
	n = 0
	n_list = []
	for i in range(len(cap_list[2])):#initialize n_list
		n_list.append(0)
	null_nodes = null_suc_null(D,nulln)[:]
	nl = []
	nl = depth_nodes_list(D,root)[:]
	for jj in range(len(cap_list[2])): 
		summ=0
		for j in nl: #change it in order to play first with max-distance null nodes.
			summ = summ + D.node[j]['sucgload'][jj] + D.node[nulln]['sucgload'][jj]
			n_list[jj] = summ
	D.node[nulln]['sucggload'] = n_list[:]
###



###############################################################################
def cap_gran_null_null0(DD,null_node): #thes to root node
	D = DD
	nulln = null_node
	n_list = []
	for i in range(len(cap_list[2])):#initialize n_list
		n_list.append(0)
	null_nodes = null_suc_null(D,nulln)[:]
	#nl = []
	#nl = depth_nodes_list(D,root)[:]
	k = 0
	for jj in range(len(cap_list[2])): 
		summ=0
		for j in D.nodes(): 
			j_suc = D.successors(j)[:]
			for n in j_suc:
				if D.node[n]['population'] != -1:
					k = k +1
			if k != 0:
				summ = summ + D.node[j]['sucgload'][jj] + D.node[nulln]['sucgload'][jj]
		n_list[jj] = summ
	D.node[nulln]['sucggload'] = n_list[:]




def all_cap_gran_null_null0(DD):
	D = DD
	for n in D.nodes():
		if D.node[n]['population']==-1 and len(null_suc_null(D,n))==1:
				cap_gran_null_null0(D,n)
###############################################################################



###############################################################################
def cap_gran_null_null00(DD,null_node): #thes to root node
	D = DD
	nulln = null_node
	n_list = []
	for i in range(len(cap_list[2])):#initialize n_list
		n_list.append(0)
	null_nodes = null_suc_null(D,nulln)[:]
	#nl = []
	#nl = depth_nodes_list(D,root)[:]
	k = 0
	for jj in range(len(cap_list[2])): 
		summ=0
		for j in D.nodes(): 
			if D.node[j]['population'] != -1:
				j_suc = D.successors(j)[:]
				for n in j_suc:
					if D.node[n]['population'] != -1:
						k = k +1
				if k != 0:
					summ = summ + D.node[j]['sucgload'][jj] + D.node[nulln]['sucgload'][jj]
		n_list[jj] = summ
	D.node[nulln]['sucggload'] = n_list[:]




def all_cap_gran_null_null00(DD):
	D = DD
	for n in D.nodes():
		if D.node[n]['population']==-1 and len(null_suc_null(D,n))==1:
				cap_gran_null_null0(D,n)
###############################################################################



def all_cap_gran_null_null(DD):
	D = DD
	for n in D.nodes():
		if D.node[n]['population']==-1 and len(null_suc_null(D,n))==1:
				cap_gran_null_null(D,n)




def cap_gran_null_null2(DD,null_node):
	D = DD
	nulln = null_node
	n = 0
	n_list = []
	for i in range(len(cap_list[2])):#initialize n_list
		n_list.append(0)
	null_nodes = null_suc_null(D,nulln)[:]
	for jj in range(len(cap_list[2])): 
		summ=0
		for j in null_nodes:
			summ = summ + D.node[j]['sucggload'][jj]
			n_list[jj] = summ
	D.node[nulln]['sucggload'] = n_list[:]


def all_cap_gran_gran_null_null(DD):
	D = DD
	for n in D.nodes():
		if D.node[n]['population']==-1 and len(null_suc_null(D,n))>1:
			cap_gran_null_null2(D,n)
###


#leaf node cost!!!!!!!!!!!!!!!!1
def semi_ln_cost(DD,nn,ggfather):
	D = DD
	nd = nn
	ggf = ggfather
	#finds the cost of gran
	cc_list = []
	cc = cap_gran_cost(D,nd)
	for i in range(len(cc)):
		for j in range(len(cc[i])):
			lmnt = cc[i][j]
			if lmnt != 0:
				ind = cc[i].index(lmnt)
				cc_list.append(lmnt*cap_list_cost[i][ind])
	#the cable and subduct go all way to the Root!
	path_node_cost1 =  path_length(D,ggf, nd) *  cc_list[0] #price for the f/c
	path_node_cost2 =  path_length(D,ggf, nd) *  cc_list[1] #price for the c/s
	#[7,24] s/d Only at its edge!
	path_node_cost3 =  path_length(D, D.predecessors(nd)[0], nd) *  cc_list[2]
	#prepei na valo to [7,24] s/d sta miki prin apo to leaf-edge
	pnca = path_node_cost1 + path_node_cost2 + path_node_cost3
	return pnca


#all the semi cost for the leaf nodes !!!!!!!!!!!!!!!!!!!!!!!!!!!!
def semi_ln_costs(DD,ggfather):
	D = DD
	ggf = ggfather
	cost_semi_ln = 0
	for n in D.nodes():
		if D.node[n]['population'] != -1 and D.out_degree(n) == 0:
			cost_semi_ln = cost_semi_ln + semi_ln_cost(D,n,ggf)
	return cost_semi_ln


#pame gia to kostos kathe akmis me akro null node
def null_node_cost(DD,null_node):
	D = DD
	nn=null_node
	nn_edge_cost = 0
	if D.node[nn]['sucggload'][0] <= cap_list[2][0] and not 0:
		nn_edge_cost1 = path_length(D, D.predecessors(nn)[0], nn) * cap_sd_cost[0]
	if D.node[nn]['sucggload'][1] <= cap_list[2][1] and not 0:
		nn_edge_cost2 = path_length(D, D.predecessors(nn)[0], nn) * cap_sd_cost[1]
	nn_edge_cost = nn_edge_cost1 + nn_edge_cost2
	return nn_edge_cost


#all the null node costs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def all_null_node_costs(DD):
	D = DD
	cost_null = 0
	for n in D.nodes():
		if D.node[n]['population'] == -1:
			cost_null = cost_null + null_node_cost(D,n)
	return cost_null


#boxes !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def all_boxes(DD):
	D = DD
	cost_null = 0
	met = 0
	for n in D.nodes():
		if D.node[n]['population'] == -1:
			met = met + 1
	return met*30 #price for the box


def all_length(DD):
	D = DD
	s = 0
	for e in D.edges():
		s = s + path_length(D, e[0], e[1])
	return s

#costs that have to do with length
def all_length_cost(DD):
	D = DD
	length = all_length(D)
	trench_cost = length * 7 #price for the trench/meter
	main_duct_cost = length * cap_d_cost[0] #price for the main duct/meter
	return trench_cost + main_duct_cost

#change is here
#given a mst graph GG, and a node of it as root, returns the DiGraph tree.
def root_tree(GG,root0):
	L = []
	init_N = GG.nodes()
	init_N.remove(root0)
	N = []
	for i in  GG.edges(root0):
		if i[1] in init_N:
			L.append(i)
			N.append(i[1])
	for root in N:
		if root in init_N:
			init_N.remove(root)
			for i in  GG.edges(root):
				if i[1] in init_N:
					L.append(i)
					N.append(i[1])
	N.append(root0)
	GGGG =nx.DiGraph()
	GGGG.add_edges_from(L)
	#tora prepei na vlao ta attrs pantou!
	for e in GGGG.edges():
		if (e[0],e[1]) in G.edges():
			GGGG[e[0]][e[1]]['weight'] = GG.edge[e[0]][e[1]]['weight']
		if (e[1],e[0]) in G.edges():
			GGGG[e[0]][e[1]]['weight'] = GG.edge[e[0]][e[1]]['weight']
	for n in GGGG.nodes():
		GGGG.node[n]['population'] = GG.node[n]['population'] 
	return GGGG




def grans_to_edges(D):
	#gives to the leaf edges of not null nodes the 'grans'
	for e in D.edges():
		if D.node[e[1]]['population'] != -1:
			D[e[0]][e[1]]['grans'] =  cap_gran_cost(D,e[1])
	#creates the list of the paths
	l_paths = []
	for n in D.nodes():
		if D.node[n]['population'] != -1:
			p = path(D,dhn,n)[2]
			p.remove(p[len(p)-1]) #last edge of path is done from above
			l_paths.append([p,n,len(p)])
	#from this list, we choose the larger one
	from operator import itemgetter, attrgetter
	sorted_l_paths = sorted(l_paths, key=itemgetter(2))
	longest_path = sorted_l_paths[len(sorted_l_paths)-1][0]
	#gives grans to edges!!!
	for e in longest_path:
		listedge = []
		le = []
		c = []
		for l in sorted_l_paths:
			if e in l[0]:
				c = cap_gran_cost(D,l[1])
				le.append([c[0],c[1]])
		dgg = D.node[e[1]]['sucggload']
		dg = D.node[e[1]]['sucgload']
		n_dgg = cap_gran(dgg[0] ,cap_list[2])
		n_dg = cap_gran(dg[0],cap_list[2])
		f_dgg = [0,0]
		f_dg = [0,0]
		f_dgg[0], f_dgg[1] = n_dgg[0], dgg[1]
		f_dg[0], f_dg[1] = n_dg[0], dg[1]
		if f_dgg != [0,0]:
			listedge.append([le,f_dgg,c[3]])
			#D[e[0]][e[1]]['grans'] = listedge[:]
			#D[e[0]][e[1]]['grans'][0][1] = D.node[e[1]]['sucggload']
		else:
			listedge.append([le,f_dg,c[3]])
			#D[e[0]][e[1]]['grans'] = listedge
		D[e[0]][e[1]]['grans'] = listedge




def grans_to_edges0(D):
	#gives to the leaf edges of not null nodes the 'grans'
	for e in D.edges():
		if D.node[e[1]]['population'] != -1:
			D[e[0]][e[1]]['grans'] =  cap_gran_cost(D,e[1])
	#creates the list of the paths
	l_paths = [] #this list is ok!!!
	dhn = find_dhn(D,D)
	for n in D.nodes():
		if D.node[n]['population'] != -1:
			p = path(D,dhn,n)[2]
			p.remove(p[len(p)-1]) #last edge of path is done from above
			l_paths.append([p,n,len(p)])
	#from this list, we choose the larger one
	#wrong!!!
	from operator import itemgetter, attrgetter
	sorted_l_paths = sorted(l_paths, key=itemgetter(2))
	#longest_path = sorted_l_paths[len(sorted_l_paths)-1][0]
	#gives grans to edges!!!
	for slp in sorted_l_paths:
		for e in slp[0]:
			listedge = []
			le = []
			c = []
			for l in sorted_l_paths:
				if e in l[0]:
					c = cap_gran_cost(D,l[1])
					le.append([c[0],c[1]])
			dgg = D.node[e[1]]['sucggload']
			dg = D.node[e[1]]['sucgload']
			n_dgg = cap_gran(dgg[0] ,cap_list[2])
			n_dg = cap_gran(dg[0],cap_list[2])
			f_dgg = [0,0]
			f_dg = [0,0]
			f_dgg[0], f_dgg[1] = n_dgg[0], dgg[1]
			f_dg[0], f_dg[1] = n_dg[0], dg[1]
			if f_dgg != [0,0]:
				listedge.append([le,f_dgg,c[3]])
				#D[e[0]][e[1]]['grans'] = listedge[:]
				#D[e[0]][e[1]]['grans'][0][1] = D.node[e[1]]['sucggload']
			else:
				listedge.append([le,f_dg,c[3]])
				#D[e[0]][e[1]]['grans'] = listedge
			D[e[0]][e[1]]['grans'] = listedge






####################################################################

def grans_again0(D):
	for e in D.edges():
		D_e = D[e[0]][e[1]]
		l = D_e['grans']
		if len(l) == 1:
			lg = []
			l0 = l[0][0][:]
			Lg = []
	#		print str(l0), " --- ",  str(len(l0))
			if len(l0) == 1:
				#print l0[0]
				for i in l0[0]:
					lg.append(i)
				for i in range(1,len(l[0])):
					lg.append(l[0][i])
			else:
				#print l0
				for i in l0:
					for j in i:
						jj_list = []
						for k in range(len(j)):
							jj_list.append(0)
						#print jj_list
						lg.append(jj_list)
				lgg = []
				for i in range(2):
					lgg.append(lg[i])
				#print lgg
				for i in range(len(l0)):
					for j in range(len(l0[i])):
						for k in range(len(l0[i][j])):
							lgg[j][k] = lgg[j][k] + l0[i][j][k]
				lg = lgg[:]
				for i in range(1,len(l[0])):
					lg.append(l[0][i])
			Lg = []
			for i in lg:
				Lg.append(i)
			#print Lg
			D_e['grans'] = Lg[:]
			D_e['ALPHA'] = Lg[:]
		else:
			D_e['ALPHA'] = l


####################################################################

def granss0(D):
	for e in D.edges():
		D_e = D[e[0]][e[1]]
		a = D_e['grans']
		if a != {}:
			D_e['grans_f'] = a[0] 
			D_e['grans_c'] = a[1] 
			D_e['grans_s'] = a[2]
			D_e['grans_d'] = a[3]


def grans_to_edges_cool(D):
	for e in D.edges():
		D_e = D[e[0]][e[1]]
		D_e_gran = D_e['grans']
		if D_e_gran != {}:
			if D.node[e[1]]['population'] == -1:
				a = cap_gran(D_e_gran[1][0],cap_list[2])
				D_e_gran[2] = a
				D_e['grans_s'] = a



def init_edges(D):
	for e in D.edges():
		D_e = D[e[0]][e[1]]
		D_e['grans'] = {}
		D_e['grans_f'] = {}
		D_e['grans_c'] = {}
		D_e['grans_s'] ={}
		D_e['grans_d'] ={}
		D_e['gr_cost'] = 0
		D_e['tr_cost'] = 0
		D_e['dum_cost'] = 0
		D_e['ALPHA'] = {}




#computes the dummy cost of each edge!
def cost_to_edges0(D):
	for e in D.edges():
		D_e = D[e[0]][e[1]]
		D_e_weight = D_e['weight']
		D_e_gran = D_e['grans']
		#prices and costs of each edge
		if D_e_gran != {}:
			grans_value = 0
			alpha = 0
			alpha_c = 0
			beta = 0
			gamma = 0
			if D.node[e[1]]['population'] == -1 and D.successors(e[1]) != []:
				#price of f
				cc_list = []
				cc = D_e_gran[0]
				if len(cc) != 0:
					for i in range(len(cc)):
						lmnt = cc[i]
						if lmnt != 0:
							ind = cc.index(lmnt)
							cc_list.append(lmnt*cap_list_cost[0][ind])
				alpha = sum(cc_list)
				#price of c
				cc_list = []
				cc = D_e_gran[1]
				if len(cc) != 0:
					for i in range(len(cc)):
						lmnt = cc[i]
						if lmnt != 0:
							ind = cc.index(lmnt)
							cc_list.append(lmnt*cap_list_cost[1][ind])
				alpha_c = sum(cc_list)
				#price of s/d
				cc_list = []
				cc = D_e_gran[2]
				if len(cc) != 0:
					for i in range(len(cc)):
						lmnt = cc[i]
						if lmnt != 0:
							ind = cc.index(lmnt)
							cc_list.append(lmnt*cap_list_cost[2][ind])
				beta = sum(cc_list)
				#price of d
				cc_list = []
				cc = D_e_gran[3]
				if len(cc) != 0:
					for i in range(len(cc)):
						lmnt = cc[i]
						if lmnt != 0:
							ind = cc.index(lmnt)
							cc_list.append(lmnt*cap_list_cost[3][ind])
				gamma = sum(cc_list)
				grans_value = alpha + alpha_c + beta + gamma
			if D.node[e[1]]['population'] != -1:
				###for leaf nodes
				#price of d
				cc_list = []
				cc = D_e_gran
				if len(cc) != 0:
					for i in range(len(cc)):
						for j in range(len(cc[i])):
							lmnt = cc[i][j]
							if lmnt != 0:
								ind = cc[i].index(lmnt)
								cc_list.append(lmnt*cap_list_cost[i][ind])
				grans_value = sum(cc_list)
			e_cost_gran = grans_value * D_e_weight
			e_cost_trench = 7 * D_e_weight
			e_cost = e_cost_gran + e_cost_trench
			D_e['gr_cost'] = e_cost_gran
			D_e['tr_cost'] = e_cost_trench
			D_e['dum_cost'] = e_cost



#gives efficiency to edges of D
def efficiency_to_edges(D,gg):
	for e in D.edges():
		if (e[0],e[1]) in gg.edges():
			D[e[0]][e[1]]['efficiency'] = gg[e[0]][e[1]]['efficiency']
		if (e[1],e[0]) in gg.edges():
			D[e[0]][e[1]]['efficiency'] = gg[e[1]][e[0]]['efficiency']


#cutoff null leafs from area
def cutoff_null_leafs(D):
	l_cutoff = []
	for n in D.nodes():
		if D.node[n]['population'] == -1 and len(D.successors(n)) == 0:
			l_cutoff.append(n)
			n_pred = D.predecessors(n)[:]
			for i in n_pred:
				if D.node[i]['population'] == -1 and D.out_degree(i) == 1:
					l_cutoff.append(i)
	for j in l_cutoff:
		D.remove_node(j)


#cutoff_null_leafs0
def cutoff_null_leafs0(g):
	check = [0]
	while len(check) > 0:
		check = [nod for nod in g.degree() if g.degree(nod) == 1 and g.node[nod]['population'] == -1]
		g.remove_nodes_from(check)



#for output in .shp. (after we find the minimum cost network)
def netwrk_cost_dummy0(G,g,dhn):
	cutoff_null_leafs0(g)
	l, gg, leafs, null_l = a_graph_efficiency(g, dhn,1)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	cost_list = []
	network_cost = 0
	for i in range(len(sub_list)):
		D = sub_list[i]
		for e in D.edges():
			D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['ALPHA'] = {}
			#D_e['dum_cost'] = 0
		init_edges(D)
		init_null(D)
		all_cap_gran_null(D) #gives sucgload to the null nodes for not null leafs
		cap_gran_null_null000(D,dhn) #gives suc2gload to the null nodes for null nodes
		cap_gran_null_null_null000(D) #gives sucggload to the null nodes 
		grans_to_edges(D)#okz!!!
		grans_again0(D)
		granss0(D)
		grans_to_edges_cool(D)
		cost_to_edges0(D) #okz!!!!
		efficiency_to_edges(D,gg)
		for e in D.edges():
			network_cost = network_cost + D[e[0]][e[1]]['dum_cost']
		cost_list.append(network_cost)
		for n in D.nodes():
			if n != dhn:
				g.node[n]['sucggload'] = str(D.node[n]['sucggload'])
				g.node[n]['sucgload'] = str(D.node[n]['sucgload'])
				g.node[n]['suc2gload'] = str(D.node[n]['suc2gload'])
		for e in D.edges():
			ee = (e[0],e[1])
			D_e = D[e[0]][e[1]]
			D_e['grans'] = {}
			D_e['grans_c'] = {}
			D_e['ALPHA'] = {}
			if (e[0],e[1]) in g.edges():
				g[e[0]][e[1]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[0]][e[1]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[0]][e[1]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[0]][e[1]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[0]][e[1]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[0]][e[1]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[0]][e[1]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[0]][e[1]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[0]][e[1]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[0]][e[1]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
			if (e[1],e[0]) in g.edges():
				g[e[1]][e[0]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[1]][e[0]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[1]][e[0]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[1]][e[0]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[1]][e[0]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[1]][e[0]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[1]][e[0]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[1]][e[0]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[1]][e[0]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[1]][e[0]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
	g.node[dhn]['sucggload'] = str(D.node[dhn]['sucggload'])
	g.node[dhn]['sucgload'] = str(D.node[dhn]['sucgload'])
	g.node[dhn]['suc2gload'] = str(D.node[dhn]['suc2gload'])
	#for u,v,d in g.edges(data=True):
	#	del d['ALPHA']
	#	del d['grans']
	#	del d['grans_c']
	#	del d['mun_code']
	#	del d['mun_name']
	#	del d['name']
	#	del d['population']
	#	del d['length']
	#	del d['x___gid']
	#	del d['building_i']
	#	del d['gid']
	#	del d['id']
	#	del d['x_gid']
	#for n,d in g.nodes(data=True):
	#	del d['suc2gload']
	#	del d['sucgload']
	#	del d['sucggload']
	g.node[dhn]['root_node'] = 1
	return [g, dhn, network_cost]



#for iteration to count the cost of null nodes
def netwrk_cost_dummy00(G,g,dhn):
	cutoff_null_leafs0(g)
	l, gg, leafs, null_l = a_graph_efficiency(g, dhn,1)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	cost_list = []
	network_cost = 0
	for i in range(len(sub_list)):
		D = sub_list[i]
		for e in D.edges():
			D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['ALPHA'] = {}
			#D_e['dum_cost'] = 0
		init_edges(D)
		init_null(D)
		all_cap_gran_null(D) #gives sucgload to the null nodes for not null leafs
		cap_gran_null_null000(D,dhn) #gives suc2gload to the null nodes for null nodes
		cap_gran_null_null_null000(D) #gives sucggload to the null nodes 
		grans_to_edges(D)#okz!!!
		grans_again0(D)
		granss0(D)
		grans_to_edges_cool(D)
		cost_to_edges0(D) #okz!!!!
		efficiency_to_edges(D,gg)
		for e in D.edges():
			network_cost = network_cost + D[e[0]][e[1]]['dum_cost']
		cost_list.append(network_cost)
	return [g, dhn, network_cost]



#for output in .shp. (after we find the minimum cost network)
def netwrk_cost_dummy1(G,g,dhn):
	cutoff_null_leafs0(g)
	g.node[dhn]['root_node'] = 1
	l, gg, leafs, null_l = a_graph_efficiency(g, dhn,1)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	cost_list = []
	network_cost = 0
	for i in range(len(sub_list)):
		D = sub_list[i]
		#for e in D.edges():
			#D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['ALPHA'] = {}
			#D_e['dum_cost'] = 0
		init_edges(D)
		init_null(D)
		all_cap_gran_null(D) #gives sucgload to the null nodes for not null leafs
		cap_gran_null_null000(D,dhn) #gives suc2gload to the null nodes for null nodes
		cap_gran_null_null_null000(D) #gives sucggload to the null nodes 
		grans_to_edges0(D)#okz!!!
		grans_again0(D)
		granss0(D)
		grans_to_edges_cool(D)
		cost_to_edges0(D) #okz!!!!
		efficiency_to_edges(D,gg)
		for e in D.edges():
			network_cost = network_cost + D[e[0]][e[1]]['dum_cost']
		cost_list.append(network_cost)
		for n in D.nodes():
			if n != dhn:
				g.node[n]['sucggload'] = str(D.node[n]['sucggload'])
				g.node[n]['sucgload'] = str(D.node[n]['sucgload'])
				g.node[n]['suc2gload'] = str(D.node[n]['suc2gload'])
		for e in D.edges():
			ee = (e[0],e[1])
			D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['grans_c'] = {}
			#D_e['ALPHA'] = {}
			if (e[0],e[1]) in g.edges():
				g[e[0]][e[1]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[0]][e[1]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[0]][e[1]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[0]][e[1]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[0]][e[1]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[0]][e[1]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[0]][e[1]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[0]][e[1]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[0]][e[1]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[0]][e[1]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
			if (e[1],e[0]) in g.edges():
				g[e[1]][e[0]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[1]][e[0]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[1]][e[0]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[1]][e[0]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[1]][e[0]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[1]][e[0]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[1]][e[0]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[1]][e[0]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[1]][e[0]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[1]][e[0]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
	for e in g.edges():
		g_e = g[e[0]][e[1]]
		if g_e['grans_f'] == {}:
			g_e['grans_f'] = str(g_e['grans_f'])
		if g_e['grans_s'] == {}:
			g_e['grans_s'] = str(g_e['grans_s'])
		if g_e['grans_d'] == {}:
			g_e['grans_d'] = str(g_e['grans_d'])
		if g_e['gr_cost'] == 0:
			g_e['gr_cost'] = str(g_e['gr_cost'])
		if g_e['tr_cost'] == 0:
			g_e['tr_cost'] = str(g_e['tr_cost'])
		if g_e['dum_cost'] == 0:
			g_e['dum_cost'] = str(g_e['dum_cost'])
		if g_e['efficiency'] == 0:
			g_e['efficiency'] = str(g_e['efficiency'])
	g.node[dhn]['sucggload'] = str(D.node[dhn]['sucggload'])
	g.node[dhn]['sucgload'] = str(D.node[dhn]['sucgload'])
	g.node[dhn]['suc2gload'] = str(D.node[dhn]['suc2gload'])
	for u,v,d in g.edges(data=True):
		del d['ALPHA']
		del d['grans']
		del d['grans_c']
		del d['mun_code']
		del d['mun_name']
		del d['name']
		del d['population']
		del d['length']
		del d['x___gid']
		del d['building_i']
		del d['gid']
		del d['id']
		del d['x_gid']
	for n,d in g.nodes(data=True):
		del d['suc2gload']
		del d['sucgload']
		del d['sucggload']
	return [g, dhn, network_cost]



#for output in .shp. (after we find the minimum cost network)
def netwrk_cost_dummy2(G,g,dhn):
	cutoff_null_leafs0(g)
	g.node[dhn]['root_node'] = 1
	l, gg, leafs, null_l = a_graph_efficiency(g, dhn,1)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	cost_list = []
	network_cost = 0
	for i in range(len(sub_list)):
		D = sub_list[i]
		#for e in D.edges():
			#D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['ALPHA'] = {}
			#D_e['dum_cost'] = 0
		init_edges(D)
		init_null(D)
		all_cap_gran_null(D) #gives sucgload to the null nodes for not null leafs
		cap_gran_null_null000(D,dhn) #gives suc2gload to the null nodes for null nodes
		cap_gran_null_null_null000(D) #gives sucggload to the null nodes 
		grans_to_edges0(D)#okz!!!
		grans_again0(D)
		granss0(D)
		grans_to_edges_cool(D)
		cost_to_edges0(D) #okz!!!!
		efficiency_to_edges(D,gg)
		for e in D.edges():
			network_cost = network_cost + D[e[0]][e[1]]['dum_cost']
		cost_list.append(network_cost)
		for n in D.nodes():
			if n != dhn:
				g.node[n]['sucggload'] = str(D.node[n]['sucggload'])
				g.node[n]['sucgload'] = str(D.node[n]['sucgload'])
				g.node[n]['suc2gload'] = str(D.node[n]['suc2gload'])
		for e in D.edges():
			ee = (e[0],e[1])
			D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['grans_c'] = {}
			#D_e['ALPHA'] = {}
			if (e[0],e[1]) in g.edges():
				g[e[0]][e[1]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[0]][e[1]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[0]][e[1]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[0]][e[1]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[0]][e[1]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[0]][e[1]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[0]][e[1]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[0]][e[1]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[0]][e[1]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[0]][e[1]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
			if (e[1],e[0]) in g.edges():
				g[e[1]][e[0]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[1]][e[0]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[1]][e[0]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[1]][e[0]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[1]][e[0]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[1]][e[0]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[1]][e[0]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[1]][e[0]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[1]][e[0]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[1]][e[0]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
	for e in g.edges():
		g_e = g[e[0]][e[1]]
		if g_e['grans_f'] == {}:
			g.remove_edge(e[0],e[1])
	g.node[dhn]['sucggload'] = str(D.node[dhn]['sucggload'])
	g.node[dhn]['sucgload'] = str(D.node[dhn]['sucgload'])
	g.node[dhn]['suc2gload'] = str(D.node[dhn]['suc2gload'])
	for u,v,d in g.edges(data=True):
		del d['ALPHA']
		del d['grans']
		del d['grans_c']
		del d['mun_code']
		del d['mun_name']
		del d['name']
		del d['population']
		del d['length']
		del d['x___gid']
		del d['building_i']
		del d['gid']
		del d['id']
		del d['x_gid']
		del d['block_id']
	for n,d in g.nodes(data=True):
		del d['suc2gload']
		del d['sucgload']
		del d['sucggload']
	return [g, dhn, network_cost]


#for output in .shp. (after we find the minimum cost network)
#sto output exei k ta directed sub_graphs tou g
def netwrk_cost_dummy22(G,g,dhn):
	cutoff_null_leafs0(g)
	g.node[dhn]['root_node'] = 1
	l, gg, leafs, null_l = a_graph_efficiency(g, dhn,1)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	cost_list = []
	network_cost = 0
	for i in range(len(sub_list)):
		D = sub_list[i]
		#for e in D.edges():
			#D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['ALPHA'] = {}
			#D_e['dum_cost'] = 0
		init_edges(D)
		init_null(D)
		all_cap_gran_null(D) #gives sucgload to the null nodes for not null leafs
		cap_gran_null_null000(D,dhn) #gives suc2gload to the null nodes for null nodes
		cap_gran_null_null_null000(D) #gives sucggload to the null nodes 
		grans_to_edges0(D)#okz!!!
		grans_again0(D)
		granss0(D)
		grans_to_edges_cool(D)
		cost_to_edges0(D) #okz!!!!
		efficiency_to_edges(D,gg)
		for e in D.edges():
			network_cost = network_cost + D[e[0]][e[1]]['dum_cost']
		cost_list.append(network_cost)
		for n in D.nodes():
			if n != dhn:
				g.node[n]['sucggload'] = str(D.node[n]['sucggload'])
				g.node[n]['sucgload'] = str(D.node[n]['sucgload'])
				g.node[n]['suc2gload'] = str(D.node[n]['suc2gload'])
		for e in D.edges():
			ee = (e[0],e[1])
			D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['grans_c'] = {}
			#D_e['ALPHA'] = {}
			if (e[0],e[1]) in g.edges():
				g[e[0]][e[1]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[0]][e[1]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[0]][e[1]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[0]][e[1]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[0]][e[1]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[0]][e[1]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[0]][e[1]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[0]][e[1]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[0]][e[1]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[0]][e[1]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
			if (e[1],e[0]) in g.edges():
				g[e[1]][e[0]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[1]][e[0]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[1]][e[0]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[1]][e[0]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[1]][e[0]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[1]][e[0]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[1]][e[0]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[1]][e[0]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[1]][e[0]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[1]][e[0]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
	for e in g.edges():
		g_e = g[e[0]][e[1]]
		if g_e['grans_f'] == {}:
			g.remove_edge(e[0],e[1])
	g.node[dhn]['sucggload'] = str(D.node[dhn]['sucggload'])
	g.node[dhn]['sucgload'] = str(D.node[dhn]['sucgload'])
	g.node[dhn]['suc2gload'] = str(D.node[dhn]['suc2gload'])
	for u,v,d in g.edges(data=True):
		del d['ALPHA']
		del d['grans']
		del d['grans_c']
		del d['mun_code']
		del d['mun_name']
		del d['name']
		del d['population']
		del d['length']
		del d['x___gid']
		del d['building_i']
		del d['gid']
		del d['id']
		del d['x_gid']
		del d['block_id']
	for n,d in g.nodes(data=True):
		del d['suc2gload']
		del d['sucgload']
		del d['sucggload']
	return [g, dhn, network_cost,sub_list]


#for output in .shp. (after we find the minimum cost network)
#taht's for percentages
def netwrk_cost_dummy2beta(G,g,dhn):
	cutoff_null_leafs0(g)
	g.node[dhn]['root_node'] = 1
	l, gg, leafs, null_l = a_graph_efficiency(g, dhn,1)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	cost_list = []
	network_cost = 0
	for i in range(len(sub_list)):
		D = sub_list[i]
		#for e in D.edges():
			#D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['ALPHA'] = {}
			#D_e['dum_cost'] = 0
		init_edges(D)
		init_null(D)
		all_cap_gran_null(D) #gives sucgload to the null nodes for not null leafs
		cap_gran_null_null000(D,dhn) #gives suc2gload to the null nodes for null nodes
		cap_gran_null_null_null000(D) #gives sucggload to the null nodes 
		grans_to_edges0(D)#okz!!!
		grans_again0(D)
		granss0(D)
		grans_to_edges_cool(D)
		cost_to_edges0(D) #okz!!!!
		efficiency_to_edges(D,gg)
		for e in D.edges():
			network_cost = network_cost + D[e[0]][e[1]]['dum_cost']
		cost_list.append(network_cost)
		for n in D.nodes():
			if n != dhn:
				g.node[n]['sucggload'] = str(D.node[n]['sucggload'])
				g.node[n]['sucgload'] = str(D.node[n]['sucgload'])
				g.node[n]['suc2gload'] = str(D.node[n]['suc2gload'])
		for e in D.edges():
			ee = (e[0],e[1])
			D_e = D[e[0]][e[1]]
			#D_e['grans'] = {}
			#D_e['grans_c'] = {}
			#D_e['ALPHA'] = {}
			if (e[0],e[1]) in g.edges():
				g[e[0]][e[1]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[0]][e[1]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[0]][e[1]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[0]][e[1]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[0]][e[1]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[0]][e[1]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[0]][e[1]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[0]][e[1]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[0]][e[1]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[0]][e[1]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
			if (e[1],e[0]) in g.edges():
				g[e[1]][e[0]]['grans_f'] = str(D[e[0]][e[1]]['grans_f'])
				g[e[1]][e[0]]['grans_c'] = str(D[e[0]][e[1]]['grans_c'])
				g[e[1]][e[0]]['grans_s'] = str(D[e[0]][e[1]]['grans_s'])
				g[e[1]][e[0]]['grans_d'] = str(D[e[0]][e[1]]['grans_d'])
				g[e[1]][e[0]]['gr_cost'] = str(D[e[0]][e[1]]['gr_cost'])
				g[e[1]][e[0]]['tr_cost'] = str(D[e[0]][e[1]]['tr_cost'])
				g[e[1]][e[0]]['dum_cost'] = str(D[e[0]][e[1]]['dum_cost'])
				g[e[1]][e[0]]['grans'] = str(D[e[0]][e[1]]['grans'])
				g[e[1]][e[0]]['ALPHA'] = str(D[e[0]][e[1]]['ALPHA'])
				g[e[1]][e[0]]['efficiency'] = str(D[e[0]][e[1]]['efficiency'])
	for e in g.edges():
		g_e = g[e[0]][e[1]]
		if g_e['grans_f'] == {}:
			g.remove_edge(e[0],e[1])
	g.node[dhn]['sucggload'] = str(D.node[dhn]['sucggload'])
	g.node[dhn]['sucgload'] = str(D.node[dhn]['sucgload'])
	g.node[dhn]['suc2gload'] = str(D.node[dhn]['suc2gload'])
	for u,v,d in g.edges(data=True):
		del d['ALPHA']
		del d['grans']
		del d['grans_c']
		#del d['mun_code']
		#del d['mun_name']
		del d['name']
		del d['population']
		del d['length']
		del d['x___gid']
		del d['building_i']
		del d['gid']
		del d['id']
		del d['x_gid']
		del d['block_id']
	for n,d in g.nodes(data=True):
		del d['suc2gload']
		del d['sucgload']
		del d['sucggload']
	return [g, dhn, network_cost]





#returns tetrades of [block_id, block nodes, som of these nodes, the sp closest node to dhn, and the distance of it from dhn]
#oi 4ades einai sorted me to sp-distance apo to dhn
def graph_blocks7(GG,G,dhn):
	l_ids = []
	#creates list with all block ids except null nodes -1
	for n in G.nodes():
		if G.node[n]['block_id'] != -1:
			l_ids.append(G.node[n]['block_id'])
	new_l = []
	for i in l_ids:
		if i not in new_l:
			new_l.append(i)
	#creates empty lists
	list_ids = []
	for j in range(len(new_l)):
		list_ids.insert(0,[])
	#put nodes to lists according to their block_id
	for ii in new_l:
		for nn in G.nodes():
			if G.node[nn]['block_id'] == ii:
				list_ids[new_l.index(ii)].append(nn)
	#computes som of block_nodes
	new_list_ids = []
	for l in list_ids:
		l_node = []
		s = 0
		#finds the em closest lmnt to dhn
		smallest_em_node = []
		for n in l:
			smallest_em_node.append([n,adistance(n,dhn)])
		from operator import itemgetter, attrgetter
		sorted_smallest_em_node = sorted(smallest_em_node, key=itemgetter(1))
		r0 = sorted_smallest_em_node[0][0] #an lmnt em closest to dhn. done!
		new_list_ids.append([l,r0,adistance(r0,dhn)])
		from operator import itemgetter, attrgetter
		sorted_new_list_ids = sorted(new_list_ids, key=itemgetter(2))
	blocks_list = []
	for l in sorted_new_list_ids:
		r = l[1]
		spr_node = (0,0)
		spr_length = 0
		spr_list = nx.dijkstra_path(GG,dhn,r)[:] #list of nodes of the sp
		#finds spr_node
		met = 0 
		for n in spr_list: ############
			if met == 0:
				lnodes = GG.neighbors(n)[:]
				for ln in lnodes:
					if met == 0:
						if GG.node[ln]['block_id'] == GG.node[r]['block_id']:
							spr_node = ln #den paizei pote auto afou sto sp yparxoun mono null nodes!
							met = 1
					else:
						break
		#spr_length0 = nx.dijkstra_path_length(GG,dhn,spr_node)
		s = 0
		for n in l[0]:
			#spr_length = nx.dijkstra_path_length(GG,dhn,n)
			s = s + G.node[n]['population']
			#l_node.append([n,adistance(n,dhn)])
			#l_node.append([n,spr_length0])
		#from operator import itemgetter, attrgetter
		#sorted_l_node = sorted(l_node, key=itemgetter(1))
		#s0 = sorted_l_node[0][0]
		s0 = spr_node
		#blocks_list.append([G.node[l[0][0]]['block_id'],l[0],s,s0, nx.shortest_path_length(GG, source=dhn, target=s0)])\
		blocks_list.append([G.node[l[0][0]]['block_id'],l[0],s,s0, nx.dijkstra_path_length(GG, dhn, s0)])
	from operator import itemgetter, attrgetter
	sorted_blocks_list = sorted(blocks_list, key=itemgetter(4))
	return sorted_blocks_list



#returns tetrades of [block_id, block nodes, som of these nodes, the sp closest node to dhn, and the distance of it from dhn]
#oi 4ades einai sorted me to sp-distance apo to dhn
#exontas to dhn, prepei na addaroume blocks stin lista mexri na ftasoun ston plithismo mas. ara o plithismos prepei na einai gnostos.
def graph_blocks70(GG,G,dhn,max_plith):
	l_ids = []
	#creates list with all block ids except null nodes -1
	for n in G.nodes():
		if G.node[n]['block_id'] != -1:
			l_ids.append(G.node[n]['block_id'])
	new_l = []
	for i in l_ids:
		if i not in new_l:
			new_l.append(i)
	#creates empty lists
	list_ids = []
	for j in range(len(new_l)):
		list_ids.insert(0,[])
	#put nodes to lists according to their block_id
	for ii in new_l:
		for nn in G.nodes():
			if G.node[nn]['block_id'] == ii:
				list_ids[new_l.index(ii)].append(nn)
	#computes som of block_nodes
	new_list_ids = []
	for l in list_ids:
		l_node = []
		s = 0
		#finds the em closest lmnt to dhn
		smallest_em_node = []
		for n in l:
			smallest_em_node.append([n,adistance(n,dhn)])
		from operator import itemgetter, attrgetter
		sorted_smallest_em_node = sorted(smallest_em_node, key=itemgetter(1))
		r0 = sorted_smallest_em_node[0][0] #an lmnt em closest to dhn. done!
		new_list_ids.append([l,r0,adistance(r0,dhn)])
		from operator import itemgetter, attrgetter
		sorted_new_list_ids = sorted(new_list_ids, key=itemgetter(2))
	blocks_list = []
	s_plith = 0
	for l in sorted_new_list_ids:
		r = l[1]
		spr_node = (0,0)
		spr_length = 0
		spr_list = nx.dijkstra_path(GG,dhn,r)[:] #list of nodes of the sp
		#finds spr_node
		met = 0 
		for n in spr_list: ############
			if met == 0:
				lnodes = GG.neighbors(n)[:]
				for ln in lnodes:
					if met == 0:
						if GG.node[ln]['block_id'] == GG.node[r]['block_id']:
							spr_node = ln #den paizei pote auto afou sto sp yparxoun mono null nodes!
							met = 1
					else:
						break
		#spr_length0 = nx.dijkstra_path_length(GG,dhn,spr_node)
		s = 0
		for n in l[0]:
			#spr_length = nx.dijkstra_path_length(GG,dhn,n)
			s = s + G.node[n]['population']
			#l_node.append([n,adistance(n,dhn)])
			#l_node.append([n,spr_length0])
		#from operator import itemgetter, attrgetter
		#sorted_l_node = sorted(l_node, key=itemgetter(1))
		#s0 = sorted_l_node[0][0]
		s0 = spr_node
		#blocks_list.append([G.node[l[0][0]]['block_id'],l[0],s,s0, nx.shortest_path_length(GG, source=dhn, target=s0)])\
		blocks_list.append([G.node[l[0][0]]['block_id'],l[0],s,s0, nx.dijkstra_path_length(GG, dhn, s0)])
	from operator import itemgetter, attrgetter
	sorted_blocks_list = sorted(blocks_list, key=itemgetter(4))
	last_sorted_bl = []
	for l in sorted_blocks_list:
		s_plith = s_plith + l[2]
		if s_plith <= plith_cl:
			last_sorted_bl.append(l)
		else:
			break
	return last_sorted_bl



def graph_blocks700(G,dhn,plith_cl):
	l_ids = []
	#creates list with all block ids except null nodes -1
	for n in G.nodes():
		if G.node[n]['block_id'] != -1:
			l_ids.append(G.node[n]['block_id'])
	new_l = []
	for i in l_ids:
		if i not in new_l:
			new_l.append(i)
	#creates empty lists
	list_ids = []
	for j in range(len(new_l)):
		list_ids.insert(0,[])
	#put nodes to lists according to their block_id
	for ii in new_l:
		for nn in G.nodes():
			if G.node[nn]['block_id'] == ii:
				list_ids[new_l.index(ii)].append(nn)
	#computes som of block_nodes
	new_list_ids = []
	for l in list_ids:
		l_node = []
		s = 0
		#finds the em closest lmnt to dhn
		smallest_em_node = []
		for n in l:
			smallest_em_node.append([n,adistance(n,dhn)])
		from operator import itemgetter, attrgetter
		sorted_smallest_em_node = sorted(smallest_em_node, key=itemgetter(1))
		r0 = sorted_smallest_em_node[0][0] #an lmnt em closest to dhn. done!
		new_list_ids.append([l,r0,adistance(r0,dhn)])
		from operator import itemgetter, attrgetter
		sorted_new_list_ids = sorted(new_list_ids, key=itemgetter(2))
	blocks_list = []
	s_plith = 0
	for l in sorted_new_list_ids:
		r = l[1]
		spr_node = r
		spr_length = 0
		spr_list = nx.dijkstra_path(G,dhn,r)[:] #list of nodes of the sp
		#finds spr_node
		met = 0 
		for n in spr_list: ############
			if met == 0:
				lnodes = G.neighbors(n)[:]
				for ln in lnodes:
					if met == 0 and G.node[ln]['population'] != -1:
						if G.node[ln]['block_id'] == G.node[r]['block_id']:
							spr_node = ln #den paizei pote auto afou sto sp yparxoun mono null nodes!
							met = 1
					else:
						break
		#spr_length0 = nx.dijkstra_path_length(GG,dhn,spr_node)
		s = 0
		for n in l[0]:
			#spr_length = nx.dijkstra_path_length(GG,dhn,n)
			s = s + G.node[n]['population']
			#l_node.append([n,adistance(n,dhn)])
			#l_node.append([n,spr_length0])
		#from operator import itemgetter, attrgetter
		#sorted_l_node = sorted(l_node, key=itemgetter(1))
		#s0 = sorted_l_node[0][0]
		s0 = spr_node
		#blocks_list.append([G.node[l[0][0]]['block_id'],l[0],s,s0, nx.shortest_path_length(GG, source=dhn, target=s0)])\
		blocks_list.append([G.node[l[0][0]]['block_id'],l[0],s,s0, nx.dijkstra_path_length(G, dhn, s0)])
	from operator import itemgetter, attrgetter
	sorted_blocks_list = sorted(blocks_list, key=itemgetter(4))
	last_sorted_bl = []
	for l in sorted_blocks_list:
		s_plith = s_plith + l[2]
		if s_plith <= plith_cl:
			last_sorted_bl.append(l)
		else:
			break
	return last_sorted_bl




#returns 3dim list of block nodes,sumofmass of them,and the Node 
def graph_blocks_all(G):
	l_ids = []
	#creates list with all block ids except null nodes -1
	for n in G.nodes():
		if G.node[n]['block_id'] != -1:
			l_ids.append(G.node[n]['block_id'])
	new_l = []
	for i in l_ids:
		if i not in new_l:
			new_l.append(i)
	#creates empty lists
	list_ids = []
	for j in range(len(new_l)):
		list_ids.insert(0,[])
	#put nodes to lists according to their block_id
	for ii in new_l:
		for nn in G.nodes():
			if G.node[nn]['block_id'] == ii:
				list_ids[new_l.index(ii)].append(nn)
	#computes som of block_nodes and the Node lmnt
	list_ids1 = []
	for l in list_ids:
		lista = change_dims(G,l)[:]
		list_ids1.append([l,cluster_m(G,l),centerofmass0(G,l)])
	return list_ids1


#returns a list with the ids of all the blocks of G
def blocks_id(G):
	l_ids = []
	#creates list with all block ids except null nodes -1
	for n in G.nodes():
		if G.node[n]['block_id'] != -1 and G.node[n]['block_id'] not in l_ids:
			l_ids.append(G.node[n]['block_id'])
	return l_ids


#returns a list with the not null nodes of a block with given id
def bid_nodes(G,idi):
	bid = blocks_id(G)[:]
	list_ids = []
	for n in G.nodes():
		if G.node[n]['block_id'] == idi:
			list_ids.append(n)
	return list_ids


def write_shp(G, outdir):
    try:
        from osgeo import ogr
    except ImportError:
        raise ImportError("write_shp requires OGR: http://www.gdal.org/")
    def netgeometry(key, data, node = False):
        if not node:
            if data.has_key('Wkb'):
                geom = ogr.CreateGeometryFromWkb(data['Wkb'])
            elif data.has_key('Wkt'):
                geom = ogr.CreateGeometryFromWkt(data['Wkt'])
            elif type(key[0]).__name__  == 'tuple': # edge keys are packed tuples
                geom = ogr.Geometry(ogr.wkbLineString)
                _from, _to = key[0], key[1]
                try:
                    geom.SetPoint(0, *_from)
                    geom.SetPoint(1, *_to)
                except TypeError:
                    # assume user used tuple of int and choked ogr
                    _ffrom = [float(x) for x in _from]
                    _fto = [float(x) for x in _to]
                    geom.SetPoint(0, *_ffrom)
                    geom.SetPoint(1, *_fto)
            else:
                geom = ogr.Geometry(ogr.wkbPoint)
                try:
                    geom.SetPoint(0, *key)
                except TypeError:
                    # assume user used tuple of int and choked ogr
                    fkey = [float(x) for x in key]
                    geom.SetPoint(0, *fkey)
        else:
                geom = ogr.Geometry(ogr.wkbPoint)
                try:
                    geom.SetPoint(0, *key)
                except TypeError:
                    # assume user used tuple of int and choked ogr
                    fkey = [float(x) for x in key]
                    geom.SetPoint(0, *fkey)
        return geom
    def create_feature(geometry, lyr, attributes=None):
        feature = ogr.Feature(lyr.GetLayerDefn())
        feature.SetGeometry(g)
        if attributes != None:
            for field, data in attributes.iteritems(): 
               feature.SetField(field,data)
        lyr.CreateFeature(feature)
        feature.Destroy()
    drv = ogr.GetDriverByName("ESRI Shapefile")
    shpdir = drv.CreateDataSource(outdir)
    try:
        shpdir.DeleteLayer("nodes")
    except:
        pass
    nodes = shpdir.CreateLayer("nodes", None, ogr.wkbPoint)
    #print nodes
    #sys.exit(1)
    nodeDict = dict(G.nodes(data=True))
    OGRTypes = {int:ogr.OFTInteger, str:ogr.OFTString, float:ogr.OFTReal}
    fields = {}
    attributes = {}
    for n in G:
        data = G.node[n].values() or [{}]
        g = netgeometry(n, data[0], True)
        for key, data in nodeDict[n].iteritems():
            if (key != 'Json' and key != 'Wkt' and key != 'Wkb' 
                and key != 'ShpName'):
                if key not in fields:
                    if type(data) in OGRTypes:
                         fields[key] = OGRTypes[type(data)]
                    else:
                         fields[key] = ogr.OFTString
                    newfield = ogr.FieldDefn(key, fields[key])
                    nodes.CreateField(newfield)
                    attributes[key] = data
                else:
                    attributes[key] = data
        create_feature(g, nodes, attributes)
    try:
        shpdir.DeleteLayer("edges")
    except:
        pass
    edges = shpdir.CreateLayer("edges", None, ogr.wkbLineString)
    # New edge attribute write support merged into edge loop
    fields = {}
    attributes = {}
    OGRTypes = {int:ogr.OFTInteger, str:ogr.OFTString, float:ogr.OFTReal}
    for e in G.edges(data=True):
        data = G.get_edge_data(*e)
        g = netgeometry(e, data)
        # Loop through data in edges
        for key, data in e[2].iteritems():
            # Reject data not for attribute table
            if (key != 'Json' and key != 'Wkt' and key != 'Wkb' 
                and key != 'ShpName'):
                  # Add new attributes for each feature
                  if key not in fields:
                     if type(data) in OGRTypes:
                         fields[key] = OGRTypes[type(data)]
                     else:
                         fields[key] = ogr.OFTString
                     newfield = ogr.FieldDefn(key, fields[key])
                     edges.CreateField(newfield)
                     attributes[key] = data
                  # Create dict of single feature's attributes
                  else:
                     attributes[key] = data
         # Create the feature with attributes
        create_feature(g, edges, attributes)
    nodes, edges = None, None



##############################################################################


cap_fc = [1,2,4,8,24,48,96,144] #fibres/cable
cap_cs = [1] #cable/subduct
cap_sd = [7,24] #subduct/duct
cap_d = [1]
cap_list = [cap_fc,cap_cs,cap_sd,cap_d]
cap_fc_cost = [1.0,1.08,1.15,1.2,1.24,1.3,1.4,1.48]
cap_cs_cost = [0.8] 
cap_sd_cost = [2,3]
cap_d_cost = [1]
cap_list_cost = [cap_fc_cost,cap_cs_cost,cap_sd_cost,cap_d_cost]


##diadikasia clustering#######################################################


##############################################


#to comP einai ekeino apo to em-clustering
def a_emsp02(G,k_init,cs):
	#k_init = 6
	P_init = graph_c_vec(G)[:]
	P0 = P_init[:]
	k0 = k_init
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	#for i in range(k0): #creates k0-clusters
	#	Call.insert(0,[])
	G0 = G
	#Points, input for clustering, thelei update kathe fora
	P00 = [] 
	for i in P_init: #we take each time the 1st cluster of em-clustering
		P00.append((i[0],i[1]))
	k = k_init  # #Clusters, input for clustering, thelei update kathe fora
	while k != 1:
		#em-clustering
		aman0 = a_emCOa_2nd_G(G0, k, 0, 1, 500) 
		aman1 = aman0[0][:]
		#creates nodes from cluster
		l_nodes = [] 
		for i in aman1[0]: #we take each time the 1st cluster of em-clustering
			l_nodes.append((i[0],i[1]))
		#define the graph
		gg = G.subgraph(l_nodes)
		#comP
		#comP = centerofmass_graph(gg)
		comP = aman0[1][0]
		#take all sps from comP
		l_paths0 = nx.single_source_dijkstra_path_length(G,comP)
		#creates the pairs [node,sp-distance from comP]
		l = []
		for n in gg.nodes():
			l.append([n,l_paths0[n]])
		#ordering from min -> max sp-distance
		from operator import itemgetter, attrgetter
		sorted_l = sorted(l, key=itemgetter(1))
		#filling up the sp-cluster
		cl_nodes = [] #nodes of the cluster
		s_nodes = 0
		for lmnt in sorted_l:
			if gg.node[lmnt[0]]['population'] != -1 and s_nodes + gg.node[lmnt[0]]['population'] <= max_plith:
				s_nodes = s_nodes + gg.node[lmnt[0]]['population']
				cl_nodes.append(lmnt[0])
				P00.remove(lmnt[0])
		#save the cluster
		Call.append(cl_nodes)
		#defining the new G0
		G0 = G.subgraph(P00)
		#defining the new number of clusters for G0
		k = k-1
	Call.append(P00)
	#normalize
	m = 1
	while len(Call)-m != 0:
		for i in range(len(Call)-m):
			norm_cl(Call[len(Call)-m],Call[i],cs)
		m = m + 1
	Call0 = []
	for c in Call:
		ggg = G.subgraph(c) ###
		comPP = centerofmass0(G,c)
		ll_paths = nx.single_source_dijkstra_path(G,comPP) ###
		alll_nodes = []
		for n in ggg.nodes():
			alll_nodes.append(ll_paths[n])
		end_listt = []
		for i in alll_nodes:
			for j in i:
				if j not in end_listt:
					end_listt.append(j)
		lll0 = end_listt[:]
		for p in lll0:
			if p not in c:
				c.append(p)
	#save the cluster
		Call0.append(c)
	return Call0



#to comP einai ekeino apo to em-clustering
def a_emsp02a(G,k_init,cs): # a_emsp02a(G,k_init,cs,about_coms):
	#k_init = 6
	P_init = graph_c_vec(G)[:]
	P0 = P_init[:]
	k0 = k_init
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	#max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	max_plith = cluster_plith_max
	Call = [] #store the clusters we find
	#for i in range(k0): #creates k0-clusters
	#	Call.insert(0,[])
	G0 = G
	#Points, input for clustering, thelei update kathe fora
	P00 = [] 
	for i in P_init: #we take each time the 1st cluster of em-clustering
		P00.append((i[0],i[1]))
	k = k_init  # #Clusters, input for clustering, thelei update kathe fora
	while k != 1:
		#em-clustering
		aman0 = a_emCOa_2nd_G(G0, k, 0, 1, 50) #a_emCOa_2nd_G(g, 6, 0, 0, 50) 
		aman1 = aman0[0][:]
		#creates nodes from cluster
		l_nodes = [] 
		for i in aman1[0]: #we take each time the 1st cluster of em-clustering
			l_nodes.append((i[0],i[1]))
		#define the graph
		gg = G.subgraph(l_nodes)
		#comP
		#comP = centerofmass_graph(gg)
		comP = aman0[1][0]
		#take all sps from comP
		l_paths0 = nx.single_source_dijkstra_path_length(G,comP)
		#creates the pairs [node,sp-distance from comP]
		l = []
		for n in gg.nodes():
			l.append([n,l_paths0[n]])
		#ordering from min -> max sp-distance
		from operator import itemgetter, attrgetter
		sorted_l = sorted(l, key=itemgetter(1))
		#filling up the sp-cluster
		cl_nodes = [] #nodes of the cluster
		s_nodes = 0
		for lmnt in sorted_l:
			if gg.node[lmnt[0]]['population'] != -1 and s_nodes + gg.node[lmnt[0]]['population'] <= max_plith:
				s_nodes = s_nodes + gg.node[lmnt[0]]['population']
				cl_nodes.append(lmnt[0])
				P00.remove(lmnt[0])
		#save the cluster
		Call.append(cl_nodes)
		#defining the new G0
		G0 = G.subgraph(P00)
		#defining the new number of clusters for G0
		k = k-1
	Call.append(P00)
	#normalize
	m = 1
	while len(Call)-m != 0:
		for i in range(len(Call)-m):
			norm_cl(Call[len(Call)-m],Call[i],cs)
		m = m + 1
	Call0 = []
	for c in Call:
		ggg = G.subgraph(c) ###
		comPP = centerofmass0(G,c)
		ll_paths = nx.single_source_dijkstra_path(G,comPP) ###
		alll_nodes = []
		for n in ggg.nodes():
			alll_nodes.append(ll_paths[n])
		end_listt = []
		for i in alll_nodes:
			for j in i:
				if j not in end_listt:
					end_listt.append(j)
		lll0 = end_listt[:]
		for p in lll0:
			if p not in c:
				c.append(p)
		#save the cluster
		Call0.append(c)
	Clusters = []
	for c in Call0:
		cl = []
		for i in c:
			if G.node[i]['population'] != -1:
				cl.append([i[0],i[1]])
		Clusters.append(cl)
	return [Clusters,0,max_plith]


##############################################################################



#to comP einai ekeino apo to em-clustering
def a_emsp02a_norm(G,k_init,cs):
	#k_init = 6
	P_init = graph_c_vec(G)[:]
	P0 = P_init[:]
	k0 = k_init
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	#for i in range(k0): #creates k0-clusters
	#	Call.insert(0,[])
	G0 = G
	#Points, input for clustering, thelei update kathe fora
	P00 = [] 
	for i in P_init: #we take each time the 1st cluster of em-clustering
		P00.append((i[0],i[1]))
	k = k_init  # #Clusters, input for clustering, thelei update kathe fora
	while k != 1:
		#em-clustering
		aman0 = a_emCOa_2nd_G(G0, k, 1, 1, 50) #aman0 = a_emCOa_2nd_G(g, 6, 0, 1, 50)
		aman1 = aman0[0][:]
		########################################################################
		alphagco = []
		for cl in aman1:
			cl_list = []
			for i in cl:
				cl_list.append([i[0],i[1]])
			alphagco.append(cl_list)
		cls = alphagco[:]
		error_nodes_list = normalize_error_nodes(G,g,alphagco)[:] #0
		cls0 = norm_error_nodes(G,g,cls,error_nodes_list) 
		########################################################################
		#creates nodes from cluster
		l_nodes = [] 
		#for i in aman1[0]: #we take each time the 1st cluster of em-clustering
		for i in cls0[0]:
			l_nodes.append((i[0],i[1]))
		#define the graph
		gg = G.subgraph(l_nodes)
		comP = centerofmass_graph0(gg)
		#comP = aman0[1][0]
		#take all sps from comP
		l_paths0 = nx.single_source_dijkstra_path_length(G,comP)
		#creates the pairs [node,sp-distance from comP]
		l = []
		for n in gg.nodes():
			l.append([n,l_paths0[n]])
		#ordering from min -> max sp-distance
		from operator import itemgetter, attrgetter
		sorted_l = sorted(l, key=itemgetter(1))
		#filling up the sp-cluster
		cl_nodes = [] #nodes of the cluster
		s_nodes = 0
		for lmnt in sorted_l:
			if gg.node[lmnt[0]]['population'] != -1 and s_nodes + gg.node[lmnt[0]]['population'] <= max_plith:
				s_nodes = s_nodes + gg.node[lmnt[0]]['population']
				cl_nodes.append(lmnt[0])
				P00.remove(lmnt[0])
		#save the cluster
		Call.append(cl_nodes)
		#defining the new G0
		G0 = G.subgraph(P00)
		#defining the new number of clusters for G0
		k = k-1
	Call.append(P00)
	#normalize
	m = 1
	while len(Call)-m != 0:
		for i in range(len(Call)-m):
			norm_cl(Call[len(Call)-m],Call[i],cs)
		m = m + 1
	Call0 = []
	for c in Call:
		ggg = G.subgraph(c) ###
		comPP = centerofmass0(G,c)
		ll_paths = nx.single_source_dijkstra_path(G,comPP) ###
		alll_nodes = []
		for n in ggg.nodes():
			alll_nodes.append(ll_paths[n])
		end_listt = []
		for i in alll_nodes:
			for j in i:
				if j not in end_listt:
					end_listt.append(j)
		lll0 = end_listt[:]
		for p in lll0:
			if p not in c:
				c.append(p)
		#save the cluster
		Call0.append(c)
	Clusters = []
	for c in Call0:
		cl = []
		for i in c:
			if G.node[i]['population'] != -1:
				cl.append([i[0],i[1]])
		Clusters.append(cl)
	return [Clusters,0,max_plith]

##############################################################################


#to comP einai ekeino apo to em-clustering
def a_emsp02a_far(G,k_init,cs):
	#k_init = 6
	P_init = graph_c_vec(G)[:]
	P0 = P_init[:]
	k0 = k_init
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	#for i in range(k0): #creates k0-clusters
	#	Call.insert(0,[])
	G0 = G
	#Points, input for clustering, thelei update kathe fora
	P00 = [] 
	for i in P_init: #we take each time the 1st cluster of em-clustering
		P00.append((i[0],i[1]))
	k = k_init  # #Clusters, input for clustering, thelei update kathe fora
	while k != 1:
		#em-clustering
		aman0 = a_emCOa_2nd_G(G0, k, 0, 1, 50) #aman0 = a_emCOa_2nd_G(g, 6, 0, 1, 50)
		aman1 = aman0[0][:]
		########################################################################
		alphagco = []
		for cl in aman1:
			cl_list = []
			for i in cl:
				cl_list.append([i[0],i[1]])
			alphagco.append(cl_list)
		cls = alphagco[:]
		#error_nodes_list = normalize_error_nodes(G,g,alphagco)[:] #0
		#cls0 = norm_error_nodes(G,g,cls,error_nodes_list) 
		########################################################################
		coms_list = []
		for c in cls:
			coms_list.append(centerofmass(c))
		sp_list = []
		for i in coms_list:
			sp_list.append([i,nx.dijkstra_path_length(G, centerofmass_graph0(G), i) ])
		from operator import itemgetter, attrgetter
		sorted_sp_list = sorted(sp_list, key=itemgetter(1))
		cls0 = cls[coms_list.index(sorted_sp_list[len(cls)-1][0])]
		#creates nodes from cluster
		l_nodes = [] 
		#for i in aman1[0]: #we take each time the 1st cluster of em-clustering
		for i in cls0:
			l_nodes.append((i[0],i[1]))
		#define the graph
		gg = G.subgraph(l_nodes)
		comP = centerofmass_graph0(gg)
		#comP = aman0[1][0]
		#take all sps from comP
		l_paths0 = nx.single_source_dijkstra_path_length(G,comP)
		#creates the pairs [node,sp-distance from comP]
		l = []
		for n in gg.nodes():
			l.append([n,l_paths0[n]])
		#ordering from min -> max sp-distance
		from operator import itemgetter, attrgetter
		sorted_l = sorted(l, key=itemgetter(1))
		#filling up the sp-cluster
		cl_nodes = [] #nodes of the cluster
		s_nodes = 0
		for lmnt in sorted_l:
			if gg.node[lmnt[0]]['population'] != -1 and s_nodes + gg.node[lmnt[0]]['population'] <= max_plith:
				s_nodes = s_nodes + gg.node[lmnt[0]]['population']
				cl_nodes.append(lmnt[0])
				P00.remove(lmnt[0])
		#save the cluster
		Call.append(cl_nodes)
		#defining the new G0
		G0 = G.subgraph(P00)
		#defining the new number of clusters for G0
		k = k-1
	Call.append(P00)
	#normalize
	m = 1
	while len(Call)-m != 0:
		for i in range(len(Call)-m):
			norm_cl(Call[len(Call)-m],Call[i],cs)
		m = m + 1
	Call0 = []
	for c in Call:
		ggg = G.subgraph(c) ###
		comPP = centerofmass0(G,c)
		ll_paths = nx.single_source_dijkstra_path(G,comPP) ###
		alll_nodes = []
		for n in ggg.nodes():
			alll_nodes.append(ll_paths[n])
		end_listt = []
		for i in alll_nodes:
			for j in i:
				if j not in end_listt:
					end_listt.append(j)
		lll0 = end_listt[:]
		for p in lll0:
			if p not in c:
				c.append(p)
		#save the cluster
		Call0.append(c)
	Clusters = []
	for c in Call0:
		cl = []
		for i in c:
			if G.node[i]['population'] != -1:
				cl.append([i[0],i[1]])
		Clusters.append(cl)
	return [Clusters,0,max_plith]


##############################################################################

#to comP einai ekeino apo to em-clustering
def a_emsp02a_farem(G,k_init,cs):
	#k_init = 6
	P_init = graph_c_vec(G)[:]
	P0 = P_init[:]
	k0 = k_init
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	#for i in range(k0): #creates k0-clusters
	#	Call.insert(0,[])
	G0 = G
	#Points, input for clustering, thelei update kathe fora
	P00 = [] 
	for i in P_init: #we take each time the 1st cluster of em-clustering
		P00.append((i[0],i[1]))
	k = k_init  # #Clusters, input for clustering, thelei update kathe fora
	while k != 1:
		#em-clustering
		aman0 = a_emCOa_2nd_G(G0, k, 0, 1, 50) #aman0 = a_emCOa_2nd_G(g, 6, 0, 1, 50)
		aman1 = aman0[0][:]
		########################################################################
		alphagco = []
		for cl in aman1:
			cl_list = []
			for i in cl:
				cl_list.append([i[0],i[1]])
			alphagco.append(cl_list)
		cls = alphagco[:]
		#error_nodes_list = normalize_error_nodes(G,g,alphagco)[:] #0
		#cls0 = norm_error_nodes(G,g,cls,error_nodes_list) 
		########################################################################
		coms_list = []
		for c in cls:
			coms_list.append(centerofmass(c))
		sp_list = []
		for i in coms_list:
			#sp_list.append([i,nx.dijkstra_path_length(G, centerofmass_graph0(G), i) ])
			sp_list.append([i,adistance(centerofmass_graph0(G), i) ])
		from operator import itemgetter, attrgetter
		sorted_sp_list = sorted(sp_list, key=itemgetter(1))
		cls0 = cls[coms_list.index(sorted_sp_list[len(cls)-1][0])]
		#creates nodes from cluster
		l_nodes = [] 
		#for i in aman1[0]: #we take each time the 1st cluster of em-clustering
		for i in cls0:
			l_nodes.append((i[0],i[1]))
		#define the graph
		gg = G.subgraph(l_nodes)
		comP = centerofmass_graph0(gg)
		#comP = aman0[1][0]
		#take all sps from comP
		l_paths0 = nx.single_source_dijkstra_path_length(G,comP)
		#creates the pairs [node,sp-distance from comP]
		l = []
		for n in gg.nodes():
			l.append([n,l_paths0[n]])
		#ordering from min -> max sp-distance
		from operator import itemgetter, attrgetter
		sorted_l = sorted(l, key=itemgetter(1))
		#filling up the sp-cluster
		cl_nodes = [] #nodes of the cluster
		s_nodes = 0
		for lmnt in sorted_l:
			if gg.node[lmnt[0]]['population'] != -1 and s_nodes + gg.node[lmnt[0]]['population'] <= max_plith:
				s_nodes = s_nodes + gg.node[lmnt[0]]['population']
				cl_nodes.append(lmnt[0])
				P00.remove(lmnt[0])
		#save the cluster
		Call.append(cl_nodes)
		#defining the new G0
		G0 = G.subgraph(P00)
		#defining the new number of clusters for G0
		k = k-1
	Call.append(P00)
	#normalize
	m = 1
	while len(Call)-m != 0:
		for i in range(len(Call)-m):
			norm_cl(Call[len(Call)-m],Call[i],cs)
		m = m + 1
	Call0 = []
	for c in Call:
		ggg = G.subgraph(c) ###
		comPP = centerofmass0(G,c)
		ll_paths = nx.single_source_dijkstra_path(G,comPP) ###
		alll_nodes = []
		for n in ggg.nodes():
			alll_nodes.append(ll_paths[n])
		end_listt = []
		for i in alll_nodes:
			for j in i:
				if j not in end_listt:
					end_listt.append(j)
		lll0 = end_listt[:]
		for p in lll0:
			if p not in c:
				c.append(p)
		#save the cluster
		Call0.append(c)
	Clusters = []
	for c in Call0:
		cl = []
		for i in c:
			if G.node[i]['population'] != -1:
				cl.append([i[0],i[1]])
		Clusters.append(cl)
	return [Clusters,0,max_plith]


##############################################################################




#c einai i aktina
def norm_cl(cluster_null,cluster,c):
	cl_null = cluster_null[:]
	cl = cluster[:]
	for i in cl_null:
		for j in cl:
			s = []
			if adistance(i,j) < c:
				s.append(j)
			for k in s:
				if k in cl:
					cluster.append(i)
					if i in cluster_null:
						cluster_null.remove(i)





#after clustering we accept All the lmnts with the same block_id to belong to the cluster
def cluster_blocks(G,cluster):
	l_ids = []
	#creates list with all block ids
	for n in cluster:
		l = (n[0],n[1])
		l_ids.append(G.node[l]['block_id'])
	new_l = []
	for i in l_ids:
		if i not in new_l:
			new_l.append(i)
	#creates empty lists
	list_ids = []
	for j in range(len(new_l)):
		list_ids.insert(0,[])
	#put nodes to lists according to their block_id
	for ii in new_l:
		for nn in G.nodes():
			if G.node[nn]['block_id'] == ii:
				list_ids[new_l.index(ii)].append(nn)
	clu = []
	for ll in list_ids:
		for a in ll:
			clu.append([a[0],a[1]])
	return clu




#after clustering we accept All the lmnts with the same block_id to belong to the cluster
def cluster_blocks0(G,cluster,cl_mass):
	l_ids = []
	#creates list with all block ids
	for n in cluster:
		l = (n[0],n[1])
		l_ids.append(G.node[l]['block_id'])
	new_l = []
	for i in l_ids:
		if i not in new_l:
			new_l.append(i)
	#creates empty lists
	list_ids = []
	for j in range(len(new_l)):
		list_ids.insert(0,[])




#	#put nodes to lists according to their block_id
#	for ii in new_l:
#		for nn in G.nodes():
#			if G.node[nn]['block_id'] == ii:
#				list_ids[new_l.index(ii)].append(nn)
#	clu = []
#	for ll in list_ids:
#		for a in ll:
#			clu.append([a[0],a[1]])
#	return clu



population_to_int(G)


#maybe add the vars that have to do with the way the clusters are filled in 
def a_emsp_b(G,k,about_coms):
	Clusters = []
	g0 = G
	while k != 1:
		print k
		#aman0 = a_emCOa_2nd_G(g0, k , 0, 1, 500)
		aman0 = a_emsp02a(g0,k,0,about_coms)[:] #this to work needs centerofmass diff!!!
		cluster = aman0[0][0][:]
		#lmnts of all clusters
		P_all = []
		for c in aman0[0]:
			for i in c:
				P_all.append([i[0],i[1]])
		#plith_cl = aman0[2] #xreiazomaste ton plithismo tou cluster
		l_nodes = []
		for i in aman0[0][0]:
			l_nodes.append((i[0],i[1]))
		gg = G.subgraph(l_nodes)
		#comP = centerofmass_graph(gg)
		comP = centerofmass0(G,l_nodes)
		l_paths = nx.single_source_dijkstra_path(G,comP)
		all_nodes = []
		for n in gg.nodes():
			all_nodes.append(l_paths[n])
		end_list = []
		for i in all_nodes:
			for j in i:
				if j not in end_list:
					end_list.append(j)
		ll0 = end_list[:]
		population_to_int(G)
		set_new_attribute_to_nodes(G,'sucgload',[0,0])
		set_new_attribute_to_nodes(G,'suc2gload',[0,0])
		set_new_attribute_to_nodes(G,'sucggload',[0,0])
		set_new_attribute_to_nodes(G,'root_node', 0)
		g = G.subgraph(ll0)
		cutoff_null_leafs0(g)
		for e in g.edges():
			g_e = g[e[0]][e[1]]
			g_e['grans'] = {}
			g_e['ALPHA'] = {}
			g_e['grans_f'] = {}
			g_e['grans_c'] = {}
			g_e['grans_s'] = {}
			g_e['grans_d'] = {}
			g_e['dum_cost'] = 0
			g_e['gr_cost'] = 0
			g_e['tr_cost'] = 0
			g_e['dum_cost'] = 0
			g_e['efficiency'] = 0
		#finds dhn of cluster
		#comPP = centerofmass_graph(g) #choose either this or aman0[0][1]
		#comPP = aman0[1][0]
		#for n in g.neighbors(comPP):
		#	if g.node[n]['population'] == -1:
		#		dhn = n
		#big70 = graph_blocks70(G,G,dhn,plith_cl)[:]
		#lmnts of the cluster after big70
		lmnts70 = cluster_blocks(G,cluster)[:]
		Clusters.append(lmnts70)
		#update P_all
		for i in lmnts70:
			if i in P_all:
				P_all.remove(i)
		#gives the lmnts the form of 3ada
		P_a = []
		for p in P_all:
			pp = (p[0],p[1])
			P_a.append((pp[0],pp[1],G.node[pp]['population']))
		g0 = cluster_to_subgraph(G,P_a)[0]  #
		k = k -1
		print "end of: ", k + 1
	Clusters.append(P_all)
	return Clusters



#maybe add the vars that have to do with the way the clusters are filled in 
#mass error correction. still has some problems :P
def a_emsp_b0(G,k):
	#computes the G_mass
	s = 0
	for n in G.nodes():
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	#computes the init_cluster_mass
	cl_mass_init = s/k
	plith_cl = cl_mass_init*1.02 #error correction cluster mass
	Clusters = []
	g0 = G
	while k != 1:
		print k
		#aman0 = a_emCOa_2nd_G(g0, k , 0, 1, 500)
		aman0 = a_emsp02a(g0,k,0)[:] #this to work needs centerofmass diff!!!
		cluster = aman0[0][0][:]
		#lmnts of all clusters
		P_all = []
		for c in aman0[0]:
			for i in c:
				P_all.append([i[0],i[1]])
		#plith_cl = aman0[2] #xreiazomaste ton plithismo tou cluster
		l_nodes = []
		for i in aman0[0][0]:
			l_nodes.append((i[0],i[1]))
		gg = G.subgraph(l_nodes)
		#comP = centerofmass_graph(gg)
		comP = centerofmass0(G,l_nodes)
		dhn = comP
		l_paths = nx.single_source_dijkstra_path(G,comP)
		all_nodes = []
		for n in gg.nodes():
			all_nodes.append(l_paths[n])
		end_list = []
		for i in all_nodes:
			for j in i:
				if j not in end_list:
					end_list.append(j)
		ll0 = end_list[:]
		population_to_int(G)
		set_new_attribute_to_nodes(G,'sucgload',[0,0])
		set_new_attribute_to_nodes(G,'suc2gload',[0,0])
		set_new_attribute_to_nodes(G,'sucggload',[0,0])
		set_new_attribute_to_nodes(G,'root_node', 0)
		g = G.subgraph(ll0)
		cutoff_null_leafs0(g)
		for e in g.edges():
			g_e = g[e[0]][e[1]]
			g_e['grans'] = {}
			g_e['ALPHA'] = {}
			g_e['grans_f'] = {}
			g_e['grans_c'] = {}
			g_e['grans_s'] = {}
			g_e['grans_d'] = {}
			g_e['dum_cost'] = 0
			g_e['gr_cost'] = 0
			g_e['tr_cost'] = 0
			g_e['dum_cost'] = 0
			g_e['efficiency'] = 0
		#finds dhn of cluster
		#comPP = centerofmass_graph(g) #choose either this or aman0[0][1]
		#for n in g.neighbors(comPP):
		#	if g.node[n]['population'] == -1:
		#		dhn = n
		big70 = graph_blocks700(G,dhn,plith_cl)[:]
		#big70 = graph_blocks70(G,G,dhn,plith_cl)[:]
		lmnts_list = []
		for b in big70:
			for lmn in b[1]:
				n = [lmn[0],lmn[1]]
				lmnts_list.append(n)
		lmnts70 = lmnts_list[:]
		#lmnts70 = cluster_blocks(G,big70)[:]
		#lmnts of the cluster after big70
		#lmnts70 = cluster_blocks(G,cluster)[:]
		Clusters.append(lmnts70)
		#update P_all
		for i in lmnts70:
			if i in P_all:
				P_all.remove(i)
		#gives the lmnts the form of 3ada
		P_a = []
		for p in P_all:
			pp = (p[0],p[1])
			P_a.append((pp[0],pp[1],G.node[pp]['population']))
		g0 = cluster_to_subgraph(G,P_a)[0]  #
		k = k -1
		print "end of: ", k + 1
	Clusters.append(P_all)
	return Clusters


#maybe add the vars that have to do with the way the clusters are filled in 
def a_emsp_b00a(G,k):
	#computes the G_mass
	s = 0
	for n in G.nodes():
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	#computes the init_cluster_mass
	cl_mass_init = s/k
	plith_cl = cl_mass_init*1.02 #error correction cluster mass
	Clusters = []
	g0 = G
	while k != 1:
		print k
		#aman0 = a_emCOa_2nd_G(g0, k , 0, 1, 500)
		aman0 = a_emsp02a(g0,k,0)[:] #this to work needs centerofmass diff!!!
		cluster = aman0[0][k-1][:]
		#lmnts of all clusters
		P_all = []
		for c in aman0[0]:
			for i in c:
				P_all.append([i[0],i[1]])
		#plith_cl = aman0[2] #xreiazomaste ton plithismo tou cluster
		l_nodes = []
		for i in aman0[0][0]:
			l_nodes.append((i[0],i[1]))
		gg = G.subgraph(l_nodes)
		comP = centerofmass_graph0(gg)
		dhn = comP
		l_paths = nx.single_source_dijkstra_path(G,comP)
		all_nodes = []
		for n in gg.nodes():
			all_nodes.append(l_paths[n])
		end_list = []
		for i in all_nodes:
			for j in i:
				if j not in end_list:
					end_list.append(j)
		ll0 = end_list[:]
		population_to_int(G)
		set_new_attribute_to_nodes(G,'sucgload',[0,0])
		set_new_attribute_to_nodes(G,'suc2gload',[0,0])
		set_new_attribute_to_nodes(G,'sucggload',[0,0])
		set_new_attribute_to_nodes(G,'root_node', 0)
		g = G.subgraph(ll0)
		cutoff_null_leafs0(g)
		for e in g.edges():
			g_e = g[e[0]][e[1]]
			g_e['grans'] = {}
			g_e['ALPHA'] = {}
			g_e['grans_f'] = {}
			g_e['grans_c'] = {}
			g_e['grans_s'] = {}
			g_e['grans_d'] = {}
			g_e['dum_cost'] = 0
			g_e['gr_cost'] = 0
			g_e['tr_cost'] = 0
			g_e['dum_cost'] = 0
			g_e['efficiency'] = 0
		#finds dhn of cluster
		#comPP = centerofmass_graph(g) #choose either this or aman0[0][1]
		#for n in g.neighbors(comPP):
		#	if g.node[n]['population'] == -1:
		#		dhn = n
		big70 = graph_blocks700(G,dhn,plith_cl)[:]
		#big70 = graph_blocks70(G,G,dhn,plith_cl)[:]
		lmnts_list = []
		for b in big70:
			for lmn in b[1]:
				n = [lmn[0],lmn[1]]
				lmnts_list.append(n)
		lmnts70 = lmnts_list[:]
		#lmnts70 = cluster_blocks(G,big70)[:]
		#lmnts of the cluster after big70
		#lmnts70 = cluster_blocks(G,cluster)[:]
		Clusters.append(lmnts70)
		#update P_all
		for i in lmnts70:
			if i in P_all:
				P_all.remove(i)
		#gives the lmnts the form of 3ada
		P_a = []
		for p in P_all:
			pp = (p[0],p[1])
			P_a.append((pp[0],pp[1],G.node[pp]['population']))
		g0 = cluster_to_subgraph(G,P_a)[0]  #
		k = k -1
		print "end of: ", k + 1
	Clusters.append(P_all)
	return Clusters



#maybe add the vars that have to do with the way the clusters are filled in 
def a_emsp_b00(G,k):
	#computes the G_mass
	s = 0
	for n in G.nodes():
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	#computes the init_cluster_mass
	cl_mass_init = s/k
	plith_cl = cl_mass_init*1.02 #error correction cluster mass
	Clusters = []
	g0 = G
	while k != 1:
		print k
		#aman0 = a_emCOa_2nd_G(g0, k , 0, 1, 500)
		aman0 = a_emsp02a(g0,k,0)[:] #this to work needs centerofmass diff!!!
		cluster = aman0[0][0][:]
		#lmnts of all clusters
		P_all = []
		for c in aman0[0]:
			for i in c:
				P_all.append([i[0],i[1]])
		#plith_cl = aman0[2] #xreiazomaste ton plithismo tou cluster
		l_nodes = []
		for i in aman0[0][0]:
			l_nodes.append((i[0],i[1]))
		gg = G.subgraph(l_nodes)
		#comP = centerofmass_graph(gg)
		comP = centerofmass0(G,l_nodes)
		#anti gia to comP os dhn, tha pairnei to node pou einai pio makria em apo to comP
		l_nodes_dis = []
		for ii in l_nodes:
			l_nodes_dis.append([ii,adistance(ii,comP)])
		from operator import itemgetter, attrgetter
		sorted_l_nodes_dis = sorted(l_nodes_dis, key=itemgetter(1))
		dhn0 = sorted_l_nodes_dis[len(sorted_l_nodes_dis)-1][0]
		if G.node[dhn0]['population'] == -1:
			dhn = dhn0
		else:
			dhn = G.neighbors(dhn0)[0]
		#dhn = comP
		l_paths = nx.single_source_dijkstra_path(G,comP)
		all_nodes = []
		for n in gg.nodes():
			all_nodes.append(l_paths[n])
		end_list = []
		for i in all_nodes:
			for j in i:
				if j not in end_list:
					end_list.append(j)
		ll0 = end_list[:]
		population_to_int(G)
		set_new_attribute_to_nodes(G,'sucgload',[0,0])
		set_new_attribute_to_nodes(G,'suc2gload',[0,0])
		set_new_attribute_to_nodes(G,'sucggload',[0,0])
		set_new_attribute_to_nodes(G,'root_node', 0)
		g = G.subgraph(ll0)
		cutoff_null_leafs0(g)
		for e in g.edges():
			g_e = g[e[0]][e[1]]
			g_e['grans'] = {}
			g_e['ALPHA'] = {}
			g_e['grans_f'] = {}
			g_e['grans_c'] = {}
			g_e['grans_s'] = {}
			g_e['grans_d'] = {}
			g_e['dum_cost'] = 0
			g_e['gr_cost'] = 0
			g_e['tr_cost'] = 0
			g_e['dum_cost'] = 0
			g_e['efficiency'] = 0
		#finds dhn of cluster
		#comPP = centerofmass_graph(g) #choose either this or aman0[0][1]
		#for n in g.neighbors(comPP):
		#	if g.node[n]['population'] == -1:
		#		dhn = n
		big70 = graph_blocks700(G,dhn,plith_cl)[:]
		#big70 = graph_blocks70(G,G,dhn,plith_cl)[:]
		lmnts_list = []
		for b in big70:
			for lmn in b[1]:
				n = [lmn[0],lmn[1]]
				lmnts_list.append(n)
		lmnts70 = lmnts_list[:]
		#lmnts70 = cluster_blocks(G,big70)[:]
		#lmnts of the cluster after big70
		#lmnts70 = cluster_blocks(G,cluster)[:]
		Clusters.append(lmnts70)
		#update P_all
		for i in lmnts70:
			if i in P_all:
				P_all.remove(i)
		#gives the lmnts the form of 3ada
		P_a = []
		for p in P_all:
			pp = (p[0],p[1])
			P_a.append((pp[0],pp[1],G.node[pp]['population']))
		g0 = cluster_to_subgraph(G,P_a)[0]  #
		k = k -1
		print "end of: ", k + 1
	Clusters.append(P_all)
	return Clusters




#maybe add the vars that have to do with the way the clusters are filled in 
def a_emsp_b000(G,k):
	#computes the G_mass
	s = 0
	for n in G.nodes():
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	#computes the init_cluster_mass
	cl_mass_init = s/k
	plith_cl = cl_mass_init*1.02 #error correction cluster mass
	Clusters = []
	g0 = G
	while k != 1:
		print k
		#aman0 = a_emCOa_2nd_G(g0, k , 0, 1, 500)
		#aman0 = a_emsp02a(g0,k,0)[:] #this to work needs centerofmass diff!!!
		#cluster = aman0[0][0][:]
		aman0 = a_emsp_b(g0,k)[0]
		#lmnts of all clusters
		P_all = []
		for i in aman0:
			P_all.append([i[0],i[1]])
		#plith_cl = aman0[2] #xreiazomaste ton plithismo tou cluster
		l_nodes = []
		for i in aman0:
			l_nodes.append((i[0],i[1]))
		gg = G.subgraph(l_nodes)
		#comP = centerofmass_graph(gg)
		comP = centerofmass0(G,l_nodes)
		#anti gia to comP os dhn, tha pairnei to node pou einai pio makria em apo to comP
		l_nodes_dis = []
		for ii in l_nodes:
			l_nodes_dis.append([ii,adistance(ii,comP)])
		from operator import itemgetter, attrgetter
		sorted_l_nodes_dis = sorted(l_nodes_dis, key=itemgetter(1))
		dhn0 = sorted_l_nodes_dis[len(sorted_l_nodes_dis)-1][0]
		if G.node[dhn0]['population'] == -1:
			dhn = dhn0
		else:
			dhn = G.neighbors(dhn0)[0]
		#dhn = comP
		l_paths = nx.single_source_dijkstra_path(G,comP)
		all_nodes = []
		for n in gg.nodes():
			all_nodes.append(l_paths[n])
		end_list = []
		for i in all_nodes:
			for j in i:
				if j not in end_list:
					end_list.append(j)
		ll0 = end_list[:]
		population_to_int(G)
		set_new_attribute_to_nodes(G,'sucgload',[0,0])
		set_new_attribute_to_nodes(G,'suc2gload',[0,0])
		set_new_attribute_to_nodes(G,'sucggload',[0,0])
		set_new_attribute_to_nodes(G,'root_node', 0)
		g = G.subgraph(ll0)
		cutoff_null_leafs0(g)
		for e in g.edges():
			g_e = g[e[0]][e[1]]
			g_e['grans'] = {}
			g_e['ALPHA'] = {}
			g_e['grans_f'] = {}
			g_e['grans_c'] = {}
			g_e['grans_s'] = {}
			g_e['grans_d'] = {}
			g_e['dum_cost'] = 0
			g_e['gr_cost'] = 0
			g_e['tr_cost'] = 0
			g_e['dum_cost'] = 0
			g_e['efficiency'] = 0
		#finds dhn of cluster
		#comPP = centerofmass_graph(g) #choose either this or aman0[0][1]
		#for n in g.neighbors(comPP):
		#	if g.node[n]['population'] == -1:
		#		dhn = n
		big70 = graph_blocks700(G,dhn,plith_cl)[:]
		#big70 = graph_blocks70(G,G,dhn,plith_cl)[:]
		lmnts_list = []
		for b in big70:
			for lmn in b[1]:
				n = [lmn[0],lmn[1]]
				lmnts_list.append(n)
		lmnts70 = lmnts_list[:]
		#lmnts70 = cluster_blocks(G,big70)[:]
		#lmnts of the cluster after big70
		#lmnts70 = cluster_blocks(G,cluster)[:]
		Clusters.append(lmnts70)
		#update P_all
		for i in lmnts70:
			if i in P_all:
				P_all.remove(i)
		#gives the lmnts the form of 3ada
		P_a = []
		for p in P_all:
			pp = (p[0],p[1])
			P_a.append((pp[0],pp[1],G.node[pp]['population']))
		g0 = cluster_to_subgraph(G,P_a)[0]  #
		k = k -1
		print "end of: ", k + 1
	Clusters.append(P_all)
	return Clusters


##############################################################################

def a_graph_efficiency_inv(Gke,i_node,nu):
	G = Gke
	alpha = aprims_mst(G,'weight') #our spanning tree
	# define the mst graph
	GG=nx.Graph()
	#GG.add_edges_from(alpha)
	GG.add_nodes_from(G.nodes())
	#get node attributes info
	nx.set_node_attributes(GG,'population', nx.get_node_attributes(G,'population'))
	GG.add_edges_from(alpha)
	#give the weights
	for e in GG.edges():
		if e in G.edges():
			GG.add_edge(e[0],e[1],weight = G.edge[e[0]][e[1]]['weight'])
		if (e[1],e[0]) in G.edges():
			GG.add_edge(e[0],e[1],weight = G.edge[e[1]][e[0]]['weight'])
	#take all the sps from chosen init_node = 'O'
	init_node = i_node
	#to xreiazomaste k gia to cable cost!
	l = []
	for i in GG.nodes():
		if i != init_node:
			if nu == 0: #avoid null nodes!
				if GG.node[i]['population'] != -1: #avoid null nodes! (we can change it later and put 'population' =-1 and for the sum of loads if 'population' == -1 then 0 will be added to the sum)
					nL_ON = [] #first the nodes
					list_ON = nx.dijkstra_path(GG,init_node,i)[:]
					#now the edges of the path
					for ii in range(len(list_ON)-1):
						nL_ON.append((list_ON[ii],list_ON[ii+1]))
					l.append(nL_ON)
			if nu == 1: #accept all nodes!
				nL_ON = [] #first the nodes
				list_ON = nx.dijkstra_path(GG,init_node,i)[:]
				#now the edges of the path
				for ii in range(len(list_ON)-1):
					nL_ON.append((list_ON[ii],list_ON[ii+1]))
				l.append(nL_ON)
	#dimiourgoume lista pou periexei ola ta main paths! apo ton init_node
	list_all = []
	for k in range(len(GG.edges(init_node))):
		list_init = []
		for i in range(len(l)):
			for j in range(len(l[i])):
				if l[i][j][0] == init_node and l[i][j][1] == GG.edges(init_node)[k][1]:
					list_init.append(l[i])
		list_all.append(list_init)
	#sorted list_init
	lista_all = []
	for j in range(len(list_all)):
		lista_all.append(sorted(list_all[j]))
	#Given an INIT NODE 
	# ALL IN ONE STROKE!!!!!
	g= GG.nodes()
	g.remove(init_node)
	for iiii in g:
		#find subtrees of root
		root = iiii
		#search in main paths for root and returns the subtree of it
		#saves also the weight of its previous edge #! 
		root_list = []
		leafs_list = []
		previous_w = float(0)
		for i in range(len(lista_all)):
			for j in range(len(lista_all[i])):
				for k in range(len(lista_all[i][j])):
					if lista_all[i][j][k][0] == root:
						root_edge = lista_all[i][j][k-1] #i akmi tis opoias ypologizoume to edge_efficiency
						r_edge = root_edge #we use it later to define the efficiency
						for ii in range(lista_all[i][j].index(lista_all[i][j][k]),len(lista_all[i][j])):
							if lista_all[i][j][ii] not in root_list:
								root_list.append(lista_all[i][j][ii])
						previous_w = GG[lista_all[i][j][k-1][0]][lista_all[i][j][k-1][1]]['weight']
					if lista_all[i][j][len(lista_all[i][j])-1][1] == root: #leaf case
						root_edge_leaf = lista_all[i][j][len(lista_all[i][j])-1]
						leafs_list.append(root_edge_leaf)
		#to give the weight_info to an edge, we take the end node of it and compute the weight_of its subtree
		#and then add it to the weight of it
		#weight and load of the subtree (here weight is the distance between two consecutive nodes)
		subtree_w = float(0)
		load = float(0)
		load_list = []
		if root_list == []: #leaf case
			subtree_w = 0
			previous_w = GG[root_edge_leaf[0]][root_edge_leaf[1]]['weight']
			if GG.node[root_edge_leaf[0]]['population'] == -1: #dealing with null_nodes
				load = float(0 + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
			else:
				load = float(GG.node[root_edge_leaf[0]]['population'] + GG.node[root_edge_leaf[1]]['population'])
				r_edge = root_edge_leaf
		else:
			for i in range(len(root_list)):
				try:
					subtree_w = subtree_w + GG[root_list[i][0]][root_list[i][1]]['weight']
				except:
					print root_list[i]
				if root_list[i][0] not in load_list:
					if GG.node[root_list[i][0]]['population'] != -1:
						load = load + GG.node[root_list[i][0]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][0])
				if root_list[i][1] not in load_list:
					if GG.node[root_list[i][1]]['population'] != -1:
						load = load + GG.node[root_list[i][1]]['population']
					else:
						load = load + 0
					load_list.append(root_list[i][1])
		total_w = previous_w + subtree_w
		total_load = load
		#edge_efficiency = total_load / total_w #people/meters
		if total_load != 0 :
			edge_efficiency = float(total_w) / total_load #meters/people
		else:
			edge_efficiency = 0
		#gives to the edge the edge_efficiency!!!
		GG[r_edge[0]][r_edge[1]]['efficiency'] = edge_efficiency
		GG[r_edge[0]][r_edge[1]]['total_w'] = total_w
		GG[r_edge[0]][r_edge[1]]['total_load'] = total_load
	null_list = []
	for jk in GG.nodes(): #creates a list with null nodes
		if GG.node[jk]['population'] == -1:
			null_list.append(jk)
	return [lista_all,GG,leafs_list,null_list]

##############################################################################


#prepare the graph for perinv_cluster()
def cluster_to_subready(G,aman1):
	l_nodes = []
	for i in aman1:
		l_nodes.append((i[0],i[1]))
	gg = G.subgraph(l_nodes)
	#comP = centerofmass_graph(gg)
	comP = centerofmass0(G,l_nodes)
	l_paths = nx.single_source_dijkstra_path(G,comP)
	all_nodes = []
	for n in gg.nodes():
		all_nodes.append(l_paths[n])
	end_list = []
	for i in all_nodes:
		for j in i:
			if j not in end_list:
				end_list.append(j)
	ll0 = end_list[:]
	population_to_int(G)
	set_new_attribute_to_nodes(G,'sucgload',[0,0])
	set_new_attribute_to_nodes(G,'suc2gload',[0,0])
	set_new_attribute_to_nodes(G,'sucggload',[0,0])
	set_new_attribute_to_nodes(G,'root_node', 0)
	g = G.subgraph(ll0)
	cutoff_null_leafs0(g)
	for e in g.edges():
		g_e = g[e[0]][e[1]]
		g_e['grans'] = {}
		g_e['ALPHA'] = {}
		g_e['grans_f'] = {}
		g_e['grans_c'] = {}
		g_e['grans_s'] = {}
		g_e['grans_d'] = {}
		g_e['dum_cost'] = 0
		g_e['gr_cost'] = 0
		g_e['tr_cost'] = 0
		g_e['dum_cost'] = 0
		g_e['efficiency'] = 0
	return g

#arrange all leafs according to their edges eff
def leafs_f(gg):
	leafs_list = []
	for n in gg.nodes():
		if G.node[n]['population'] != -1:
			e = gg.edges(n)[0]
			leafs_list.append([n,gg[e[0]][e[1]]['efficiency']])
	from operator import itemgetter, attrgetter
	sorted_leafs_list = sorted(leafs_list, key=itemgetter(1))
	return sorted_leafs_list


#given the leaf_node with the worst efficiency computes the new efficiencys of its path if we cut it out
#moreover it removes the null_nodes from its path after the removing of itself.
def new_cluster_efs(gg,dhn,leaf_node,leaf_node_plith):
	gg_dipath, gg_dipath_nodes, dd_dipath_edges = path(gg,dhn,leaf_node) #path as DiGraph
	#computes the w2del
	w2del = leaf_node_plith
	a_node = leaf_node
	k = 0
	met = 1
	while k == 0:
		if gg_dipath.predecessors(a_node) != []:
			pre_a = gg_dipath.predecessors(a_node)[0]
			if gg.degree(pre_a) == 2:
				w2del = w2del + gg[pre_a][a_node]['weight']
				met = met + 1
				a_node = pre_a
			else:
				k = 1
		else:
			break
	#recalculate the vars
	for i in range(len(dd_dipath_edges)-met):
		e = dd_dipath_edges[i]
		gg[e[0]][e[1]]['total_w'] = gg[e[0]][e[1]]['total_w'] - w2del
		gg[e[0]][e[1]]['total_load'] = gg[e[0]][e[1]]['total_load'] - leaf_node_plith
		if gg[e[0]][e[1]]['total_load'] != 0 :
			gg[e[0]][e[1]]['efficiency'] = gg[e[0]][e[1]]['total_w']/gg[e[0]][e[1]]['total_load'] #meters/people
		else:
			edge_efficiency = 0
	#clean the null_nodes before leaf_node
	a = 0
	for i in range(met):
		a = a + 1
		if gg_dipath_nodes[len(gg_dipath_nodes)-a] != dhn:
			gg.remove_node(gg_dipath_nodes[len(gg_dipath_nodes)-a])
		#cutoff_null_leafs0(gg)



#given the leaf_node with the worst efficiency computes the new efficiencys of its path if we cut it out
#moreover it removes the null_nodes from its path after the removing of itself.
def new_cluster_efs22(gg,dhn,worst_fedge1,fedge_nodes_plith,fedge_subedges_weight,fedge_subedges):
	gg_dipath, gg_dipath_nodes, dd_dipath_edges = path(gg,dhn,worst_fedge1) #path as DiGraph
	#computes the w2del
	w2del = fedge_subedges_weight
	a_node = worst_fedge1
	k = 0
	met = 1
	while k == 0:
		if a_node in gg_dipath.nodes():
			if gg_dipath.predecessors(a_node) != []:
				pre_a = gg_dipath.predecessors(a_node)[0]
				if gg.degree(pre_a) == 2:
					w2del = w2del + gg[pre_a][a_node]['weight'] #???
					met = met + 1
					a_node = pre_a
				else:
					k = 1
			else:
				break
		else:
			break
	#recalculate the vars
	for i in range(len(dd_dipath_edges)-met):
		e = dd_dipath_edges[i]
		gg[e[0]][e[1]]['total_w'] = gg[e[0]][e[1]]['total_w'] - w2del
		gg[e[0]][e[1]]['total_load'] = gg[e[0]][e[1]]['total_load'] - fedge_nodes_plith
		if gg[e[0]][e[1]]['total_load'] != 0 :
			gg[e[0]][e[1]]['efficiency'] = gg[e[0]][e[1]]['total_w']/gg[e[0]][e[1]]['total_load'] #meters/people
		else:
			edge_efficiency = 0
	#remove fedge_subedges from gg
	for e in fedge_subedges:
		if e in gg.edges():
			gg.remove_edge(e[0],e[1])
		if (e[1],e[0]) in gg.edges():
			gg.remove_edge(e[1],e[0])
	#cutoff subedges_nodes
	for n in gg.nodes():
		if gg.degree(n) == 0:
			gg.remove_node(n)
	#clean the null_nodes before leaf_node
	#a = 0
	#for i in range(met):
	#	a = a + 1
	#	if gg_dipath_nodes[len(gg_dipath_nodes)-a] != dhn:
	#		gg.remove_node(gg_dipath_nodes[len(gg_dipath_nodes)-a])
	#	#cutoff_null_leafs0(gg)




#given the leaf_node with the worst efficiency computes the new efficiencys of its path if we cut it out
#moreover it removes the null_nodes from its path after the removing of itself.
def new_cluster_efs0(gg,dhn,leaf_node,leaf_node_plith):
	gg_dipath, gg_dipath_nodes, dd_dipath_edges = path(gg,dhn,leaf_node) #path as DiGraph
	#computes the w2del
	w2del = leaf_node_plith
	a_node = leaf_node
	k = 0
	met = 1
	while k == 0:
		if gg_dipath.predecessors(a_node) != []:
			pre_a = gg_dipath.predecessors(a_node)[0]
			if pre_a != dhn:
				if gg.degree(pre_a) == 2:
					w2del = w2del + gg[pre_a][a_node]['weight']
					met = met + 1
					a_node = pre_a
				else:
					k = 1
			else:
				w2del = w2del + gg[pre_a][a_node]['weight']
				met = met + 1
				k = 1
	#	else:
	#		break
	#recalculate the vars
	for i in range(len(dd_dipath_edges)-met):
		e = dd_dipath_edges[i]
		gg[e[0]][e[1]]['total_w'] = gg[e[0]][e[1]]['total_w'] - w2del
		gg[e[0]][e[1]]['total_load'] = gg[e[0]][e[1]]['total_load'] - leaf_node_plith
		if gg[e[0]][e[1]]['total_load'] != 0 :
			gg[e[0]][e[1]]['efficiency'] = gg[e[0]][e[1]]['total_w']/gg[e[0]][e[1]]['total_load'] #meters/people
		else:
			edge_efficiency = 0
	#clean the null_nodes before leaf_node
	a = 0
	for i in range(met):
		a = a + 1
		if gg_dipath_nodes[len(gg_dipath_nodes)-a] != dhn:
			gg.remove_node(gg_dipath_nodes[len(gg_dipath_nodes)-a])
		#cutoff_null_leafs0(gg)



#finds dhn
def find_dhn(G,g):
	#comP = centerofmass_graph(gg)
	comPP = centerofmass0(G,g.nodes())
	dhn = 0
	for n in g.neighbors(comPP):
		if g.node[n]['population'] == -1:
			dhn = n
	return dhn


#return the list with percentages of invs
def cluster_invs(G,g,percent):
	ggs_list = []
	#given dhn
	#finds dhn of cluster
	dhn = find_dhn(G,g)
	#gives the % of the cluster to invent
	#percent = 75 #%
	per = float(percent)/100
	errorr = 0.01
	#computes the init mass of cluster
	cluster_mass = 0
	for n in g.nodes():
		if g.node[n]['population'] != -1:
			cluster_mass = cluster_mass + g.node[n]['population']
	#initial effs
	l, gg, leafs, null_l = a_graph_efficiency_inv(g, dhn,1)
	ggs_list.append(gg)
	l_list = leafs_f(gg)[:]
	leaf_node = l_list[len(l_list)-1][0] #leaf_node with biggest f
	leaf_node_plith = G.node[leaf_node]['population'] #population of worst_leaf_node
	#define the var
	end_mass = float(cluster_mass - leaf_node_plith)
	frac_mass = end_mass/cluster_mass
	k=1
	#print k, ": ", frac_mass
	#for steps
	#step = 25
	#steps_list = []
	#for i in range(100/step):
	#	steps_list.append(tot-i*step)
	#steps_list.remove(steps_list[0])
	###
	while frac_mass - errorr > per:
		if leaf_node in gg.nodes():
			new_cluster_efs(gg,dhn,leaf_node,leaf_node_plith)
		l_list = leafs_f(gg)[:]
		leaf_node = l_list[len(l_list)-1][0] #leaf_node with biggest f
		leaf_node_plith = G.node[leaf_node]['population'] #population of worst_leaf_node
		#define the var
		end_mass = float(end_mass - leaf_node_plith)
		frac_mass = end_mass/cluster_mass
	ggs_list.append(gg)
		#for st in steps_list:
		#	if st/100 - 0.05  <= frac_mass <= st/100 + 0.05:
		#		ggs_list.append(gg)
		#k = k +1
		#print k, ": ", leaf_node, ": ", leaf_node_plith, " | ", end_mass, "::: ", frac_mass
	return ggs_list




#sortarei All edges of a graph 
def sort_fs(gg):
	list_fs_gg = []
	for e in gg.edges():
		list_fs_gg.append([e,gg[e[0]][e[1]]["efficiency"]])
	from operator import itemgetter, attrgetter
	sorted_list_fs_gg = sorted(list_fs_gg, key=itemgetter(1))
	return sorted_list_fs_gg


#given a directed graph and an edge of it, returns the edges of the subtree of the starting node of that edge
def fedge_sub(D,worst_fedge):
	#initial step
	a = worst_fedge
	D_edges = D.edges(a)[:]
	D_edges.remove(a)
	for e in D_edges:
		if e[0] == a[0]:
			D_edges.remove(e)
	l_a = D_edges[:] #very first edges of the subtree without root edge
	#recursive step
	for a in l_a:
		for edd in D.edges(a):
			if edd not in l_a:
				l_a.append(edd)
	#add the root edge
	l_a.append(worst_fedge)
	return l_a


#finds the nodes of a list of edges
def edges_nodes(fedge_subedges):
	l_n = []
	for e in fedge_subedges:
		n0 = e[0]
		n1 = e[1]
		if n0 not in l_n:
			l_n.append(n0)
		if n1 not in l_n:
			l_n.append(n1)
	return l_n


#g = cluster_to_subready(G,beta)

#return the list with percentages of invs
#using sub_trees
def cluster_invs22(G,g,percent):
	import copy
	ggs_list = []
	#given dhn
	#finds dhn of cluster
	dhn = find_dhn(G,g)
	#gives the % of the cluster to invent
	#percent = 75 #%
	per = float(percent)/100
	errorr = 0.01
	#computes the init mass of cluster
	cluster_mass = 0
	for n in g.nodes():
		if g.node[n]['population'] != -1:
			cluster_mass = cluster_mass + g.node[n]['population']
	#initial effs
	l, gg, leafs, null_l = a_graph_efficiency_inv(g, dhn,1)
	#for the sub_trees ;)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	#ggs_list.append(copy.deepcopy(gg)) 
	l_list = sort_fs(gg)[:] #sorting of edges according to fs
	worst_fedge, worst_fedge_f = l_list[len(l_list)-1] #worst f edge
	print worst_fedge
	#find to which sub_list's digraphs the worst_fedge belongs
	for Di in sub_list:
		e = worst_fedge
		if e in Di.edges():
			D = Di
			break
		if (e[1],e[0]) in Di.edges():
			D = Di
			worst_fedge = (e[1],e[0])
			break
	#finds the edges of the subtree!!! the last one is the fedge
	fedge_subedges = fedge_sub(D,worst_fedge)[:]
	#nodes of fedge_subedges, to know the sum of their population
	fedge_nodes = edges_nodes(fedge_subedges)[:]
	#finds the population of the nodes of the subedges
	s = 0
	for n in fedge_nodes:
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	fedge_nodes_plith = s
	#finds the total weight of the subtree
	w = 0
	for se in fedge_subedges:
		if se in G.edges():
			w = w + G[se[0]][se[1]]['weight']
		if (se[1],se[0]) in G.edges():
			w = w + G[se[1]][se[0]]['weight']
	fedge_subedges_weight = w
	#define the var
	end_mass = float(cluster_mass - fedge_nodes_plith)
	frac_mass = end_mass/cluster_mass
	k=1
	print k
	print "---"
	while frac_mass - errorr > per: #put a checker ;)
		ggs_list.append(copy.deepcopy(gg)) 
		if worst_fedge[1] in gg.nodes():
			worst_fedge1 = worst_fedge[1]
		print "........"
		print len(gg.nodes())
		print "+++"
		#new_cluster_efs22(gg,dhn,leaf_node,leaf_node_plith) #sub_tress ???
		new_cluster_efs22(gg,dhn,worst_fedge1,fedge_nodes_plith,fedge_subedges_weight,fedge_subedges)
		print len(gg.nodes())
		print "+-+-+"
		l_list = sort_fs(gg)[:] #sorting of edges according to fs
		worst_fedge, worst_fedge_f = l_list[len(l_list)-1] #worst f edge
		#find to which sub_list's digraphs the worst_fedge belongs
		for Di in sub_list:
			e = worst_fedge
			if e in Di.edges():
				D = Di
				break
			if (e[1],e[0]) in Di.edges():
				D = Di
				worst_fedge = (e[1],e[0])
				break
		#finds the edges of the subtree!!! the last one is the fedge
		fedge_subedges = fedge_sub(D,worst_fedge)[:]
		#nodes of fedge_subedges, to know the sum of their population
		fedge_nodes = edges_nodes(fedge_subedges)[:]
		#finds the population of the nodes of the subedges
		s = 0
		for n in fedge_nodes:
			if G.node[n]['population'] != -1:
				s = s + G.node[n]['population']
		fedge_nodes_plith = s
		#finds the total weight of the subtree
		w = 0
		for se in fedge_subedges:
			if se in G.edges():
				w = w + G[se[0]][se[1]]['weight']
			if (se[1],se[0]) in G.edges():
				w = w + G[se[1]][se[0]]['weight']
		fedge_subedges_weight = w
		#define the var
		end_mass = float(end_mass - fedge_nodes_plith)
		frac_mass = end_mass/cluster_mass
		k = k + 1
		print worst_fedge
		print k
		print end_mass, ", ", frac_mass
		print "---"
		#ggs_list.append(copy.deepcopy(gg))
	return ggs_list





def cluster_invs_dummy(G,g,dhn,percentt):
	#########75%
	cls1 = cluster_invs(G,g,percentt)
	cls75 = cls1[1]
	gg0 = cls1[2] #o  arithmos ton nodes einai sostos
	n_gg0 = []
	for n in gg0.nodes():
		n_gg0.append([n[0],n[1]])
	g75 = cluster_to_subready(G,n_gg0) #allazei ton arithmo ton nodes!!!
	#correction of number of nodes
	g75_0 = g75
	for n in g75_0.nodes():
		if n not in gg0.nodes() and n in g75.nodes():
			g75.remove_node(n)
	return netwrk_cost_dummy2(G,g75,dhn) #also works!!!


#sub_trees
def cluster_invs_dummy22(G,g,dhn,percentt):
	#########75%
	cls1 = cluster_invs22(G,g,percentt)
	cls75 = cls1[len(cls1)-1]
	#gg0 = cls1[2] #o  arithmos ton nodes einai sostos? den yparxei!!!
	gg0 = cls75
	n_gg0 = []
	for n in gg0.nodes():
		n_gg0.append([n[0],n[1]])
	g75 = cluster_to_subready(G,n_gg0) #allazei ton arithmo ton nodes!!!
	#correction of number of nodes
	g75_0 = g75
	for n in g75_0.nodes():
		if n not in gg0.nodes() and n in g75.nodes():
			g75.remove_node(n)
	return netwrk_cost_dummy2(G,g75,dhn) #also works!!!



def all_invs(p):
	larissa =  nx.DiGraph.to_undirected(nx.read_shp('/home/bluesman/Dropbox/NGNMarcostuff/LarissasPython/aa_scratch/networkcreationclean.py/revision10/forNetX/axons_larissa_with_buildings6_sub0.shp'))#forNetX
	set_new_attribute_to_nodes(larissa,'population',-1.0)
	set_new_attribute_to_nodes(larissa,'building_i',-1)
	set_new_attribute_to_nodes(larissa,'block_id',-1)
	change_length_attr(larissa)
	num = find_building_edges_and_update_nodes(larissa)
	restore_attributes(larissa)
	check = [nod for nod in larissa.degree() if larissa.degree(nod) > 1 and larissa.node[nod]['population'] != -1]
	G = larissa
	set_new_attribute_to_nodes(G,'sucgload',[0,0])
	set_new_attribute_to_nodes(G,'suc2gload',[0,0])
	set_new_attribute_to_nodes(G,'sucggload',[0,0])
	set_new_attribute_to_nodes(G,'root_node', 0)
	for e in G.edges():
		G_e = G[e[0]][e[1]]
		G_e['grans'] = {}
		G_e['ALPHA'] = {}
		G_e['grans_f'] = {}
		G_e['grans_c'] = {}
		G_e['grans_s'] = {}
		G_e['grans_d'] = {}
		G_e['dum_cost'] = 0
		G_e['gr_cost'] = 0
		G_e['tr_cost'] = 0
		G_e['dum_cost'] = 0
		G_e['efficiency'] = 0
	g = cluster_to_subready(G,beta)
	dhn = find_dhn(G,g)
	if p == 100:
		ggg, node100, cost100 = netwrk_cost_dummy2(G,g,dhn)
		graph_list = [ggg,cost100]
	if p == 75:
		ggg75, node75, cost75 = cluster_invs_dummy(G,g,dhn,75)
		graph_list = [ggg75,cost75]
	if p == 50:
		ggg50, node50, cost50 = cluster_invs_dummy(G,g,dhn,50)
		graph_list = [ggg50,cost50]
	if p == 25:
		ggg25, node25, cost25 = cluster_invs_dummy(G,g,dhn,25)
		graph_list = [ggg25,cost25]
	return graph_list


#paizei me ta sub_graphs & xrisimopoiei ta netwrk_cost_dummy22 !!!
#ston ypologismo tou 100% den allazei kati.
#gia ton ypologismo ton invs percentages xreiazomaste to sub_list apo to 100%
def all_invs22(p):
	larissa =  nx.DiGraph.to_undirected(nx.read_shp('/home/bluesman/Dropbox/NGNMarcostuff/LarissasPython/aa_scratch/networkcreationclean.py/revision10/forNetX/axons_larissa_with_buildings6_sub0.shp'))#forNetX
	set_new_attribute_to_nodes(larissa,'population',-1.0)
	set_new_attribute_to_nodes(larissa,'building_i',-1)
	set_new_attribute_to_nodes(larissa,'block_id',-1)
	change_length_attr(larissa)
	num = find_building_edges_and_update_nodes(larissa)
	restore_attributes(larissa)
	check = [nod for nod in larissa.degree() if larissa.degree(nod) > 1 and larissa.node[nod]['population'] != -1]
	G = larissa
	set_new_attribute_to_nodes(G,'sucgload',[0,0])
	set_new_attribute_to_nodes(G,'suc2gload',[0,0])
	set_new_attribute_to_nodes(G,'sucggload',[0,0])
	set_new_attribute_to_nodes(G,'root_node', 0)
	for e in G.edges():
		G_e = G[e[0]][e[1]]
		G_e['grans'] = {}
		G_e['ALPHA'] = {}
		G_e['grans_f'] = {}
		G_e['grans_c'] = {}
		G_e['grans_s'] = {}
		G_e['grans_d'] = {}
		G_e['dum_cost'] = 0
		G_e['gr_cost'] = 0
		G_e['tr_cost'] = 0
		G_e['dum_cost'] = 0
		G_e['efficiency'] = 0
	g = cluster_to_subready(G,beta)
	dhn = find_dhn(G,g)
	if p == 100:
		ggg, node100, cost100 = netwrk_cost_dummy2(G,g,dhn)
		graph_list = [ggg,cost100]
	if p == 75:
		ggg75, node75, cost75 = cluster_invs_dummy22(G,g,dhn,75)
		graph_list = [ggg75,cost75]
	if p == 50:
		ggg50, node50, cost50 = cluster_invs_dummy22(G,g,dhn,50)
		graph_list = [ggg50,cost50]
	if p == 25:
		ggg25, node25, cost25 = cluster_invs_dummy22(G,g,dhn,25)
		graph_list = [ggg25,cost25]
	return graph_list




#maybe add the vars that have to do with the way the clusters are filled in 
def a_emsp_b000(G,k):
	#computes the G_mass
	s = 0
	for n in G.nodes():
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	#computes the init_cluster_mass
	cl_mass_init = s/k
	plith_cl = cl_mass_init*1.02 #error correction cluster mass
	Clusters = []
	g0 = G
	while k != 1:
		print k
		#aman0 = a_emCOa_2nd_G(g0, k , 0, 1, 500)
		aman0 = a_emsp02a(g0,k,0)[:] #this to work needs centerofmass diff!!!
		cluster = aman0[0][0][:]
		#lmnts of all clusters
		P_all = []
		for c in aman0[0]:
			for i in c:
				P_all.append([i[0],i[1]])
		#plith_cl = aman0[2] #xreiazomaste ton plithismo tou cluster
		l_nodes = []
		for i in aman0[0][0]:
			l_nodes.append((i[0],i[1]))
		gg = G.subgraph(l_nodes)
		comP = centerofmass_graph0(gg)
		#anti gia to comP os dhn, tha pairnei to node pou einai pio makria em apo to comP
		l_nodes_dis = []
		for ii in l_nodes:
			l_nodes_dis.append([ii,adistance(ii,comP)])
		from operator import itemgetter, attrgetter
		sorted_l_nodes_dis = sorted(l_nodes_dis, key=itemgetter(1))
		dhn0 = sorted_l_nodes_dis[len(sorted_l_nodes_dis)-1][0]
		if G.node[dhn0]['population'] == -1:
			dhn = dhn0
		else:
			dhn = G.neighbors(dhn0)[0]
		#dhn = comP
		l_paths = nx.single_source_dijkstra_path(G,comP)
		all_nodes = []
		for n in gg.nodes():
			all_nodes.append(l_paths[n])
		end_list = []
		for i in all_nodes:
			for j in i:
				if j not in end_list:
					end_list.append(j)
		ll0 = end_list[:]
		population_to_int(G)
		set_new_attribute_to_nodes(G,'sucgload',[0,0])
		set_new_attribute_to_nodes(G,'suc2gload',[0,0])
		set_new_attribute_to_nodes(G,'sucggload',[0,0])
		set_new_attribute_to_nodes(G,'root_node', 0)
		g = G.subgraph(ll0)
		cutoff_null_leafs0(g)
		for e in g.edges():
			g_e = g[e[0]][e[1]]
			g_e['grans'] = {}
			g_e['ALPHA'] = {}
			g_e['grans_f'] = {}
			g_e['grans_c'] = {}
			g_e['grans_s'] = {}
			g_e['grans_d'] = {}
			g_e['dum_cost'] = 0
			g_e['gr_cost'] = 0
			g_e['tr_cost'] = 0
			g_e['dum_cost'] = 0
			g_e['efficiency'] = 0
		#finds dhn of cluster
		#comPP = centerofmass_graph(g) #choose either this or aman0[0][1]
		#for n in g.neighbors(comPP):
		#	if g.node[n]['population'] == -1:
		#		dhn = n
		big70 = graph_blocks700(G,dhn,plith_cl)[:]
		#big70 = graph_blocks70(G,G,dhn,plith_cl)[:]
		lmnts_list = []
		for b in big70:
			for lmn in b[1]:
				n = [lmn[0],lmn[1]]
				lmnts_list.append(n)
		lmnts70 = lmnts_list[:]
		#lmnts70 = cluster_blocks(G,big70)[:]
		#lmnts of the cluster after big70
		#lmnts70 = cluster_blocks(G,cluster)[:]
		Clusters.append(lmnts70)
		#update P_all
		for i in lmnts70:
			if i in P_all:
				P_all.remove(i)
		#gives the lmnts the form of 3ada
		P_a = []
		for p in P_all:
			pp = (p[0],p[1])
			P_a.append((pp[0],pp[1],G.node[pp]['population']))
		g0 = cluster_to_subgraph(G,P_a)[0]  #
		k = k -1
		print "end of: ", k + 1
	Clusters.append(P_all)
	return Clusters



###################################################################
###################    if we want clustering    ###################
###################################################################

##clustering
#g = cluster_to_subready(G,beta)
#alphag = a_emsp_b0(Gb,3)[:] #poly kalo gia clustering se CO-areas,xreiazetai mass_error correction
#alphag = a_COa_2ndV2_Gex1(g, 3, 4, 1, 500) #go to COa_2ndV2_Gex1.py

#C_w = alphag[:]
#print "idd,X,Y,cluster"
#for l in range(len(C_w)):
#	for j in range(0,len(C_w[l])):
#		print "idd"+str(l)+str(j+1)+","+str(C_w[l][j][0])+","+str(C_w[l][j][1])+",cluster"+str(l)

#finds the mass of a cluster
def cluster_m(G,cluster):
	s = 0
	for i in cluster:
		n = (i[0],i[1])
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	return s


##alpha is the initial cluster
#beta = alpha[0][:]

###################################################################
###################################################################

###################################################################
###################    play with blocks init    ###################
###################################################################

def print_mass(G,alphag):
	l = []
	for a in alphag:
		l.append(cluster_m(G,a))
	return l


#normalize
def norm_end(alphag,cs):
	Call = alphag[:]
	m = 1
	while len(Call)-m != 0:
		for i in range(len(Call)-m):
			norm_cl(Call[len(Call)-m],Call[i],cs)
		m = m + 1


#Gb = G

##gb = cluster_to_subready(G,beta)
##Gb_blocks = graph_blocks_all(gb)[:]

#Gb_blocks = graph_blocks_all(Gb)[:] #if we want all

#instead of all the nodes we play with only one node of each block
def gblock_graph(G):
	Gb = G.copy()
	Gb_blocks = graph_blocks_all(Gb)[:]
	gamma = []
	for i in range(len(Gb_blocks)):
		n = Gb_blocks[i][2]
		gamma.append(n) #the set of Nodes of blocks; the init set
		Gb.node[n]['population'] = Gb_blocks[i][1] #changing the population of these nodes
	g = cluster_to_subready(Gb,gamma)
	return g

#
###################################################################
###################################################################

#since it's very fast we will use it ;)
#pairnei olo to G
def a_emsp_b_inb(G,k):
	###initial step
	Gb = G
	#gb = cluster_to_subready(G,beta)
	#Gb_blocks = graph_blocks_all(gb)[:]
	Gb_blocks = graph_blocks_all(Gb)[:] #if we want all
	gamma = []
	for i in range(len(Gb_blocks)):
		n = Gb_blocks[i][2]
		gamma.append(n) #the set of Nodes of blocks; the init set
		Gb.node[n]['population'] = Gb_blocks[i][1] #changing the population of these nodes
	g = cluster_to_subready(Gb,gamma)
	###########
	#initialize all nodes list
	#P_all = []
	#for n in g.nodes():
	#	P_all.append([n[0],n[1]])
	C_list = []
	while k != 1:
		cl_remove = a_emsp_b(g,k,0)[0][:]
		C_list.append(cl_remove)
		#update gamma
		for i in cl_remove:
			inode = (i[0],i[1])
			if inode in gamma:
				gamma.remove(inode)
		#define new g
		g = cluster_to_subready(Gb,gamma)
		k = k -1
	C_list.append(gamma)
	return C_list


#since it's very fast we will use it ;)
#pairnei olo to G
def a_emsp_b0_inb(G,k):
	###initial step
	Gb = G
	#gb = cluster_to_subready(G,beta)
	#Gb_blocks = graph_blocks_all(gb)[:]
	Gb_blocks = graph_blocks_all(Gb)[:] #if we want all
	gamma = []
	for i in range(len(Gb_blocks)):
		n = Gb_blocks[i][2]
		gamma.append(n) #the set of Nodes of blocks; the init set
		Gb.node[n]['population'] = Gb_blocks[i][1] #changing the population of these nodes
	g = cluster_to_subready(Gb,gamma)
	###########
	#initialize all nodes list
	#P_all = []
	#for n in g.nodes():
	#	P_all.append([n[0],n[1]])
	C_list = []
	while k != 1:
		cl_remove = a_emsp_b0(g,k)[0][:]
		C_list.append(cl_remove)
		#update gamma
		for i in cl_remove:
			inode = (i[0],i[1])
			if inode in gamma:
				gamma.remove(inode)
		#define new g
		g = cluster_to_subready(Gb,gamma)
		k = k -1
	C_list.append(gamma)
	return C_list


#since it's very fast we will use it ;)
#pairnei olo to G
def a_emsp_b00_inb(G,k):
	###initial step
	Gb = G
	#gb = cluster_to_subready(G,beta)
	#Gb_blocks = graph_blocks_all(gb)[:]
	Gb_blocks = graph_blocks_all(Gb)[:] #if we want all
	gamma = []
	for i in range(len(Gb_blocks)):
		n = Gb_blocks[i][2]
		gamma.append(n) #the set of Nodes of blocks; the init set
		Gb.node[n]['population'] = Gb_blocks[i][1] #changing the population of these nodes
	g = cluster_to_subready(Gb,gamma)
	###########
	#initialize all nodes list
	#P_all = []
	#for n in g.nodes():
	#	P_all.append([n[0],n[1]])
	C_list = []
	while k != 1:
		cl_remove = a_emsp_b00(g,k)[0][:]
		C_list.append(cl_remove)
		#update gamma
		for i in cl_remove:
			inode = (i[0],i[1])
			if inode in gamma:
				gamma.remove(inode)
		#define new g
		g = cluster_to_subready(Gb,gamma)
		k = k -1
	C_list.append(gamma)
	return C_list



#alphag = a_emsp_b_inb(G,3)[:] 
#alphag = a_emsp_b0_inb(G,6)[:]
#alphag = a_emsp_b00_inb(G,6)[:]

#print "---"
#print_mass(alphag)
#print "---"


#C_w = alphag[0][:]
#print "idd,X,Y,cluster"
#for l in range(len(C_w)):
#	for j in range(0,len(C_w[l])):
#		print "idd"+str(l)+str(j+1)+","+str(C_w[l][j][0])+","+str(C_w[l][j][1])+",cluster"+str(l)



######################################
#####################################################
#######################################################################
# sp clustering ...
#V_one_min
#after clustering it starts to fill in clusters 1 by 1 not closer to max (min->full)
def a_COa_2nd_G_new(GG,k_init,about_coms,about_minmax,num_it):
	"""
	1st var: Set of Points to be Clustered
				1 := All Mean Points of Larissa
				0 := cluster0 points
	2nd var: #Clusters
	3rd var: n \in {1,2,3,4}. corresponds to which function we will use to 
				initialize tha coms for the em-clustering
				1 := rancom_points
				2 := rancom_points_half
				3 := rancom_points_tenth
				4 := rancom_points_20th
	4th var: 1 := fill in em_clustering from minimum som
				2 := fill in em_clustering from maximum som
	5th var: # iterations of clustering to stabilize the coms 
	"""
	G = GG
	#create the two initial sets of Points. The one has Points with 0 mass
	X_minus = []
	X_plus = []
	i = 0 #seperates the input Points to 2 sets.
	P_init0 = graph_c_vec(G)[:]
	while i < len(P_init0):
		if P_init0[i][2] == 0:
			X_minus.append(P_init0[i])
			i = i + 1
		else:
			X_plus.append(P_init0[i])
			i = i +1
	P_init = X_plus[:]
	P0 = P_init[:]
	k0 = k_init
	NumClusters = 0
	#finds the max_plith per cluster
	P_plith = sumofmass(P_init) #global
	import math
	max_frac = float(P_plith)/float(k_init)
	cluster_plith_max = math.ceil(max_frac) #max som. per cluster
	med_plith = math.ceil(P_plith/len(P_init)) #median of the plithismos/node
	max_plith = cluster_plith_max - med_plith #synthiki gia to som ton clusters
	Call = [] #store the clusters we find
	P00 = P_init[:] #Points, input for clustering
	kk = k_init  # #Clusters, input for clustering
	Cmin = [0]
	comP = centerofmass0(G,P_init)
	while len(Call) != k0:
		#clustering
		if about_coms == 0:
			C = akcom00(P00,ran_points(P00,kk),kk,num_it)
		if about_coms == 1:
			C = akcom00(P00,rancom_points(P00,kk),kk,num_it)
		if about_coms == 2:
			C = akcom00(P00,rancom_points_half(P00,kk),kk,num_it)
		if about_coms == 3:
			C = akcom00(P00,rancom_points_tenth(P00,kk),kk,num_it)
		if about_coms == 4:
			C = akcom00(P00,rancom_points_20th(P00,kk),kk,num_it)
		k = kk
		cl_sorted = [] #creates empty sorted clusters
		for i in range(k): #creates k-clusters
			cl_sorted.insert(0,[])
		for i in range(k): #initializing cl_sorted
			cl_sorted[i] = C[0][1][i]
		CS = cl_sorted
		CS_sorted = []
		for i in range(k):
			dis_l = []
			for j in range(len(CS[i])):
				x = CS[i][j] #choose a point from S
				dis_l.append([x, nx.dijkstra_path_length(G, centerofmass0(G,CS[i]), (x[0],x[1]))])
				from operator import itemgetter, attrgetter
				sorted_dis_l = sorted(dis_l, key=itemgetter(1))
			CS_sorted.append(sorted_dis_l)
		#creates a list with the lmnts according to the load of coms
		C_w = []
		for i in range(k):
			x_out = []
			C_weighted = []
			for j in range(len(CS_sorted[i])):
				x = CS_sorted[i][j]
				if sumofmass(C_weighted) + x[0][2] <= cluster_plith_max:
					C_weighted.append(x[0])
			C_w.append(C_weighted)
		#checks if there are clusters with som < max_plith
		Cmin = []
		for i in range(k):
			if sumofmass(C_w[i]) < max_plith:
				Cmin.append(C_w[i])
		if len(Cmin) == 0:
			for i in range(len(C_w)):
				Call.append(C_w[i])
			break
		else:
			#the set of lmnts of clusters with som < max_plith
			#put Cmins in a row ... depending on their som
			dis_Cmin = []
			for i in range(len(Cmin)):
				dis_Cmin.append([sumofmass(Cmin[i]),Cmin[i]])
			from operator import itemgetter, attrgetter
			sorted_Cmin = sorted(dis_Cmin, key=itemgetter(0))
			#create the list with the clusters from minimum som to maximum
			#so the filling up will start from clusters with minimum som
			if about_minmax == 1:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
			##the previous list but from maximum som to minimum
			if about_minmax == 2:
				Cminn = []
				for i in range(len(sorted_Cmin)):
					Cminn.append(sorted_Cmin[i][1]) 
				Llist = []
				for i in range(len(Cminn)):
					Llist.append(Cminn[len(Cminn)-i-1])
				Cminn = Llist[:]
			Cminset = Cminn[0]
			#update P0 according to new Cminset
			for i in range(len(Cminset)):
				if Cminset[i] in P0: 
					P0.remove(Cminset[i])
			##fill in the clusters with som < cluster_plith_max
			Cmin00 = Cminn[0]
			coms_l_C_w  = centerofmass0(G,Cmin00)
			dis_l_xw = []
			i = 0
			listt = []
			while i < len(P0):
				xw = P0[i] #choose a point from P0[i]
				dis_l_xw.append([adistance(xw,coms_l_C_w), xw])
				i = i+1
			from operator import itemgetter, attrgetter
			dis_l_xw_sorted = sorted(dis_l_xw, key=itemgetter(0))
			for i in range(len(dis_l_xw_sorted)):
				xw = dis_l_xw_sorted[i][1]
				if sumofmass(Cmin00) + xw[2] <= cluster_plith_max:
					Cmin00.append(xw) #upgrade Cmin00
					P0.remove(xw) #upgrade P0 
					coms_l_C_w = centerofmass0(G,Cmin00)
				else:
					break
			Call.append(Cmin00)
			NumClusters = NumClusters + 1
			if NumClusters == k0-1:
				Call.append(P0)
				break
			P00 = P0[:] #update P00 for the next clustering
			kk = k - 1
	coms_l_Call = [] #update the coms
	for i in range(len(Call)): 
		coms_l_Call.append(centerofmass0(G,Call[i]))
	i = 0
	dis_l_X_minus = []
	dis_l_X_minus_sorted = []
	while i < len(X_minus):
		xw = X_minus[i] #choose a point from X_minus[i]
		for j in range(len(coms_l_Call)):
			dis_l_X_minus.append([adistance(xw,coms_l_Call[j]), j])
		from operator import itemgetter, attrgetter
		dis_l_X_minus_sorted = sorted(dis_l_X_minus, key=itemgetter(0))
		Call[dis_l_X_minus_sorted[0][1]].append(xw)
		dis_l_X_minus = []
		dis_l_X_minus_sorted = []
		i = i + 1
	coms_l_Call = [] 
	i = 0
	for i in range(len(Call)):
		coms_l_Call.append(centerofmass0(G,Call[i]))
	import os 
	os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 1, 391.995))
	return [Call,coms_l_Call,max_plith]



#maybe add the vars that have to do with the way the clusters are filled in 
#mass error correction. still has some problems :P
def a_emsp_b0000new(G,g,k):
	#computes the G_mass
	s = 0
	for n in G.nodes():
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	#computes the init_cluster_mass
	cl_mass_init = s/k
	plith_cl = cl_mass_init*1.02 #error correction cluster mass
	Clusters = []
	g0 = g
	while k != 1:
		print k
		#aman0 = a_emCOa_2nd_G(g0, k , 0, 1, 500)
		#aman0 = a_emsp02a(g0,k,0)[:] #this to work needs centerofmass diff!!!
		aman0 = a_COa_2nd_G_new(g0,k,0,2,50)[:]
		cluster = aman0[0][0][:]
		#lmnts of all clusters
		P_all = []
		for c in aman0[0]:
			for i in c:
				P_all.append([i[0],i[1]])
		#plith_cl = aman0[2] #xreiazomaste ton plithismo tou cluster
		l_nodes = []
		for i in aman0[0][0]:
			l_nodes.append((i[0],i[1]))
		gg = G.subgraph(l_nodes)
		#comP = centerofmass_graph(gg)
		comP = centerofmass0(G,l_nodes)
		dhn = comP
		l_paths = nx.single_source_dijkstra_path(G,comP)
		all_nodes = []
		for n in gg.nodes():
			all_nodes.append(l_paths[n])
		end_list = []
		for i in all_nodes:
			for j in i:
				if j not in end_list:
					end_list.append(j)
		ll0 = end_list[:]
		population_to_int(G)
		set_new_attribute_to_nodes(G,'sucgload',[0,0])
		set_new_attribute_to_nodes(G,'suc2gload',[0,0])
		set_new_attribute_to_nodes(G,'sucggload',[0,0])
		set_new_attribute_to_nodes(G,'root_node', 0)
		g = G.subgraph(ll0)
		cutoff_null_leafs0(g)
		for e in g.edges():
			g_e = g[e[0]][e[1]]
			g_e['grans'] = {}
			g_e['ALPHA'] = {}
			g_e['grans_f'] = {}
			g_e['grans_c'] = {}
			g_e['grans_s'] = {}
			g_e['grans_d'] = {}
			g_e['dum_cost'] = 0
			g_e['gr_cost'] = 0
			g_e['tr_cost'] = 0
			g_e['dum_cost'] = 0
			g_e['efficiency'] = 0
		#finds dhn of cluster
		#comPP = centerofmass_graph(g) #choose either this or aman0[0][1]
		#for n in g.neighbors(comPP):
		#	if g.node[n]['population'] == -1:
		#		dhn = n
		big70 = graph_blocks700(G,dhn,plith_cl)[:]
		#big70 = graph_blocks70(G,G,dhn,plith_cl)[:]
		lmnts_list = []
		for b in big70:
			for lmn in b[1]:
				n = [lmn[0],lmn[1]]
				lmnts_list.append(n)
		lmnts70 = lmnts_list[:]
		#lmnts70 = cluster_blocks(G,big70)[:]
		#lmnts of the cluster after big70
		#lmnts70 = cluster_blocks(G,cluster)[:]
		Clusters.append(lmnts70)
		#update P_all
		for i in lmnts70:
			if i in P_all:
				P_all.remove(i)
		#gives the lmnts the form of 3ada
		P_a = []
		for p in P_all:
			pp = (p[0],p[1])
			P_a.append((pp[0],pp[1],G.node[pp]['population']))
		g0 = cluster_to_subgraph(G,P_a)[0]  #
		k = k -1
		print "end of: ", k + 1
	Clusters.append(P_all)
	return Clusters






#for all
#create a list with all the nodes of the blocks to the corresponding alphags
def lalphags(G,alphag):
	Gb = G.copy()
	Gb_blocks = graph_blocks_all(Gb)[:]
	lalphag = []
	for a in alphag:
		ll = []
		k = 0
		s = 0
		for n in a:
			na = (n[0],n[1])
			for bl in Gb_blocks:
				if bl[2] == (n[0],n[1]):
					k = k + 1
					s = s + G.node[na]['population']
					for i in bl[0]:
						ll.append(i)
		lalphag.append(ll)
	return lalphag


#for all
#create a list with all the nodes of the blocks to the corresponding alphags
def lalphags0(G,alphag):
	Gb = G.copy()
	Gb_blocks = graph_blocks_all(Gb)[:]
	lalphag = []
	for a in alphag:
		ll = []
		k = 0
		s = 0
		for n in a:
			na = (n[0],n[1])
			for bl in Gb_blocks:
				if bl[2] == (n[0],n[1]):
					k = k + 1
					s = s + G.node[na]['population']
					for i in bl[0]:
						ll.append([i[0],i[1]])
		lalphag.append(ll)
	return lalphag


#clusters are in alphag list
#so we create a list with the corresponding graphs of them
def lalphags_graphs(G,alphag):
	lalphag = lalphags(G,alphag)[:]
	gs_list = []
	import copy
	for l in lalphag:
		gs = cluster_to_subready(G,l)
		gs_list.append(copy.deepcopy(gs))
	return gs_list

##################3 mexri edo einai same






#returns all we need for fedge stuff
def cluster_invs22_init(G,g):
	dhn = find_dhn(G,g)
	#computes the init mass of cluster
	cluster_mass = 0
	for n in g.nodes():
		if g.node[n]['population'] != -1:
			cluster_mass = cluster_mass + g.node[n]['population']
	#initial effs
	l, gg, leafs, null_l = a_graph_efficiency_inv(g, dhn,1)
	#for the sub_trees ;)
	q = a_di_main_paths(G,l)
	sub_list = att_to_subtrees(G,q)[:]
	cluster_mass_gg = 0
	for n in gg.nodes():
		if g.node[n]['population'] != -1:
			cluster_mass_gg = cluster_mass_gg + gg.node[n]['population']
	return [g,dhn,cluster_mass,sub_list,gg,cluster_mass_gg]



#return the list with percentages of invs
#using sub_trees
#initially gg = g
def cluster_invs22_fedge(G,g,gg,worst_fedge,dhn,sub_list):
	#g,dhn,cluster_mass,sub_list = cluster_invs22_init(G,g)[:]
	gg_mass = 0
	for n in gg.nodes():
		if gg.node[n]['population'] != -1:
			gg_mass = gg_mass + gg.node[n]['population']
	#synthiki gia to pote tha recompute all about cluster
	#if float(gg_mass)/float(cluster_mass) > 0.5:
	#worst_fedge, worst_fedge_f = #as input
	#find to which sub_list's digraphs the worst_fedge belongs
	for Di in sub_list:
		e = worst_fedge
		if e in Di.edges():
			D = Di
			break
		if (e[1],e[0]) in Di.edges():
			D = Di
			worst_fedge = (e[1],e[0])
			break
	#finds the edges of the subtree!!! the last one is the fedge
	fedge_subedges = fedge_sub(D,worst_fedge)[:]
	#nodes of fedge_subedges, to know the sum of their population
	fedge_nodes = edges_nodes(fedge_subedges)[:]
	#finds the population of the nodes of the subedges
	s = 0
	for n in fedge_nodes:
		if G.node[n]['population'] != -1:
			s = s + G.node[n]['population']
	fedge_nodes_plith = s
	#finds the total weight of the subtree
	w = 0
	for se in fedge_subedges:
		if se in G.edges():
			w = w + G[se[0]][se[1]]['weight']
		if (se[1],se[0]) in G.edges():
			w = w + G[se[1]][se[0]]['weight']
	fedge_subedges_weight = w
	#define the var
	#end_mass = float(cluster_mass - fedge_nodes_plith)
	#frac_mass = end_mass/cluster_mass
	if worst_fedge[1] in gg.nodes():
		worst_fedge1 = worst_fedge[1]
	#new_cluster_efs22(gg,dhn,leaf_node,leaf_node_plith) #sub_tress ???
	new_cluster_efs22(gg,dhn,worst_fedge1,fedge_nodes_plith,fedge_subedges_weight,fedge_subedges)
	#computing gg_mass
	gg_mass = 0
	for n in gg.nodes():
		if gg.node[n]['population'] != -1:
			gg_mass = gg_mass + gg.node[n]['population']
	return [gg,gg_mass]



#great!!! return a list with all the graphs according to cutoff subtrees.
#the percentage of the last one over the first one is the closest one to what we want
def cluster_invs22_all(G,g,p):
	import copy
	ggs_list = []
	g,dhn,cluster_mass,sub_list,gg,cluster_mass_gg = cluster_invs22_init(G,g)[:]
	l_list = sort_fs(gg)[:] #sorting of edges according to fs
	worst_fedge, worst_fedge_f = l_list[len(l_list)-1] #worst f edge
	gg, gg_mass = cluster_invs22_fedge(G,g,gg,worst_fedge,dhn,sub_list)[:]
	while float(gg_mass)/float(cluster_mass) > p:
		ggs_list.append(copy.deepcopy(gg))
		l_list = sort_fs(gg)[:] #sorting of edges according to fs
		worst_fedge, worst_fedge_f = l_list[len(l_list)-1] #worst f edge
		gg, gg_mass = cluster_invs22_fedge(G,g,gg,worst_fedge,dhn,sub_list)[:]
	return ggs_list


#given an edge, worst or not, cutoff the subtree of it,recomputes the fs and mpla mpla.
def cluster_inv_cutoff_edge(G,g0,worst_fedge):
	import copy
	ggs_list = []
	g,dhn,cluster_mass,sub_list,gg = cluster_invs22_init(G,g0) #at the new algo
	ggs_list.append(copy.deepcopy(gg))
	gg, gg_mass = cluster_invs22_fedge(G,g,gg,worst_fedge,sub_list)
	ggs_list.append(copy.deepcopy(gg))
	return ggs_list




#sub_trees
def cluster_invs_dummy22_all(G,g,dhn,percentt):
	#########75%
	cls1 = cluster_invs22_all(G,g,percentt)[:]
	cls75 = cls1[len(cls1)-1]
	#gg0 = cls1[2] #o  arithmos ton nodes einai sostos? den yparxei!!!
	gg0 = cls75
	n_gg0 = []
	for n in gg0.nodes():
		n_gg0.append([n[0],n[1]])
	g75 = cluster_to_subready(G,n_gg0) #allazei ton arithmo ton nodes!!!
	#correction of number of nodes
	g75_0 = g75
	for n in g75_0.nodes():
		if n not in gg0.nodes() and n in g75.nodes():
			g75.remove_node(n)
	return netwrk_cost_dummy2(G,g75,dhn) #also works!!!



#paizei me ta sub_graphs & xrisimopoiei ta netwrk_cost_dummy22 !!!
#ston ypologismo tou 100% den allazei kati.
#gia ton ypologismo ton invs percentages xreiazomaste to sub_list apo to 100%
def all_invs22_all(G,beta,p):
	larissa =  nx.DiGraph.to_undirected(nx.read_shp('/home/bluesman/Dropbox/NGNMarcostuff/LarissasPython/aa_scratch/networkcreationclean.py/revision10/forNetX/axons_larissa_with_buildings6_sub0.shp'))#forNetX
	set_new_attribute_to_nodes(larissa,'population',-1.0)
	set_new_attribute_to_nodes(larissa,'building_i',-1)
	set_new_attribute_to_nodes(larissa,'block_id',-1)
	change_length_attr(larissa)
	num = find_building_edges_and_update_nodes(larissa)
	restore_attributes(larissa)
	check = [nod for nod in larissa.degree() if larissa.degree(nod) > 1 and larissa.node[nod]['population'] != -1]
	G = larissa
	set_new_attribute_to_nodes(G,'sucgload',[0,0])
	set_new_attribute_to_nodes(G,'suc2gload',[0,0])
	set_new_attribute_to_nodes(G,'sucggload',[0,0])
	set_new_attribute_to_nodes(G,'root_node', 0)
	for e in G.edges():
		G_e = G[e[0]][e[1]]
		G_e['grans'] = {}
		G_e['ALPHA'] = {}
		G_e['grans_f'] = {}
		G_e['grans_c'] = {}
		G_e['grans_s'] = {}
		G_e['grans_d'] = {}
		G_e['dum_cost'] = 0
		G_e['gr_cost'] = 0
		G_e['tr_cost'] = 0
		G_e['dum_cost'] = 0
		G_e['efficiency'] = 0
	g = cluster_to_subready(G,beta)
	dhn = find_dhn(G,g)
	ggg, node, cost = cluster_invs_dummy22_all(G,g,dhn,p)
	graph_list = [ggg,cost]
	return graph_list




#def for cuttingoff the worst edge of all clusters
#alphag is the list of clusters.
def cutoffedges(G,alphag,p):
	import copy
	#creates the list of init_graphs of clusters
	g_all = []
	for a in alphag:
		import copy
		g = cluster_to_subready(G,a)
		g_all.append(copy.deepcopy(g))
	#g,dhn,cluster_mass,sub_list,gg,cluster_mass_gg = cluster_invs22_init(G,g)[:]
	#list of graphs with all the info we want!
	g_all_info = []
	for gke in g_all:
		g_all_info.append(cluster_invs22_init(G,gke))
	#all clusters mass_init = 0
	cluster_mass_all_init = 0
	for i in range(len(g_all_info)):
		cluster_mass_all_init = cluster_mass_all_init + g_all_info[i][2]
	#from here it will be used again ######################################
	#list of all edges with their fs and an id of which cluster they belong
	k = 0
	g_all_es = []
	for i in g_all_info:
		g = i[4]
		for e in g.edges():
			g_all_es.append([e,g[e[0]][e[1]]['efficiency'],k])
		k = k + 1
	#sorting of above list
	from operator import itemgetter, attrgetter
	sorted_g_all_es = sorted(g_all_es, key=itemgetter(1))
	worst_fedge, fedgee, fedge_cl = sorted_g_all_es[len(sorted_g_all_es)-1]
	#20:34/20.09.14
	#finds to which graph the worst edge belongs and defines the graph to play with
	for i in range(len(g_all_info)):
		if i == fedge_cl:
			g = g_all_info[i][0]
			gg = g_all_info[i][4]
			dhn = g_all_info[i][1]
			cluster_mass = g_all_info[i][2]
			sub_list = g_all_info[i][3]
			cluster_mass_gg = g_all_info[i][5]
			break
	gg, gg_mass = cluster_invs22_fedge(G,g,gg,worst_fedge,dhn,sub_list)
	#after the cutoff we give new values to some of the vars
	#maybe we will put constraint on the frac of masses > 50%
	for i in range(len(g_all_info)):
		if i == fedge_cl:
			g_all_info[i][4] = gg
			g_all_info[i][5] = gg_mass
			break
	#all clusters mass after
	cluster_mass_all_after = 0
	for i in range(len(g_all_info)):
		cluster_mass_all_after = cluster_mass_all_after + g_all_info[i][5]
	all_cluster_mass_frac = float(cluster_mass_all_after)/float(cluster_mass_all_init)
	info_list = [cluster_mass_all_init, cluster_mass_all_after, all_cluster_mass_frac, fedge_cl,g_all_info]
	liste = []
	liste.append(copy.deepcopy(info_list))
	while all_cluster_mass_frac > p:
		info_list = []
		k = 0
		g_all_es = []
		for i in g_all_info:
			g = i[4]
			for e in g.edges():
				g_all_es.append([e,g[e[0]][e[1]]['efficiency'],k])
			k = k + 1
		#sorting of above list
		from operator import itemgetter, attrgetter
		sorted_g_all_es = sorted(g_all_es, key=itemgetter(1))
		worst_fedge, fedgee, fedge_cl = sorted_g_all_es[len(sorted_g_all_es)-1]
		#finds to which graph the worst edge belongs and defines the graph to play with
		for i in range(len(g_all_info)):
			if i == fedge_cl:
				g = g_all_info[i][0]
				gg = g_all_info[i][4]
				dhn = g_all_info[i][1]
				cluster_mass = g_all_info[i][2]
				sub_list = g_all_info[i][3]
				cluster_mass_gg = g_all_info[i][5]
				break
		gg, gg_mass = cluster_invs22_fedge(G,g,gg,worst_fedge,dhn,sub_list)
		#after the cutoff we give new values to some of the vars
		#maybe we will put constraint on the frac of masses > 50%
		for i in range(len(g_all_info)):
			if i == fedge_cl:
				g_all_info[i][4] = gg
				g_all_info[i][5] = gg_mass
				break
		#all clusters mass after
		cluster_mass_all_after = 0
		for i in range(len(g_all_info)):
			cluster_mass_all_after = cluster_mass_all_after + g_all_info[i][5]
		all_cluster_mass_frac = float(cluster_mass_all_after)/float(cluster_mass_all_init)
		info_list = [cluster_mass_all_init, cluster_mass_all_after, all_cluster_mass_frac, fedge_cl,g_all_info]
		liste.append(copy.deepcopy(info_list))
	return liste




beta = [[364947.957563, 4385329.833609],
 [364949.75239499996, 4385316.276632],
 [364934.35569, 4385369.454937],
 [364938.97579999996, 4385355.422522999],
 [364958.222244, 4385284.672737],
 [364996.243641, 4385183.112593],
 [364940.383416, 4385248.729267],
 [364974.841203, 4385185.443642],
 [364967.911208, 4385288.275145],
 [364954.685077, 4385251.967801],
 [364979.460147, 4385233.7896529995],
 [364962.48299499997, 4385177.794569],
 [364964.188024, 4385278.32027],
 [364950.11498099996, 4385219.748679],
 [364999.142193, 4385172.840372],
 [364969.115657, 4385162.4931809995],
 [364977.78160499997, 4385167.176572],
 [364987.364037, 4385198.0922799995],
 [364966.523628, 4385247.430255],
 [364982.464474, 4385222.791019],
 [364958.41601, 4385298.854994],
 [364963.73433899996, 4385287.38698],
 [364976.948634, 4385243.785722],
 [364971.222367, 4385267.990918],
 [365011.707281, 4385234.104201],
 [365050.10769499996, 4385308.225229],
 [365050.547264, 4385290.944012],
 [365037.579301, 4385296.821049],
 [365069.07175899995, 4385305.163006],
 [365081.78129899997, 4385317.195346],
 [365062.16278799996, 4385291.643796],
 [365042.704941, 4385280.670243],
 [365084.45700299996, 4385291.659413],
 [365034.878675, 4385310.51935],
 [365064.803542, 4385317.289035],
 [365042.74666999996, 4385273.277172999],
 [365057.84518999996, 4385279.36709],
 [365048.50649199996, 4385278.218013],
 [365037.92758699995, 4385281.2751589995],
 [365054.39724099997, 4385301.771466],
 [365048.900072, 4385319.337301],
 [365005.20386899996, 4385338.580782],
 [364989.32246999996, 4385340.610952999],
 [364982.65783499996, 4385400.180306],
 [364997.012796, 4385337.365739999],
 [364982.259897, 4385346.976659],
 [364971.206206, 4385406.013657],
 [365024.95627699996, 4385451.729665],
 [365032.370181, 4385486.305651],
 [365008.92064599996, 4385448.650161],
 [365036.46397, 4385452.69346],
 [365007.91954699997, 4385487.540361],
 [365001.954491, 4385471.402061],
 [365050.81403, 4385479.530627],
 [365047.433052, 4385493.434487],
 [365034.27283699997, 4385461.830525],
 [365013.293623, 4385465.2325989995],
 [364999.36504999996, 4385485.068612],
 [365054.985538, 4385457.408212],
 [365026.28100799996, 4385469.375755],
 [365004.308395, 4385462.737248],
 [365018.80466699996, 4385486.430499],
 [364975.96113, 4385464.5610879995],
 [364950.491338, 4385466.950933],
 [364974.038196, 4385475.393595],
 [365059.547907, 4385246.0568389995],
 [365070.555353, 4385247.66165],
 [365048.194607, 4385239.753086],
 [365086.76182799996, 4385228.353407],
 [365016.35486699996, 4385414.166964999],
 [365062.51728599996, 4385398.419571999],
 [365056.06004799996, 4385397.798009],
 [365058.030846, 4385410.165411999],
 [365028.631816, 4385430.572023],
 [365012.200978, 4385420.642357999],
 [365092.84167, 4385209.593146],
 [365110.51578899997, 4385431.914865],
 [365091.056513, 4385408.174215],
 [365095.50578199996, 4385427.91667],
 [365103.82921, 4385421.710024],
 [365092.329843, 4385420.496987],
 [365116.041216, 4385410.966894],
 [365125.63250999997, 4385450.100075],
 [365097.78688699997, 4385442.88121],
 [365106.380956, 4385446.624301],
 [365103.23399, 4385428.825716],
 [365079.92914799997, 4385435.259629],
 [365125.03386799997, 4385435.894952999],
 [365131.00036299997, 4385411.865931],
 [365129.363257, 4385424.790031],
 [365104.757401, 4385409.028933],
 [365095.04146499996, 4385408.426508],
 [365116.941499, 4385451.148752],
 [365112.083592, 4385425.352562999],
 [365114.312898, 4385439.922122],
 [365084.914094, 4385407.785843],
 [365072.259369, 4385472.372517],
 [365117.815718, 4385493.595635],
 [365097.265443, 4385502.36819],
 [365071.663387, 4385485.263776],
 [365097.578123, 4385488.020711999],
 [365099.741868, 4385481.334815],
 [365094.446763, 4385474.736318],
 [365106.57091199997, 4385483.220970999],
 [365086.220933, 4385465.373567],
 [365120.649651, 4385473.2005509995],
 [365075.314205, 4385457.871915],
 [365060.04504399997, 4385537.731835],
 [365144.300482, 4385243.474083],
 [365125.894054, 4385238.939319],
 [365168.068867, 4385250.827258],
 [365142.55717499997, 4385205.341448],
 [365132.58793, 4385221.743852],
 [365162.404598, 4385228.525752],
 [365165.933476, 4385212.750557],
 [365176.749265, 4385216.58567],
 [365154.368667, 4385211.2338189995],
 [365151.015561, 4385223.823121999],
 [365174.162451, 4385232.2645809995],
 [365130.17524099996, 4385203.2130889995],
 [364850.176272, 4385330.1574949995],
 [364872.031373, 4385329.817474999],
 [364853.02242399997, 4385334.999856],
 [364870.23920099996, 4385342.805767],
 [364897.136074, 4385337.551662],
 [364885.374156, 4385333.647969],
 [364855.34022799996, 4385341.923901999],
 [364861.18193099997, 4385331.8220959995],
 [364865.690106, 4385348.858434],
 [364920.964628, 4385351.803009],
 [364904.164561, 4385359.394238],
 [364843.021647, 4385339.8823029995],
 [364916.25606499997, 4385362.779233],
 [364879.163516, 4385351.262704],
 [364909.82135, 4385341.666269],
 [364914.24707399996, 4385322.917905],
 [364871.651096, 4385293.316118999],
 [364920.952109, 4385325.251312],
 [364902.499163, 4385320.091852],
 [364910.870826, 4385303.157245],
 [364899.661026, 4385298.710562],
 [364889.61649, 4385296.7622569995],
 [364878.832299, 4385310.322339],
 [364934.2374, 4385311.320028],
 [364928.84614599997, 4385329.07446],
 [364940.42758699995, 4385268.025703],
 [364898.314042, 4385274.6542919995],
 [364881.707303, 4385251.577157],
 [364870.54273399996, 4385247.677604],
 [364947.422231, 4385271.896148],
 [364914.88975699997, 4385261.3727629995],
 [364919.44657, 4385284.758543],
 [364904.363525, 4385258.820017],
 [364930.434233, 4385287.110425999],
 [364875.615748, 4385270.0366549995],
 [364924.810887, 4385265.7277069995],
 [364892.423967, 4385254.574161],
 [364940.92601999996, 4385291.460682999],
 [364935.007721, 4385275.396477],
 [364908.143888, 4385280.719574],
 [364805.09854499996, 4385344.550729],
 [364931.84823199996, 4385387.553959],
 [364822.77074999997, 4385349.675953],
 [364866.823107, 4385376.9387179995],
 [364830.941667, 4385356.525995],
 [364809.70328099997, 4385351.046405],
 [364915.513627, 4385402.1840969995],
 [364916.32460399996, 4385382.108016],
 [364819.63777699997, 4385377.762434999],
 [364855.546054, 4385360.071436],
 [364927.219436, 4385405.268445999],
 [364832.925, 4385370.388499999],
 [364900.786659, 4385396.213735],
 [364873.161609, 4385368.685556999],
 [364844.896702, 4385360.517278],
 [364887.42773299996, 4385373.621683],
 [364873.709124, 4385388.252421999],
 [364828.670827, 4385369.122347],
 [364839.489322, 4385375.9749839995],
 [364864.20655199996, 4385386.841388],
 [364871.07958799996, 4385434.999443],
 [364838.966304, 4385403.134955],
 [364864.281419, 4385424.725386],
 [364891.84976199997, 4385438.816191],
 [364880.29480599996, 4385437.93274],
 [364884.184694, 4385417.490135999],
 [364854.820045, 4385421.584426],
 [364856.312186, 4385430.530208],
 [364828.608822, 4385421.290305],
 [364861.827895, 4385407.775292],
 [364915.105664, 4385210.61642],
 [364892.924986, 4385204.290973],
 [364902.661157, 4385185.130171],
 [364908.489627, 4385171.300554],
 [364896.829811, 4385235.634606],
 [364923.721601, 4385246.866393],
 [364934.849752, 4385152.161458],
 [364903.711072, 4385144.418242999],
 [364949.920299, 4385155.500584],
 [364915.131932, 4385158.137980999],
 [364945.29396, 4385167.975281999],
 [364897.017879, 4385163.486707],
 [364902.214439, 4385193.687639],
 [364882.10708399996, 4385211.005236],
 [364917.45076499996, 4385143.226404],
 [364918.064854, 4385198.900936999],
 [364927.39082599996, 4385177.224326],
 [364914.786178, 4385240.096419999],
 [364931.073454, 4385160.511516999]]


#Gb = G
#Gb = G.copy()

#Gb_blocks = graph_blocks_all(Gb)[:] #if we want all


#either we have fixed our cluster, as it is beta above, or we have it in a list 
#of clusters after the clustering. 
#REMARKS••••••••••••••••
#1. the form of beta MUST be the same as above and have ALL the building nodes
#   so after clustering we have to check or give to betas of the clusters the 
#   appropriate form!!!


############################## CLUSTERING ####################################
#alphag = 0
#alphag = a_COa_2nd_G_new(g,6,0,1,23)[:] #50 iters are the best! same as 10 iters
# print_mass(alphag)
#Out[5]: [3293, 3296, 3306, 3306, 3289, 3345]



#alphagco = a_COa_2nd_G_new(g,8,0,1,50)[:] #50 iters are the best!

g = gblock_graph(G)
alphagco = a_emsp02(g,3,0)[:] #secs!!!

lalphag = lalphags(G,alphagco)[:]

alphag = []
alphag = lalphag[:]

g_list = lalphags_graphs(G,alphag)[:]

g0 = g_list[0]
---

alphagco_g0 = a_emsp02(g0,3,0)[:] #clustering to the 1st cluster of the first clustering

C_w = alphagco[:]
print "idd,X,Y,cluster"
for l in range(len(C_w)):
	for j in range(0,len(C_w[l])):
		print "idd"+str(l)+str(j+1)+","+str(C_w[l][j][0])+","+str(C_w[l][j][1])+",cluster"+str(l)


C_w = alphagco_g0[:]
print "idd,X,Y,cluster"
for l in range(len(C_w)):
	for j in range(0,len(C_w[l])):
		print "idd"+str(l)+str(j+1)+","+str(C_w[l][j][0])+","+str(C_w[l][j][1])+",cluster"+str(l)



---
#alphagco = a_COa_2nd_G_new(g,3,0,1,23)[:] #50 iters are the best!

#alphagco = a_emsp_b0(G,3)[:] [6712, 6741, 6659] same

#alphagco = a_emsp_b0000new(G,g,3)[:] [6706, 6719, 1046] problem

#aa = alphagco[0][:]
#alphagc = aa[:]

###########
#lalphag = lalphags(G,alphag)[:]

#alphag = []
#alphag = lalphag[:]

#cutoffedges(G,alphag0,0.60)[:] # check for 100% ;)

##if we want to cluster the CO areas #####################
#lalphag = lalphags(G,alphag)[:]

#alphag = []
#alphag = lalphag[:]

#g_list =  lalphags_graphs(G,alphag)[:]
#beta = lalphag[0] #choose a COa to cluster
#g = g_list[0]
###########

#C_w = alphagco_new[:]
#print "idd,X,Y,cluster"
#for l in range(len(C_w)):
#	for j in range(0,len(C_w[l])):
#		print "idd"+str(l)+str(j+1)+","+str(C_w[l][j][0])+","+str(C_w[l][j][1])+",cluster"+str(l)
###############################################################################

################################# FIXED CLUSTER ###############################

#alphag = [beta][:]

#cbeta = cutoffedges(G,alphag,0.70)[:]

###############################################################################

def feeder_graph(G,comP_dhns,dhns):
	return cluster_to_subgraph_f(G,dhns,comP_dhns)[0]

#g_feeder = feeder_graph(G,comP_dhns,dhns)

###############################################################################
##################### Testing the Clustering Algos ############################

#g = gblock_graph(G) #######

#alphagco = a_COa_2nd_G_new(g,6,0,1,23)[0][:] #2 hours
#alphagco = a_emsp02a(g,10,23)[0][:] #seconds!!! some problems with a few nodes!


#alphagco = a_emsp02a_norm(g,6,23)[0][:] #seconds!!! some problems with a few nodes!


#alphagco = a_emsp_b_inb(g,10)[:] #seconds!!! some problems with a few nodes!
#alphagco = a_emsp_b0000new(G,g,6)[:] ???
#alphagc0 = a_emsp_b0_inb(g,6) #mins!!! not nice
#alphagco = a_emsp_b00_inb(g,6)[:] #mins!!! not nice

#alphagco = a_emsp_b(g,8)[:] #secs!!! some problems with a few nodes #######

#alphagco = a_emsp_b0(g,6)[:] #mins!!! wrong!!!
#alphagco = a_emsp_b00a(g,6)[:] #mins!!! wrong
#alphagco = a_emsp_b00(g,6)[:] #mins!!! wrong

#alphagco = a_emsp_b000(g,6)[:] #mins!!! wrong
#alphagco = a_emsp02(g,3,0)[:] #secs!!! some problems with a few nodes! correction nodes done ;)
#alphagco = a_COa_2ndV2_Gex1(g,3,0,1,23)[:] 


