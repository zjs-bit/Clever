import numpy as np
import networkx as nx
from typing import List

def best_pour_strategy(shortest_pours, target: int):
    
    min_pours: int = np.inf
    shortest_pour: List = []
    for p in shortest_pours:
        if target in p and len(shortest_pours[p]) < min_pours:
            shortest_pour = shortest_pours[p]
            min_pours = len(shortest_pour)

    return min_pours-1, shortest_pour[1:]

def shortest_pours(capA: int, capB: int):
    
    pitcherlevels =[(i,j) for i in range(capA+1) for j in range(capB+1)]
    edges = [(n,e) for n in pitcherlevels for e in add_edges(*n,capA,capB)]
    G = nx.DiGraph(edges)
    return nx.single_source_shortest_path(G,source=(0,0))

def add_edges(Aamt: int,Bamt: int, capA: int, capB: int):
    edge_list = set((
                 (0,Bamt),(Aamt,0), 
                 (Aamt,capB), 
                 (max(0,Aamt - (capB - Bamt)),min(capB,Aamt + Bamt)),
                 (capA,Bamt), (min(capA, Aamt + Bamt), max(0,Bamt - (capA - Aamt)))))
    
    edge_list.discard((Aamt, Bamt))
    return edge_list

def fiddler_pours_solve():

    #Solve the fiddler:
    best_pours = shortest_pours(capA=10,capB=3)
    pours, steps = best_pour_strategy(best_pours, target = 5)
    print(f"Target can be achieved in {pours} pours as follows: {steps}")

    #Solve the extra credit:
    best_pours_EC = shortest_pours(capA = 100, capB = 93)
    f_n = [best_pour_strategy(best_pours_EC, target = n)[0] for n in range(1,101)]
    max_fn = max(f_n)
    max_n = f_n.index(max_fn) + 1
    print(f"The maximum optimal number of pours is {max(f_n)} when n = {max_n}")

fiddler_pours_solve()

    
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