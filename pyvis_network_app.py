import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Read dataset (CSV)
df_data = pd.read_csv('data/transaction_data.csv')
df_chem_list = pd.read_csv('data/chem_list.csv')
df_agency_list = pd.read_csv('data/agency_list.csv')
df_contractor_list = pd.read_csv('data/contractor_list.csv')

df_nodes = pd.read_csv('data/nodes.csv')
df_edges = pd.read_csv('data/edges.csv')

# Set header title
st.title('Network Graph Visualization of the Federal Chemical Market')

# Define list of selection options and sort alphabetically
chem_list = df_chem_list['Chemicals'].tolist()
chem_list.sort()
agency_list = df_agency_list['Agency'].tolist()
agency_list.sort()
contractor_list = df_contractor_list['Contractor'].tolist()
contractor_list.sort()

# Group transaction data by chemical, agency, contractor, and sum
df_data['amount'] = pd.to_numeric(df_data['amount'], errors='coerce')
df_data['amount'].dtypes
x = df_data.groupby(['chemical', 'agency', 'contractor']).agg({'amount': ['sum']})
x = x.reset_index()

# Implement multiselect dropdown menu for option selection (returns a list)
selected_chem = st.selectbox('Choose a chemical to explore!', chem_list)

# Set info message on initial site load
if len(selected_chem) == 0:
    st.text('Make a selection from the list')

# Create network graph when user selects >= 1 item                                                                     
else:
    df_select = df_data.loc[df_data['chemical'] == selected_chem]
    df_select = df_select.reset_index(drop=True)                                               #Need to get the weights here

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'contractor', 'agency')

    
    # Initiate PyVis network object
    drug_net = Network(
                       height='810px',
                       width='100%',                                                        #Can we color different kinds of nodes differently? YES, GROUP=1 or GROUP=2....
                       bgcolor='#222222',                                                   
                       font_color='white'
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout settings
    drug_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,                                                 #Is there something we can do to show the size of the contract? YES, SIZE = XXX
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = './html_files'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')
    
    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)

# Footer
st.markdown(
    """
    <br>
    <h6>Data source: Deep Water Point, Aug 26. Data includes $2.8B worth of product-only contracts. Ask Scott for more details.</h6>
    """, unsafe_allow_html=True
    )
