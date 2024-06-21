import streamlit as st
import graphviz
import numpy as np

class BST:
    def __init__(self, size):
        self.arr = [None] * size
        self.graph = graphviz.Digraph()
    
    def add(self, data: int):
        if data not in self.arr:
            add_p = [0]
            i = 0
            while self.arr[i] is not None:
                add_p.append(i)
                if data > self.arr[i]:
                    i = (i * 2) + 2
                else:
                    i = (i * 2) + 1
                if i >= len(self.arr):
                    print("array full")
                    break
            add_p.append(i)
            if i < len(self.arr):
                self.arr[i] = data
            return add_p
        else:
            res, path = self.find(data)
            return path

    def __str__(self):
        return str(self.arr)

    def find(self, data: int):
        path = [0]
        ret = self.findHelper(path, data, 0)
        return ret, path

    def findHelper(self, path, data: int, curr):
        if curr > len(self.arr) - 1:
            return -1
        path.append(curr)
        if self.arr[curr] is None:
            return -1
        if self.arr[curr] == data:
            return curr
        elif self.arr[curr] > data:
            return self.findHelper(path, data, curr * 2 + 1)
        else:
            return self.findHelper(path, data, curr * 2 + 2)

    def displayTree(self, path=[]):
        self.graph = graphviz.Digraph()
        if self.arr[0] is not None:
            self.graph.node(str(0), str(self.arr[0]))
            self.visualHelper(0, 1, path)
            self.visualHelper(0, 2, path)
        else:
            st.write('No Arr')
        st.graphviz_chart(self.graph)

    def visualHelper(self, prev, curr, path):
        if curr < len(self.arr):
            if self.arr[curr] is not None:
                if curr in path:
                    self.graph.node(str(curr), str(self.arr[curr]), color='red')
                else:
                    self.graph.node(str(curr), str(self.arr[curr]))
                if curr in path:
                    self.graph.edge(str(prev), str(curr), color='red' if curr in path else 'black')
                else:
                    self.graph.edge(str(prev), str(curr))
                self.visualHelper(curr, curr * 2 + 1, path)
                self.visualHelper(curr, curr * 2 + 2, path)
            else:
                self.graph.node(str(curr), 'None', shape='ellipse', style='dotted')
                self.graph.edge(str(prev), str(curr), style='dotted')

if 'bst' not in st.session_state:
    st.session_state.bst = BST(35)

bst = st.session_state.bst

st.title("BST Visualization")
st.write("This application allows you to visualize a Binary Search Tree (BST) and perform operations such as adding and searching for elements.")

st.subheader("Add or Search for a Value in the BST")
col1, col2 = st.columns(2)

with col1:
    add_value = st.number_input("Enter a value to add to the BST", min_value=1, max_value=100, step=1, value=1)
    if st.button("Add"):
        add_path = bst.add(add_value)
        bst.displayTree(add_path)

with col2:
    search_value = st.number_input("Enter a value to search in the BST", min_value=1, max_value=100, step=1, value=5)
    if st.button("Search"):
        result, path = bst.find(search_value)
        if result == -1:
            st.write(f"Value {search_value} not found in BST.")
        else:
            st.write(f"Value {search_value} found at index {result}.")
        bst.displayTree(path)

st.divider()
st.subheader("Current BST")
bst.displayTree()
