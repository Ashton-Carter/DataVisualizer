import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict

class dScalls:
    def shortestPath(self, n: int, edges: List[List[int]], src: int) -> Dict[int, int]:
        adj = {i: [] for i in range(n)}
        
        for s, d, weight in edges:
            adj[s].append((d, weight))

        shortest = {}
        minHeap = [(0, src)]
        steps = []
        
        while minHeap:
            w1, n1 = heapq.heappop(minHeap)
            
            if n1 in shortest:
                continue
            
            shortest[n1] = w1
            steps.append((n1, shortest.copy()))
            
            for n2, w2 in adj[n1]:
                if n2 not in shortest:
                    heapq.heappush(minHeap, (w1 + w2, n2))
        
        for i in range(n):
            if i not in shortest:
                shortest[i] = -1

        return shortest, steps

def draw_graph(edges, shortest_paths, steps):
    G = nx.DiGraph()
    for s, d, w in edges:
        G.add_edge(s, d, weight=w)
    
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    st.pyplot(plt)

    for step, (node, shortest) in enumerate(steps):
        st.write(f"Step {step + 1}: Visited node {node}")
        plt.figure()
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest.keys(), node_color='lightgreen')
        st.pyplot(plt)

st.title("Dijkstra's Algorithm Visualization")

default_edges = [
    [0, 1, 4], [0, 2, 1], [1, 3, 1], [2, 1, 2],
    [2, 3, 5], [3, 4, 3]
]
default_n = 5
default_src = 0

use_default = st.checkbox("Use default example graph", value=True)

if not use_default:
    n = st.number_input("Enter the number of nodes:", min_value=1, value=5, step=1)

    st.write("Enter the edges (source, destination, weight):")
    edges = []
    num_edges = st.number_input("Enter the number of edges:", min_value=1, value=5, step=1)
    for i in range(num_edges):
        col1, col2, col3 = st.columns(3)
        with col1:
            s = st.number_input(f"Edge {i+1} - Source:", min_value=0, max_value=n-1, step=1, key=f"source_{i}")
        with col2:
            d = st.number_input(f"Edge {i+1} - Destination:", min_value=0, max_value=n-1, step=1, key=f"destination_{i}")
        with col3:
            w = st.number_input(f"Edge {i+1} - Weight:", min_value=1, step=1, key=f"weight_{i}")
        edges.append([s, d, w])

    src = st.number_input("Enter the source node:", min_value=0, max_value=n-1, step=1)
else:
    n = default_n
    edges = default_edges
    src = default_src

if st.button("Compute Shortest Paths"):
    dijkstra = dScalls()
    shortest_paths, steps = dijkstra.shortestPath(n, edges, src)

    st.write("Shortest paths from the source node:")
    for node, distance in shortest_paths.items():
        st.write(f"Node {node}: {distance}")
    
    draw_graph(edges, shortest_paths, steps)
