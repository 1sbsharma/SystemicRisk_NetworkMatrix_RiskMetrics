import pandas as pd
import networkx as nx
import plotly.graph_objects as go

def create_network_graph(
    adjacency_df: pd.DataFrame, 
    institution_names: list,
    node_size_metric: pd.Series,
    node_color_metric: pd.Series,
    size_label: str,
    color_label: str
) -> go.Figure:
    """
    Creates an interactive network graph using Plotly.

    Parameters:
    - adjacency_df: DataFrame of the adjacency matrix.
    - institution_names: List of institution names for hover labels.
    - node_size_metric: Series of values to determine node size.
    - node_color_metric: Series of values to determine node color.
    - size_label: Label for the size metric (for hover info).
    - color_label: Label for the color metric (for hover info).

    Returns:
    - go.Figure: A Plotly figure object.
    """
    # Create a graph from the adjacency matrix
    G = nx.from_pandas_adjacency(adjacency_df)
    pos = nx.spring_layout(G, k=0.5, iterations=50) # Force-directed layout

    # --- Create Edge Trace ---
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # --- Create Node Trace ---
    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
    node_hover_text = [
        f"<b>{name}</b><br>"
        f"{size_label}: {size:.4f}<br>"
        f"{color_label}: {color:.4f}"
        for name, size, color in zip(institution_names, node_size_metric, node_color_metric)
    ]

    # Create node labels (just numbers: 1, 2, 3, ...)
    node_labels = [str(i+1) for i in range(len(G.nodes()))]
    
    # Calculate node sizes based on compromise score
    # Base size is 30, scaled by compromise score (or keep base size if score is 0)
    base_size = 30
    node_sizes = [base_size * metric if metric > 0 else base_size for metric in node_size_metric]
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_labels,
        textposition="middle center",
        textfont=dict(
            size=18,
            color='white',
            family='Arial Black'
        ),
        hovertext=node_hover_text,
        marker=dict(
            showscale=False,
            color='#1f77b4',  # Solid blue color for all nodes
            size=node_sizes,  # Variable size based on compromise score
            line=dict(width=2, color='white')
        )
    )

    # --- Assemble Figure ---
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text='<br>Interactive Network Graph',
                font=dict(size=16)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[dict(
                text="Network visualization of financial institutions",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002)],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )
    return fig
