from email.mime import base
import streamlit as st
import plotly.graph_objects as go

def count_plot(df, col1, col2):
    df_count1 = df.groupby(col1).size().reset_index(name='count')
    df_count2 = df.groupby(col2).size().reset_index(name='count')
    # print(df_count1, df_count2)
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_count1[col1], 
            y=[0-i for i in df_count1['count']], 
            base=0,
            name=col1,
            hovertemplate = '%{text}',
            text = [i for i in df_count1['count']])
    )
    fig.add_trace(
        go.Bar(
            x=df_count2[col2], 
            y=df_count2['count'],
            base=0, 
            name=col2,
            hovertemplate = '%{text}',
            text = [i for i in df_count1['count']])
    )

    fig.update_layout(
        title = f'Count Plot - {col1} vs {col2}',
        xaxis_title = 'Metal Loss Class',
        yaxis_title = 'Number of Anomalies',
        width=900,
        height=700
    )
    st.plotly_chart(fig)
    return None