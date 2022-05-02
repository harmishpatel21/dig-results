import streamlit as st
from scripts import data_preparation as dp
from scripts import dataframe_operations as df_op
from scripts import get_statistics as gs
from scripts.unity_plot import unity_plot
from scripts.distribution_plot import distribution_plot


def dent(dent_df, metalloss_measurement_error_in_dent, confidence_interval):
    dent_df = df_op.dent_operations(
            dent_df, 
            metalloss_measurement_error_in_dent, 
            confidence_interval)
        
    dent_dataframe = st.checkbox('Show Dent Dataframe')
    if dent_dataframe:
        st.header('Dent Dataframe')
        st.write(dent_df)

    dent_statistics = st.checkbox('Show Dent Statistics')
    if dent_statistics:
        gs.statistics(dent_df, 'Dent Diff ILI_Depth - F_Depth', 'Dent Violates Confidence Criterion Out of Tolerance', 'Dent', confidence_interval)

    dent_unity_plot = st.checkbox('Show Dent Unity Plot')
    if dent_unity_plot:
        fig1 = unity_plot(dent_df, 'F_Dent Depth (%)', 'ILI_Dent Depth (%)', 'Dent')

    dent_distplot = st.checkbox('Show Dent Distribution Plot')
    if dent_distplot:
        bin_size = st.slider('Bin Size', 1, 10, 1)
        show_hist = st.checkbox("Show Histogram")
        histnorm = st.selectbox("Histogram Normalization", ['', 'probability'])
        distribution_plot(dent_df, 'ILI_Dent Depth (%)', 'F_Dent Depth (%)', 'Metal Loss', bin_size, histnorm, show_hist)

    

    export_dent_df = st.checkbox('Export Dent Dataframe')
    if export_dent_df:
        dp.export_data(dent_df, 'Calculated Dent dataframe')
    return None