
import sys
import networkx as nx
import matplotlib.pyplot as plt
import math
import random
from heapq import heappop, heappush




G =  nx.DiGraph.to_undirected(nx.read_shp('./aa_scratch0/axons_larissa_with_buildings6_sub0.shp'))
for x in G:
    print (x)

print sys.argv[1] # first parameter




