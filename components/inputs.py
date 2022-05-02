
import streamlit as st
import pandas as pd
from scripts.data_preparation import read_data

def get_inputs(string, value):
    try:
        user_input = st.sidebar.text_input(string, value)
        return float(user_input)
    except:
        pass
    # return float(user_input)

def file():
    try:
        uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
        if uploaded_file is not None:
            df = read_data(uploaded_file)
            return df
    except:
        pass
    
def get_measurement_errors():
    wallthickness_measurement_error_in = get_inputs('Wall thickness measurement error in (inches)', 0)
    metalloss_measurement_error_in_ml = get_inputs('Metal loss measurement error in metal loss in (inches)', 0)
    metalloss_measurement_error_in_dent = get_inputs('Metal loss measurement error in Dent in (inches)', 0)

    confidence_interval = get_inputs('Confidence Interval', 80)
    return wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, metalloss_measurement_error_in_dent, confidence_interval

