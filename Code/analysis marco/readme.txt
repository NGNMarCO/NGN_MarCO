
This is an analysis which was made in order to compare run time of execution of the algorithm.
The aim of the analysis was to find ways to reduce the total run time of the calculation 
of the distribution network.

One of the main steps of the calculation of the best point to place the KV is to make 
a network analysis (including costs etc.) in each 3way junction of a prespecified area.
Initially we take as input the centerOfmass of the cluster and based on this we calculate 
the best point for the KV. This is programmatically very expensive.

Theoretically the centerOfmass (based on population) of each cluster should be in close distance
to the ideal location of the KV. The folders 2clusters and 3clusters contain CSV files 
with coordinates of the 3way junctions, centerOfmass, and best calculated point for KV.
The corresponding qgis files illustrate the above.

In these maps it is visible that indeed the calculated "best KV spot" is very close to 
the centerOfMass.

Based on this I modified the initial function (made by Thanasis): "find_best_dhn()"
so instead of making a network analysis for each single 3-way point to assume that 
the best point to place the KV is the one closest (euclidean distance) to the centerOfMass.

I run the algorithm twice for 3 clusters (once with the old function and once with the new).
The excel file contains the results. 
The conclusion is that although in some cases the total cost differences are very small (2-3k)
in some other cases the difference reach up to 20%.
