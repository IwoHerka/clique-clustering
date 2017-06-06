from __future__ import print_function

import time

import networkx as nx

from clique_clustering import cluster
from helpers import draw


def test_graph(which=0):
    G = nx.Graph()

    if which == 0:
        # Handmade Square-Templar graph
        # for testing edge case.
        G.add_nodes_from([i + 1 for i in range(13)])
        G.add_edge(1, 2)
        G.add_edge(4, 3)
        G.add_edge(5, 6)
        G.add_edge(7, 8)
        G.add_edge(1, 9)
        G.add_edge(2, 9)
        G.add_edge(3, 9)
        G.add_edge(4, 9)
        G.add_edge(5, 9)
        G.add_edge(6, 9)
        G.add_edge(7, 9)
        G.add_edge(8, 9)
        G.add_edge(10, 11)
        G.add_edge(10, 12)
        G.add_edge(10, 13)
        G.add_edge(12, 11)
        G.add_edge(12, 13)
        G.add_edge(11, 13)
        G.add_edge(11, 8)
    elif which == 1:
        G = nx.karate_club_graph()

    return G


# Pre-calculated co-ords for
# karate club graph.
pos = {
   0: [0.24854411,  0.56789969],
   1: [0.3451995 ,  0.58944501],
   2: [0.51316793,  0.40191814],
   3: [0.33389867,  0.69504922],
   4: [0.00898965,  0.40152274],
   5: [0.06415735,  0.7237055 ],
   6: [0.0311286 ,  0.65284374],
   7: [0.26070767,  0.42654751],
   8: [0.60600687,  0.57338364],
   9: [0.78437374,  0.12241452],
   10: [0.00214003,  0.49118077],
   11: [0.        ,  0.56674156],
   12: [0.29413052,  0.93757276],
   13: [0.47448654,  0.5654252 ],
   14: [0.94668806,  0.70993262],
   15: [ 1.        ,  0.55315955],
   16: [0.17109661,  0.8727277 ],
   17: [0.10385152,  0.31154113],
   18: [0.9223013 ,  0.29868656],
   19: [0.51174613,  0.74706561],
   20: [0.98214366,  0.63597046],
   21: [0.11502686,  0.80959331],
   22: [0.98635785,  0.3679618 ],
   23: [0.84066805,  0.21902472],
   24: [0.45742417,  0.        ],
   25: [0.61200884,  0.00792277],
   26: [0.90736859,  0.77769893],
   27: [0.6399027 ,  0.12675693],
   28: [0.67613702,  0.22746644],
   29: [0.98578492,  0.47293429],
   30: [0.68777401,  0.70012877],
   31: [0.53544508,  0.25858682],
   32: [0.8284044 ,  0.47321508],
   33: [0.76616909,  0.46319817]
}


G = test_graph(1)

start = time.time()
res = cluster(G)
print(time.time() - start)

draw(G, res, pos)
