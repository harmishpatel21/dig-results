import streamlit as st
from scripts import data_preparation as dp
from scripts import dataframe_operations as df_op
from components.inputs import file, get_measurement_errors
from scripts import get_statistics as gs
from scripts.unity_plot import unity_plot
from scripts.distribution_plot import distribution_plot


def metal_loss(metalloss_df, wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, confidence_interval):
    metalloss_df = df_op.ml_operations(
                metalloss_df, 
                wallthickness_measurement_error_in, 
                metalloss_measurement_error_in_ml,
                confidence_interval)
            
    ml_dataframe = st.checkbox('Show Metal loss Dataframe')
    if ml_dataframe:
        st.header('Metalloss Dataframe')
        st.write(metalloss_df)

    ml_stats = st.checkbox("Show Metal Loss Statistics")
    if ml_stats:
        gs.statistics(metalloss_df, 'ML Diff ILI_Depth - F_Depth', 'ML Violates Confidence Criterion Out of Tolerance', 'Metal Loss', confidence_interval)

    ml_unity_plot = st.checkbox('Show Metal Loss Unity Plot')
    if ml_unity_plot:
        ml_unity = unity_plot(metalloss_df, 'F_Metal Loss Depth (%)', 'ILI_Metal Loss Depth (%)', 'Metal Loss')

    ml_distplot = st.checkbox('Show Metal Loss Distribution Plot')
    if ml_distplot:
        bin_size = st.slider('Bin Size', 1, 10, 1, key='ml')
        show_hist = st.checkbox("Show Histogram", key='ml')
        histnorm = st.selectbox("Histogram Normalization", ['', 'probability'], key='ml')
        distribution_plot(metalloss_df, 'ILI_Metal Loss Depth (%)', 'F_Metal Loss Depth (%)', 'Metal Loss', bin_size, histnorm, show_hist)

    export_ml_df = st.checkbox('Export Metal Loss Dataframe')
    if export_ml_df:
        dp.export_data(metalloss_df, 'Metal Loss')
    return None
