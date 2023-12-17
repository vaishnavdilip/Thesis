import igraph as ig
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from chart_studio import plotly as py
from plotly.graph_objs import *
from plotly.offline import iplot
from py2neo import Graph

def plot_connections(df, predictions):

    df['prediction'] = predictions

    df['node1'] = df['node1'].astype(str)
    df['node2'] = df['node2'].astype(str)

    df = df.sample(n=100, random_state=1)

    nodes = list(set(df['node1'].unique()).union(set(df['node2'].unique())))
    edges_real = df.loc[df['label'] == 1, ['node1', 'node2']]
    edges_predicted = df.loc[df['prediction'] == 1, ['node1', 'node2']]
    edges_real = list(edges_real.itertuples(index=False, name=None))
    edges_predicted = list(edges_predicted.itertuples(index=False, name=None))

    g = ig.Graph()
    g.add_vertices(nodes)
    g.add_edges(edges_real)
    g.add_edges(edges_predicted)

    N = len(g.vs)
    E_real = [e.tuple for e in g.es if (g.vs[e.tuple[1]]['name'],g.vs[e.tuple[0]]['name']) in edges_real]
    E_predicted = [e.tuple for e in g.es if (g.vs[e.tuple[1]]['name'],g.vs[e.tuple[0]]['name']) in edges_predicted]

    labels = get_info(g.vs['name'])['name'].tolist()

    layt = g.layout("fr")

    Xn = [layt[k][0] for k in range(N)]
    Yn = [layt[k][1] for k in range(N)]

    Xe_real = []
    Ye_real = []

    Xe_predicted = []
    Ye_predicted = []

    for e in E_real:
        Xe_real += [layt[e[0]][0], layt[e[1]][0], None]
        Ye_real += [layt[e[0]][1], layt[e[1]][1], None]

    for e in E_predicted:
        Xe_predicted += [layt[e[0]][0], layt[e[1]][0], None]
        Ye_predicted += [layt[e[0]][1], layt[e[1]][1], None]

    fig = go.Figure()

    trace1 = go.Scatter(x=Xe_real,
                        y=Ye_real,
                        mode = 'lines',
                        line = dict(
                            color='green', 
                            width=1,
                            ),
                        hoverinfo = 'none',
                        name = 'real',
                        showlegend=True
                        )

    trace2 = go.Scatter(x=Xe_predicted,
                        y=Ye_predicted,
                        mode = 'lines',
                        line = dict(
                            color='green', 
                            width=1,
                            shape = 'spline',
                            dash = 'dot'
                            ),
                        hoverinfo = 'none',
                        name = 'predicted',
                        showlegend=True
                        )

    trace3 = go.Scatter(x=Xn,
                        y=Yn,
                        mode='markers',
                        marker=dict(
                                    symbol='circle',
                                    size=10,
                                    color='red',                                
                                    ),
                        text=labels,
                        hoverinfo='text',
                        showlegend=False
                        )


    fig.add_trace(trace3)
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

    fig.update_layout(title="Random test graph",
                        font=dict(size=12),
                        showlegend=True,
                        autosize=False,
                        width=800,
                        height=800,
                        margin=layout.Margin(
                            l=40,
                            r=40,
                            b=85,
                            t=100,
                        ),
                        hovermode='closest',
                        # annotations=[
                        #     dict(
                        #         showarrow=False,
                        #         text='This igraph.Graph has the Kamada-Kawai layout',
                        #         xref='paper',
                        #         yref='paper',
                        #         x=0,
                        #         y=-0.1,
                        #         xanchor='left',
                        #         yanchor='bottom',
                        #         font=dict(
                        #             size=14
                        #         )
                        #     )
                        # ]
                        )
    return fig

def get_info(vertices):

    graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4jneo4j"))

    query = """ 
    UNWIND $vertices AS vertex
    MATCH (p:Company) WHERE p.id = toString(vertex)
    RETURN p.id AS id, p.name AS name
    """

    params = {"vertices": vertices}

    t = graph.run(query, params).to_data_frame()

    return t