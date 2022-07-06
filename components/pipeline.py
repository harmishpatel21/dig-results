from scripts import data_preparation as dp
from components.inputs import file, get_measurement_errors
from components.metalloss import metal_loss
from components.dent import dent
import streamlit as st
from os import listdir
import pandas as pd

def tasks(data):
    data = dp.clean_data(data)
    dent_df = dp.filter_data(data, 'ILI_Anomaly Type', 'Dent')
    metalloss_df = data[data['ILI_Anomaly Type'] != 'Dent']
    metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'].notnull()]
    return metalloss_df, dent_df

def show_project_data(client_selected, project_list, project_selected, folderpath):
    if len(project_selected) == 0:
        df = pd.DataFrame()
        for id, _ in enumerate(project_list):
            file_read = f'{folderpath}{client_selected}_{project_list[id]}.csv'
            data = pd.read_csv(file_read)
            df = df.append(data, ignore_index = True)
        return df
    elif len(project_selected) == 1:
        file_read = f'{folderpath}{client_selected}_{project_selected[0]}.csv'
        data = pd.read_csv(file_read)
        return data
    else:
        df = pd.DataFrame()
        for id, _ in enumerate(project_selected):
            file_read = f'{folderpath}{client_selected}_{project_selected[id]}.csv'
            data = pd.read_csv(file_read)
            df = df.append(data)
        return df

def main():
    st.title('ENTEGRA - Dig Analysis for Defects')
    st.sidebar.title('Dig Result Statistics')
    masterDatabaseValue = st.sidebar.selectbox('Use Master database', options=['Yes','No'])
    if masterDatabaseValue == 'Yes':
        folderpath = 'C:/projects/reports/dig stats/file format/'
        filepaths = [f for f in listdir(folderpath) if f.endswith('.csv')]
        client_list = list(set([(i.split('.')[0]).split('_')[0] for i in filepaths]))
        client_selected = st.sidebar.selectbox('Select Client Name', 
                                    options=client_list, 
                                    help='Choose the client from the list and project will be shown in followed tab.')
        project_list = [(i.split('.')[0]).split('_')[1] for i in filepaths if client_selected in i]
        project_selected = st.sidebar.multiselect('Select Project Name', 
                                    options=project_list, 
                                    help='You can select multiple projects, if none selected all the projects will be considered.')
        # st.write(project_selected)
        try:
            data = show_project_data(client_selected, 
                    project_list, 
                    project_selected, 
                    folderpath) 
        except:
            # st.error('Please select the options from drop-down menu')
            pass
        
        # button_clicked = st.sidebar.button('Calculate')
        # if button_clicked:
        metalloss_df, dent_df = tasks(data)
        wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, metalloss_measurement_error_in_dent, confidence_interval = get_measurement_errors()
        try:
            # wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, metalloss_measurement_error_in_dent, confidence_interval = get_measurement_errors()
            metal_loss(metalloss_df, 
                        wallthickness_measurement_error_in, 
                        metalloss_measurement_error_in_ml, 
                        confidence_interval)
        except:
            pass

        try:
            dent(dent_df, 
                metalloss_measurement_error_in_dent, 
                confidence_interval)
        except:
            pass

    else:
        try:
            data = file()
            wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, metalloss_measurement_error_in_dent, confidence_interval = get_measurement_errors()
        except:
            st.error('Please upload a CSV file')

        try:
            data = dp.clean_data(data)
            dent_df = dp.filter_data(data, 'ILI_Anomaly Type', 'Dent')
            metalloss_df = data[data['ILI_Anomaly Type'] != 'Dent']
            metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'].notnull()]
            metal_loss(metalloss_df, 
                        wallthickness_measurement_error_in, 
                        metalloss_measurement_error_in_ml, 
                        confidence_interval)
        except:
            pass

        try:
            dent(dent_df, 
                metalloss_measurement_error_in_dent, 
                confidence_interval)
        except:
            pass
    return None

