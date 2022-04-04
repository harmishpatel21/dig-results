from tkinter import Y
from scripts import data_preparation as dp
from components.inputs import file, get_measurement_errors
from components.metalloss import metal_loss
from components.dent import dent
import streamlit as st

def main():
    try:
        data = file()
        wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, metalloss_measurement_error_in_dent, confidence_interval = get_measurement_errors()
    except:
        pass
    
    try:
        data = dp.clean_data(data)
        dent_df = dp.filter_data(data, 'ILI_Anomaly Type', 'Dent')
        metalloss_df = data[data['ILI_Anomaly Type'] != 'Dent']
        metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'].notnull()]
    except:
        pass

    # dent_df = dp.filter_data(data, 'ILI_Anomaly Type', 'Dent')
    # metalloss_df = data[data['ILI_Anomaly Type'] != 'Dent']
    # metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'].notnull()]

    try:
        metal_loss(metalloss_df, wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, confidence_interval)
    except:
        st.error('No Metal Loss Data available')

    try:
        dent(dent_df, metalloss_measurement_error_in_dent, confidence_interval)
    except:
        st.error('No Dent Data available')
    return None