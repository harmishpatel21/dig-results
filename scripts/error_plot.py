from unicodedata import name
import plotly.graph_objects as go
import streamlit as st
import numpy as np

def error_graph(df, col1, col2, string):
    print(f'{string}')
    mean1 = df[col1].mean()
    mean2 = df[col2].mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = [mean1]*len(df[col1]),
        y = np.arange(0, 100),
        mode = 'lines',
        name = f'mean of {col1}'
        )
    )
    fig.add_trace(go.Scatter(
        x = [mean2]*len(df[col2]),
        y = np.arange(0, 100),
        mode = 'lines',
        name = f'mean of {col2}'
        )
    )
    fig.add_trace(go.Scatter(
        x = df[col1],
        y = df[col2],
        mode = 'markers',
        name = col1
        )
    )
    
    # fig.add_trace(go.Scatter(
    #     x = df[col2],
    #     mode = 'markers',
    #     name = col2
    #     )
    # )
    # st.plotly_chart(fig)
    return fig