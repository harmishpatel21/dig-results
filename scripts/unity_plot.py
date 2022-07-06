import numpy as np
import plotly.graph_objects as go
import streamlit as st

def get_min_max(df, col1, col2):
    max_value = max([x for i in zip(df[col1], df[col2]) for x in i])
    min_value = min([x for i in zip(df[col1], df[col2]) for x in i])
    return max_value, min_value

def set_range(string, max_value, min_value):
    if string == "Metal Loss":
        range_x = np.arange(0, 86, 1)
        range_y = np.arange(10, 86, 1)
        tick0 = 10
        dtick = 5
        name = '± 10%'

    elif string == "Dent":
        range_x = np.arange(0, 10, 1)
        range_y = np.arange(0.5, 10, 1)
        tick0 = 1
        dtick = 1
        name = '± 0.5%'

    elif string == "Length" or string == "Width":
        range_x = np.arange(0, np.floor(max_value)+1.05, 0.05)
        range_y = np.arange(0.35, np.floor(max_value)+1.05, 0.05)
        tick0 = 0.35
        dtick = 0
        name  = '± 0.35in./± 9mm'
    
    elif string == "Orientation":
        range_x = np.arange(0, 12, 1)
        range_y = np.arange(1, 12, 1)
        tick0 = 1
        dtick = 1
        name = 'Orientation tolerance'

    elif string == "Pressure":
        range_x = np.arange(np.ceil(min_value/100)*100-100, np.floor(max_value/100)*100+100, 1)
        range_y = np.arange(np.ceil(min_value/100)*100-75, np.floor(max_value/100)*100+100, 1)
        tick0 = 100
        dtick = 25
        name = '± 25 Pressure tolerance'

    else:
        range_x = np.arange(0, 11, 1)
        range_y = np.arange(1, 11, 1)
        tick0 = 1
        dtick = 1
    return range_x, range_y, tick0, dtick, name

def add_unity_range(fig, string, max_value, min_value):
    range_x, range_y, tick0, dtick, name = set_range(string, max_value, min_value)
    fig.add_trace(go.Scatter(
        x = range_x,
        y = range_x,
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
        name = name
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
            dtick = dtick,
            rangemode = 'nonnegative', 
        ),
        yaxis = dict(
            tick0 = tick0,
            dtick = dtick,
            rangemode = 'nonnegative',
    ))
    return fig

def unity_plot(df, col1, col2, string, col3 = 'ILI_Metal Loss Class'):
    max_value, min_value = get_min_max(df, col1, col2)
    # print(max_value, min_value)
    fig = go.Figure()

    if string == "Length" or string == "Width" or string == 'Metal Loss':
        for i in df[col3].unique():
            fig.add_trace(go.Scatter(
                x = df[col1][df[col3] == i],
                y = df[col2][df[col3] == i],
                mode = 'markers',
                name = i
            ))
    else:
        fig.add_trace(go.Scatter(
                x=df[col1],
                y=df[col2],
                mode='markers',
                name=string
        ))
    fig = add_unity_range(fig, string, max_value, min_value)

    fig.update_layout(
        xaxis_title = col1,
        yaxis_title = col2
    )
    st.plotly_chart(fig)
    return fig