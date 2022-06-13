import plotly.figure_factory as ff
import streamlit as st
import numpy as np
import plotly.graph_objects as go

def distribution_plot(df, col1, col2, string, bins, histnorm, show_hist=True):
    x1 = df[col1]
    x2 = df[col2]
    hist_data = [x1, x2]
    group_labels = [col1, col2]
    fig = ff.create_distplot(
        hist_data,
        group_labels,
        curve_type='normal',
        bin_size=bins,
        show_rug=False,
        histnorm=histnorm,
        show_hist=show_hist
    )

    fig.update_layout(
        title = f'Distribution Plot - {string}',
        xaxis_title = f'{string} Depth (%)',
        yaxis_title = f'{"Count" if histnorm == "" else histnorm}',
        width=900,
        height=700,
        xaxis = dict(
            tick0 = 0,
            dtick = bins),
        bargap = 0.01,
        showlegend = True
    )
    st.plotly_chart(fig) 
    return None
