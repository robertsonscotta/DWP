import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
from scipy.stats import zscore

# Read dataset (CSV)
df_data = pd.read_csv('data/transaction_data.csv')
df_chem_list = pd.read_csv('data/chem_list.csv')
df_sub_data = pd.read_csv('data/sub_data.csv')
# df_sub_list = pd.read_csv('data/sub_list.csv')

# Set header title
st.image('data/logo.png', width=200)
st.title('Network Graph Visualization of the Federal Chemical Market')

# Define list of selection options and sort alphabetically
chem_list = df_chem_list['Chemicals'].tolist()
chem_list.sort()
chem_list.insert(0,'All')

# Group transaction data by chemical, agency, contractor, and sum
df_data['amount'] = pd.to_numeric(df_data['amount'], errors='coerce')
x = df_data.groupby(['chemical', 'agency', 'contractor']).agg({'amount': ['sum']})
x = x.reset_index()

#Group prime/sub relationships
# Group transaction data by chemical, agency, contractor, and sum
df_sub_data['amount'] = pd.to_numeric(df_sub_data['amount'], errors='coerce')
y = df_sub_data.groupby(['prime', 'sub']).agg({'amount': ['sum']})
y = y.reset_index()

# Implement multiselect dropdown menu for option selection (returns a list)
sub_list = ['Prime Contracts', 'Prime-Sub Relationships']
select_mode = st.selectbox('Choose to display prime contracts or prime/sub relationships:', sub_list)
selected_chem = st.selectbox('Choose a chemical to explore!', chem_list)

#Choose Display Mode
if select_mode == 'Prime Contracts':

    # Set info message on initial site load
    if selected_chem == 'All':
        g = Network(
                       height='1000px',
                       width='100%',                                                       
                       bgcolor='#222222',                                                   
                       font_color='white'
                      )
        x_sel = x

        f = x_sel['agency'].unique().tolist()
        m = x_sel['contractor'].unique().tolist()
        tot_list = f + m

        z = 0
        for point in range(len(f)):
            g.add_node(z, label=f[point], color='#F17B7B')
            z += 1
        for points in range(len(m)):
            g.add_node(z, label=m[points], value=.1, color='#6F7CDB')
            z += 1

        df_track = pd.DataFrame(tot_list)
        agen_list = x_sel['agency'].tolist()
        cont_list = x_sel['contractor'].tolist()

        d = x_sel['amount'].apply(zscore).values.tolist()
        weight_list = []
        for numbers in range(len(d)):
            weight_list.append(d[numbers][0])
        floor = min(weight_list)
        wt_list = [x-floor for x in weight_list]

        agen_list = [df_track.index[df_track[0] == agen_list[t]].tolist()[0] for t in range(len(agen_list))]
        cont_list = [df_track.index[df_track[0] == cont_list[u]].tolist()[0] for u in range(len(cont_list))]

        for i in range(len(agen_list)):
            g.add_edge(agen_list[i], cont_list[i], value=wt_list[i])


        # Generate network with specific layout settings
        g.repulsion(
                            node_distance=420,
                            central_gravity=0.33,
                            spring_length=110,                                                 
                            spring_strength=0.10,
                            damping=0.95
                           )

        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            path = '/tmp'
            g.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
        except:
            path = './html_files'
            g.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=435)

    # Create network graph when user selects >= 1 item                                                                     
    else:
        # Initiate PyVis network object
        g = Network(
                           height='1000px',
                           width='100%',                                                       
                           bgcolor='#222222',                                                   
                           font_color='white'
                          )
        x_sel = x.loc[x['chemical'] == selected_chem]
        x_sel = x_sel.reset_index()

        f = x_sel['agency'].unique().tolist()
        m = x_sel['contractor'].unique().tolist()
        tot_list = f + m

        z = 0
        for point in range(len(f)):
            g.add_node(z, label=f[point], color='#F17B7B')
            z += 1
        for points in range(len(m)):
            g.add_node(z, label=m[points], value=.1, color='#6F7CDB')
            z += 1

        df_track = pd.DataFrame(tot_list)
        agen_list = x_sel['agency'].tolist()
        cont_list = x_sel['contractor'].tolist()

        d = x_sel['amount'].apply(zscore).values.tolist()
        weight_list = []
        for numbers in range(len(d)):
            weight_list.append(d[numbers][0])
        floor = min(weight_list)
        wt_list = [x-floor for x in weight_list]

        agen_list = [df_track.index[df_track[0] == agen_list[t]].tolist()[0] for t in range(len(agen_list))]
        cont_list = [df_track.index[df_track[0] == cont_list[u]].tolist()[0] for u in range(len(cont_list))]

        for i in range(len(agen_list)):
            g.add_edge(agen_list[i], cont_list[i], value=wt_list[i])


        # Generate network with specific layout settings
        g.repulsion(
                            node_distance=420,
                            central_gravity=0.33,
                            spring_length=110,                                                 
                            spring_strength=0.10,
                            damping=0.95
                           )

        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            path = '/tmp'
            g.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
        except:
            path = './html_files'
            g.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=435)

else:
    g = Network(
                       height='1000px',
                       width='100%',                                                       
                       bgcolor='#222222',                                                   
                       font_color='white'
                      )

    f = y['prime'].unique().tolist()
    m = y['sub'].unique().tolist()
    tot_list = f + m

    z = 0
    for point in range(len(f)):
        g.add_node(z, label=f[point], color='#F17B7B')
        z += 1
    for points in range(len(m)):
        g.add_node(z, label=m[points], value=.1, color='#6F7CDB')
        z += 1

    df_track = pd.DataFrame(tot_list)
    agen_list = y['prime'].tolist()
    cont_list = y['sub'].tolist()

    d = y['amount'].apply(zscore).values.tolist()
    weight_list = []
    for numbers in range(len(d)):
        weight_list.append(d[numbers][0])
    floor = min(weight_list)
    wt_list = [x-floor for x in weight_list]

    agen_list = [df_track.index[df_track[0] == agen_list[t]].tolist()[0] for t in range(len(agen_list))]
    cont_list = [df_track.index[df_track[0] == cont_list[u]].tolist()[0] for u in range(len(cont_list))]

    for i in range(len(agen_list)):
        g.add_edge(agen_list[i], cont_list[i], value=wt_list[i])


    # Generate network with specific layout settings
    g.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,                                                 
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        g.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = './html_files'
        g.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)
        
        
        
# Footer
st.markdown(
    """
    <br>
    <h4>Red circles represent federal agencies | Blue circles represent companies</h4>
    <h4>Line weight is proportional to contract size for the chemical group selected</h4>
    <h6></h6>
    <h6>Data source: Deep Water Point, Sep 2021. Data includes 27,186 transaction worth $13.4B. Ask <b>Scott</b> for more details.</h6>
    """, unsafe_allow_html=True
    )
