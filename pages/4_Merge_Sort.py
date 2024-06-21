import streamlit as st
import graphviz as gv

def merge_sort(arr, graph_list, merge_list, depth=0):
    if len(arr) > 1:
        left_arr = arr[:len(arr)//2]
        right_arr = arr[len(arr)//2:]

        graph = gv.Digraph(format='png')
        graph1 = gv.Digraph(format='png')
        graph.attr(rankdir='LR')
        graph1.attr(rankdir='LR')
        displayArr(left_arr, graph)
        displayArr(right_arr, graph1)
        if depth not in graph_list:
            graph_list[depth] = []
        graph_list[depth].append(graph)
        graph_list[depth].append(graph1)
        
        merge_sort(left_arr, graph_list, merge_list, depth+1)
        merge_sort(right_arr, graph_list, merge_list, depth+1)

        i = 0
        j = 0
        k = 0

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] < right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
        
        merge_graph = gv.Digraph(format='png')
        merge_graph.attr(rankdir='LR')
        displayArr(arr, merge_graph)
        if depth not in merge_list:
            merge_list[depth] = []
        merge_list[depth].append(merge_graph)

def displayArr(arr, graph):
    for i in range(len(arr)):
        graph.node(str(i), str(arr[i]))
        if i != 0:
            graph.edge(str(i-1), str(i))

st.title("Merge Sort Visualization")

input_array = st.text_input("Enter an array (comma-separated):", "8, 2, 5, 3, 4, 7, 6, 1")
arr = list(map(int, input_array.split(',')))

if st.button("Visualize Merge Sort"):
    graph_list = {}
    merge_list = {}
    merge_sort(arr, graph_list, merge_list)

    st.write("Divide")
    max_depth = max(graph_list.keys())
    for depth in range(max_depth + 1):
        graphs = graph_list.get(depth, [])
        cols = st.columns(len(graphs))
        for i, graph in enumerate(graphs):
            with cols[i]:
                st.graphviz_chart(graph)

    st.write("Merging:")
    for depth in reversed(range(max_depth + 1)):
        graphs = merge_list.get(depth, [])
        cols = st.columns(len(graphs))
        for i, graph in enumerate(graphs):
            with cols[i]:
                st.graphviz_chart(graph)
