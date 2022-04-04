import numpy as np
import plotly.graph_objects as go
import streamlit as st

def add_unity_range(fig, string):
    if string == 'Metal Loss':
        range_x = np.arange(0, 91, 1)
        range_y = np.arange(10, 91, 1)
        range_mid = np.arange(0, 91, 1)
        tick0 = 10
        dtick = 10
    else:
        range_x = np.arange(0, 11, 1)
        range_y = np.arange(1, 11, 1)
        range_mid = np.arange(0, 11, 1)
        tick0 = 1
        dtick = 1
    
    fig.add_trace(go.Scatter(
        x = range_mid,
        y = range_mid,
        mode = 'lines',
        line = dict(color='black', width=1),
        opacity = 0.5,
        name = 'Unity Line'
    ))

    fig.add_trace(go.Scatter(
        y = range_y,
        x = range_x,
        mode = 'lines',
        line = dict(color='green', width=1),
        name = '± 10%'
    ))

    fig.add_trace(go.Scatter(
        y = range_x,
        x = range_y,
        mode = 'lines',
        line = dict(color='green', width=1),
        showlegend = False
    ))

    fig.update_layout(
        title = f'Unity Plot - {string}',
        width = 900,
        height = 700,
        xaxis = dict(
            tick0 = tick0,
            dtick = dtick
        ),
        yaxis = dict(
            tick0 = tick0,
            dtick = dtick
        )
    )
    return fig

def unity_plot(df, col1, col2, string, col3 = 'ILI_Metal Loss Class'):
    fig = go.Figure()
    if string == 'Metal Loss':
        u_metalloss_classes = df[col3].unique()
        # u_metalloss_classes = np.unique(df[col3].values)
        d = dict(zip(u_metalloss_classes, np.arange(len(u_metalloss_classes))))
        for i in df[col3].unique():
            fig.add_trace(go.Scatter(
                x=df[df[col3] == i][col1],
                y=df[df[col3] == i][col2],
                mode='markers',
                marker=dict(
                    color=d[i],
                    opacity=0.8
                ),
                name=i
            ))
    else:
        fig.add_trace(go.Scatter(
                x=df[col1],
                y=df[col2],
                mode='markers',
                name='Dent'
        ))
    fig = add_unity_range(fig, string)

    fig.update_layout(
        xaxis_title = col1,
        yaxis_title = col2
    )
    st.plotly_chart(fig)
    return fig