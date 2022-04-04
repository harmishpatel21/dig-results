
import streamlit as st
import pandas as pd
from scripts.data_preparation import read_data

def get_inputs(string):
    try:
        user_input = st.text_input(string)
        return float(user_input)
    except:
        pass
    # return float(user_input)

def file():
    try:
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded_file is not None:
            df = read_data(uploaded_file)
            return df
    except:
        pass
    
def get_measurement_errors():
    wallthickness_measurement_error_in = get_inputs('wall thickness measurement error in')
    metalloss_measurement_error_in_ml = get_inputs('metalloss measurement error in metal loss')
    metalloss_measurement_error_in_dent = get_inputs('Metalloss measurement error in Dent')

    confidence_interval = get_inputs('Confidence interval')
    return wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, metalloss_measurement_error_in_dent, confidence_interval

