import streamlit as st
from scripts import data_preparation as dp
from scripts import dataframe_operations as df_op
from scripts import get_statistics as gs
from scripts.error_plot import error_graph
from scripts.unity_plot import unity_plot
from scripts.distribution_plot import distribution_plot
from scripts.count_by_type import count_plot

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
        unity_plot(metalloss_df, 'F_Metal Loss Depth (%)', 'ILI_Metal Loss Depth (%)', 'Metal Loss')

    ml_distplot = st.checkbox('Show Metal Loss Distribution Plot')
    if ml_distplot:
        bin_size = st.slider('Bin Size', 1, 10, 1, key='ml')
        show_hist = st.checkbox("Show Histogram", key='ml')
        histnorm = st.selectbox("Histogram Normalization", ['', 'probability'], key='ml')
        distribution_plot(metalloss_df, 'F_Metal Loss Depth (%)', 'ILI_Metal Loss Depth (%)', 'Metal Loss', bin_size, histnorm, show_hist)
    
    if 'ILI_Length (in)' in metalloss_df.columns and 'F_Length (in)' in metalloss_df.columns:
        metalloss_df['ILI_Length (in)'] = metalloss_df['ILI_Length (in)'].astype(float)
        metalloss_df['F_Length (in)'] = metalloss_df['F_Length (in)'].astype(float)
        show_length_unity = st.checkbox('Show Length Unity Plot')
        if show_length_unity:
            print('Length Unity Plot')
            unity_plot(metalloss_df, 'F_Length (in)', 'ILI_Length (in)', 'Length')
    else:
        st.error('No Length Data available')
    
    if 'ILI_Width (in)' in metalloss_df.columns and 'F_Width (in)' in metalloss_df.columns:
        metalloss_df['ILI_Width (in)'] = metalloss_df['ILI_Length (in)'].astype(float)
        metalloss_df['F_Width (in)'] = metalloss_df['F_Width (in)'].astype(float)
        show_width_unity = st.checkbox('Show Width Unity Plot')
        if show_width_unity:
            print('Width Unity Plot')
            unity_plot(metalloss_df, 'F_Width (in)', 'ILI_Width (in)', 'Width')
    else:
        st.error('No Width Data available')
    
    if 'ILI_Clock Position' in metalloss_df.columns and 'F_Clock Position' in metalloss_df.columns:
        
        show_orientation_unity = st.checkbox('Show Orientation Unity Plot')
        if show_orientation_unity:
            print('Orientation Unity Plot')
            unity_plot(metalloss_df, 'F_Clock Position', 'ILI_Clock Position', 'Orientation')
    else:
        st.error('No Orientation Data available')
    
    if 'Actual_Burst_Pressure' in metalloss_df.columns and 'F_Burst_Pressure' in metalloss_df.columns:
        show_pressure_unity = st.checkbox('Show Pressure Unity Plot')
        if show_pressure_unity:
            print('Pressure Unity Plot')
            unity_plot(metalloss_df, 'Actual_Burst_Pressure', 'ILI_Burst_Pressure', 'Pressure')
    
    show_count_by_metalloss_class_type = st.checkbox('Show Count by Metal Loss Class Type')
    if show_count_by_metalloss_class_type:
        count_plot(metalloss_df, 'Actual_Metal Loss Class', 'ILI_Metal Loss Class')

    # error_plot = st.checkbox('Show Error Plot')
    # if error_plot:
    #     a = error_graph(metalloss_df, 'ILI_Metal Loss Depth (%)', 'F_Metal Loss Depth (%)', 'Metal Loss')


    export_ml_df = st.checkbox('Export Metal Loss Dataframe')
    if export_ml_df:
        dp.export_data(metalloss_df, 'Metal Loss')
    return None
