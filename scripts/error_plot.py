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
        y = np.arange(0, 1, 0.1),
        mode = 'lines'
        )
    )
    fig.add_trace(go.Scatter(
        x = [mean2]*len(df[col2]),
        y = np.arange(0, 1, 0.1),
        mode = 'lines'
        )
    )
    fig.add_trace(go.Scatter(
        x = df[col1],
        mode = 'markers'
        )
    )
    fig.add_trace(go.Scatter(
        x = df[col2],
        mode = 'markers'
        )
    )
    st.plotly_chart(fig)
    return fig