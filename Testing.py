import numpy as np
import networkx as nx

def RiddlerBobvsSusan():

    nsims = 100000
    nflips = 100
    running_total = 0

    for i in range(nsims):

        flips = np.random.randint(0,2,size = nflips)
        first_diffs = flips[0:-1] - flips[1:]
        susan_score = (first_diffs == 1).sum()
        bob_score = (first_diffs + flips[0:-1] == 1).sum()

        running_total += (susan_score > bob_score)*1 + (susan_score == bob_score)*.5

    return running_total/nsims

def riddler_water(capA: int, capB: int, target: int):

    nodes =[(i,j) for i in range(capA+1) for j in range(capB+1)]
    edges = [(n,e) for n in nodes for e in add_edges(*n,capA,capB)]
    G = nx.Graph(edges)
    
    print(list(G.nodes))


def add_edges(Aamt: int,Bamt: int, capA: int, capB: int):

    edge_list = set((
                 (0,Bamt),(Aamt,0), 
                 (Aamt,capB), 
                 (max(0,Aamt - (capB - Bamt)),min(capB,Aamt + Bamt)),
                 (capA,Bamt), (min(capA, Aamt + Bamt), max(0,Bamt - (capA - Aamt)))))
    
    edge_list.discard((Aamt, Bamt))

    return edge_list

    
riddler_water(10,3,5)