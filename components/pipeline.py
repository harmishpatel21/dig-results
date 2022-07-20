from scripts import data_preparation as dp
from components.inputs import file, get_measurement_errors
from components.metalloss import metal_loss
from components.dent import dent
import streamlit as st
from os import listdir
import pandas as pd
import os

def tasks(data):
    data = dp.clean_data(data)
    dent_df = dp.filter_data(data, 'ILI_Anomaly Type', 'Dent')
    metalloss_df = data[data['ILI_Anomaly Type'] != 'Dent']
    metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'].notnull()]
    metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'] != 0]
    return metalloss_df, dent_df

def show_project_data(project_list, project_selected, folderpath):
    if len(project_selected) == 0:
        df = pd.DataFrame()
        for id, _ in enumerate(project_list):
            file_read = f'{folderpath}{project_list[id]}.csv'
            print(file_read)
            data = pd.read_csv(file_read)
            df = df.append(data, ignore_index=True)
        return df
    elif len(project_selected) == 1:
        file_read = f'{folderpath}{project_selected[0]}.csv'
        print(file_read)
        data = pd.read_csv(file_read)
        return data
    else:
        df = pd.DataFrame()
        for id, _ in enumerate(project_selected):
            file_read = f'{folderpath}{project_selected[id]}.csv'
            print(file_read)
            data = pd.read_csv(file_read)
            df = df.append(data, ignore_index=True)
        return df

def main():
    st.title('ENTEGRA - Dig Analysis for Defects')
    st.sidebar.title('Dig Result Statistics')
    masterDatabaseValue = st.sidebar.selectbox('Use Master database', options=['Yes','No'])
    if masterDatabaseValue == 'Yes':
        # folderpath = 'C:/projects/reports/dig stats/dig results/'
        # folderpath = 'D:/Data Science/Dig Results Database/'
        folderpath = st.text_input('Please enter path')
        # path = os.getcwd()
        newpath = os.path.join(folderpath,'')
        st.write(newpath)
        filepaths = [f for f in listdir(folderpath) if f.endswith('.csv')]
        client_list = list(set([(i.split('.')[0])[:3] for i in filepaths]))
        print(client_list)
        # client_list = list(set([(i.split('.')[0]).split('_')[0] for i in filepaths]))
        client_selected = st.sidebar.selectbox('Select Client Name', 
                                    options=client_list, 
                                    help='Choose the client from the list and project will be shown in followed tab.')
        # project_list = [(i.split('.')[0]).split('_')[1] for i in filepaths if client_selected in i]
        project_list = [i.split('.')[0] for i in filepaths if client_selected in i]
        project_selected = st.sidebar.multiselect('Select Project Name', 
                                    options=project_list, 
                                    help='You can select multiple projects, if none selected all the projects will be considered.')
        
        data = show_project_data(
            project_list, 
            project_selected, 
            folderpath) 
    
        metalloss_df, dent_df = tasks(data)
        wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, metalloss_measurement_error_in_dent, confidence_interval = get_measurement_errors()
        
        metal_loss(metalloss_df, 
                        wallthickness_measurement_error_in, 
                        metalloss_measurement_error_in_ml, 
                        confidence_interval)
    
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
            metalloss_df, dent_df = tasks(data)
            # data = dp.clean_data(data)
            # dent_df = dp.filter_data(data, 'ILI_Anomaly Type', 'Dent')
            # metalloss_df = data[data['ILI_Anomaly Type'] != 'Dent']
            # metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'].notnull()]
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

