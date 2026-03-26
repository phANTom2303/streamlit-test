import streamlit as st
from src.graph_utils import build_adjacency_list
from src.algorithms import bidirectional_bfs, unidirectional_bfs
from src.plotting import generate_graph_figure

st.set_page_config(page_title="BFS Visualizer", layout="wide")

st.title("Step-by-Step BFS Visualizer")

# Sidebar for inputs
with st.sidebar:
    st.header("Graph Configuration")
    nodes = st.number_input("Number of Cities (Nodes)", min_value=2, value=12)
    source = st.number_input("Source City", min_value=1, max_value=nodes, value=1)
    destination = st.number_input("Destination City", min_value=1, max_value=nodes, value=12)
    
    st.subheader("Edges Input")
    default_edges = "1 2\n1 5\n1 3\n2 4\n3 6\n4 5\n5 6\n4 7\n5 8\n6 9\n7 10\n8 10\n8 11\n9 11\n10 12\n8 12\n11 12"
    edges_text = st.text_area("Edges", value=default_edges, height=300)
    
    run_btn = st.button("Generate Algorithm Data", type="primary")

# Run the algorithms ONCE and save to memory
if run_btn:
    try:
        adjList = build_adjacency_list(nodes, edges_text)
        
        # Save to session_state so it persists when sliders move
        st.session_state['adjList'] = adjList
        st.session_state['bi_history'] = bidirectional_bfs(nodes, adjList, source, destination)
        st.session_state['uni_history'] = unidirectional_bfs(nodes, adjList, source, destination)
        st.session_state['data_ready'] = True
    except Exception as e:
        st.error(f"An error occurred. Check your inputs. Error: {e}")

# If data is in memory, render the UI
if st.session_state.get('data_ready'):
    adjList = st.session_state['adjList']
    bi_hist = st.session_state['bi_history']
    uni_hist = st.session_state['uni_history']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bidirectional BFS")
        # The Slider connects to the length of the history array
        step_bi = st.slider("Time Travel (Step)", 0, len(bi_hist) - 1, 0, key="slider_bi")
        
        # Grab the specific snapshot based on the slider
        state_bi = bi_hist[step_bi]
        fig_bi = generate_graph_figure(adjList, state_bi['visited'], state_bi['path'], f"Bidirectional (Step {step_bi})")
        st.pyplot(fig_bi)
        
        if state_bi['path']:
            st.success(f"Path Found! Length: {len(state_bi['path']) - 1} edges.")
            st.write(f"**Path:** {state_bi['path']}")
            
    with col2:
        st.subheader("Unidirectional BFS")
        step_uni = st.slider("Time Travel (Step)", 0, len(uni_hist) - 1, 0, key="slider_uni")
        
        state_uni = uni_hist[step_uni]
        fig_uni = generate_graph_figure(adjList, state_uni['visited'], state_uni['path'], f"Unidirectional (Step {step_uni})")
        st.pyplot(fig_uni)
        
        if state_uni['path']:
            st.success(f"Path Found! Length: {len(state_uni['path']) - 1} edges.")
            st.write(f"**Path:** {state_uni['path']}")