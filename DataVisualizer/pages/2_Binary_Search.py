import streamlit as st
import pandas as pd
import numpy as np
import graphviz as gv
import time

def vis_bs(low, high, arr, data, m_path, l_path, h_path): 
    if(high >= low):
        mid = low + (high - low) // 2
        m_path.append(mid)
        h_path.append(high)
        l_path.append(low)
        if arr[mid] == data:
            return mid, m_path, h_path, l_path
        elif arr[mid] > data:
            return vis_bs(low, mid-1, arr, data, m_path, h_path, l_path)
        else:
            return vis_bs(mid+1, high, arr, data, m_path, h_path, l_path)
    else:
        return -1, m_path, h_path, l_path

def binarySearch(arr, data):
    high = len(arr) - 1
    low = 0
    m_path = []
    l_path = []
    h_path = []
    return vis_bs(low, high, arr, data, m_path, l_path, h_path)

def display(arr, m_path, h_path, l_path, pace):
    g = gv.Digraph(format='png')
    g.attr(rankdir='LR')
    for i in range(len(arr)):
        g.node(str(i), str(arr[i]))
        if(i>0):
            g.edge(str(i-1), str(i))
 
    for step in range(len(m_path)):
        g.node(str(h_path[step]), color = 'red', style = 'filled', fontcolor = 'white')
        g.node(str(l_path[step]), color = 'red', style = 'filled', fontcolor = 'white')
        g.node(str(m_path[step]), color = 'blue', style = 'filled', fontcolor = 'white')
        st.graphviz_chart(g)
        col1, col2, col3 = st.columns(3)
        col1.metric("Upper Bound:", arr[h_path[step]])
        col2.metric("Lower Bound:", arr[l_path[step]])
        col3.metric("Middle:", arr[m_path[step]])
        
        time.sleep(pace)
        g.node(str(m_path[step]), str(arr[m_path[step]]), color = 'black', style = 'solid', fontcolor = 'black')
        g.node(str(h_path[step]), str(arr[h_path[step]]), color = 'black', style = 'solid', fontcolor = 'black')
        g.node(str(l_path[step]), str(arr[l_path[step]]), color = 'black', style = 'solid', fontcolor = 'black')
        

if 'arr' not in st.session_state:
    st.session_state.arr = []

add_value = st.number_input("Enter a value to add to the Array", min_value=1, max_value=100, step=1, value=1)

if st.button("Add"):
    if(add_value not in st.session_state.arr):
        st.session_state.arr.append(add_value)
    st.session_state.arr.sort()
st.write("Array:", ', '.join(map(str, st.session_state.arr)))

find_val = st.number_input("Enter a value to locate in the Array", min_value=1, max_value=100, step=1, value=1)

pace = st.slider("Speed", min_value = 1, max_value = 5)

mid = None
if st.button("Start"):
    mid, m_path, h_path, l_path = binarySearch(st.session_state.arr, find_val)
    display(st.session_state.arr, m_path, h_path, l_path, pace)
if mid is not None:
    if mid != -1:
        st.success("Found Element")
        print(mid)
    else:
        st.error("Does Not Contain Element")
        print(mid)



