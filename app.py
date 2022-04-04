import pandas as pd
import numpy as np
import streamlit as st
import scipy.stats as stats
from plotly import graph_objects as go
import plotly.figure_factory as ff
import os



def read_data(path):
    df = pd.read_csv(path)
    return df

def export_data(df, string):
    path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # filename = f'{path}/{str(uploaded_file["name"].split(".")[0])}_export.csv'
    filename = f'{path}/{string}.csv'
    df.to_csv(filename, index=False)
    return None

def filter_data(df, col, val):
    return df[df[col] == val]

def clean_data(df):
    for i in df.columns:
        if '%' in i:
            df[i] = df[i].apply(lambda x: int(str(x).replace('%', '')) if '%' in str(x) else x)
    return df

def get_inputs(string):
    user_input = st.text_input(string)
    return float(user_input)

def z_value(confidence_interval, n_sided=2):
    return stats.norm.ppf(1-(1-confidence_interval/100)/n_sided)

def measurement_tolerance_within_confidence(value1, value2, confidence_interval):
    return (value1*z_value(confidence_interval)/value2*100).round(2)

def measurement_tolerance_within_confidence_metalloss(value1, value2, value3, value4, value5, confidence_interval):
    return z_value(confidence_interval)*np.sqrt((value1/value2)**2 + (value3/value4)**2)*value5

def measured_wt_loss_with_measured_tolerance(value1, value2):
    return value1+value2

def combined_measurement_error(value1, value2):
    return np.sqrt(value1**2 + value2**2).round(6)

def wt_loss_difference(value1, value2):
    return abs(value1-value2)

def get_tolerance(pipe_type, class_type):
    return tool_tolerance_data[tool_tolerance_data['Pipe Type'] == pipe_type][class_type].values[0]

def measurement_error_combined_tolerance(tolerance_value, value1):
    return np.sqrt(tolerance_value**2 + value1**2)

def is_violates_confidence(value1, value2):
    return 'Yes' if value1 > value2 else 'No'

def average_bias(df, col):
    return df[col].mean()

def standard_deviation(df, col):
    return df[col].std()

def conclusion_from_bias(avg):
    return 'Positive bias indicates -- ILI tool over-estimates depths on average' if avg > 0 else 'Negative bias indicates -- ILI tool under-estimates depths on average'


def statistics(df, col1, col2, string):
    st.header(f'Adjusted Tool Tolerance - {string}')
    avg_bias = average_bias(df, col1).round(2)
    bias_conclusion = conclusion_from_bias(avg_bias)
    std_dev = standard_deviation(df, col1).round(2)
    outlier = (std_dev/100)*2.5 if std_dev/100 > 0.1 else (std_dev/100)*3
    sample_size = df[col1].count()
    data_comparison  = len(df[df[col2] == 'No'])
    avg_bias_string = f'{avg_bias:.2f}'
    std_dev_string = f'Standard Deviation: **{std_dev:.2f}%**'
    outlier_string = f'Outliers: ± **{outlier.round(2)}**'
    sample_size_string = f'Sample Size: **{sample_size}** # Number of features with completed evaluations'
    st.markdown(sample_size_string)
    st.markdown(f'**{data_comparison}** of **{sample_size}** features are within the vendor stated **{confidence_interval}%** confidence interval')
    st.markdown(f'**{avg_bias_string}%** for each depth measurement in the tool; **{bias_conclusion}**')
    st.markdown(f'{std_dev_string} & {outlier_string}')
    return None


def add_unity_range(fig, string):
    if string == 'Metal Loss':
        range_x = np.arange(0, 91, 1)
        range_y = np.arange(10, 91, 1)
        range_mid = np.arange(0, 91, 1)
        tick0 = 10
        dtick = 10
    else:
        range_x = np.arange(0, 11, 1)
        range_y = np.arange(1, 11, 1)
        range_mid = np.arange(0, 11, 1)
        tick0 = 1
        dtick = 1
    
    fig.add_trace(go.Scatter(
        x = range_mid,
        y = range_mid,
        mode = 'lines',
        line = dict(color='black', width=1),
        opacity = 0.5,
        name = 'Unity Line'
    ))

    fig.add_trace(go.Scatter(
        y = range_y,
        x = range_x,
        mode = 'lines',
        line = dict(color='green', width=1),
        name = '± 10%'
    ))

    fig.add_trace(go.Scatter(
        y = range_x,
        x = range_y,
        mode = 'lines',
        line = dict(color='green', width=1),
        showlegend = False
    ))

    fig.update_layout(
        title = f'Unity Plot - {string}',
        width = 900,
        height = 700,
        xaxis = dict(
            tick0 = tick0,
            dtick = dtick
        ),
        yaxis = dict(
            tick0 = tick0,
            dtick = dtick
        )
    )
    return fig

def unity_plot(df, col1, col2, string, col3 = 'ILI_Metal Loss Class'):
    fig = go.Figure()
    if string == 'Metal Loss':
        u_metalloss_classes = df[col3].unique()
        # u_metalloss_classes = np.unique(df[col3].values)
        d = dict(zip(u_metalloss_classes, np.arange(len(u_metalloss_classes))))
        for i in df[col3].unique():
            fig.add_trace(go.Scatter(
                x=df[df[col3] == i][col1],
                y=df[df[col3] == i][col2],
                mode='markers',
                marker=dict(
                    color=d[i],
                    opacity=0.8
                ),
                name=i
            ))
    else:
        fig.add_trace(go.Scatter(
                x=df[col1],
                y=df[col2],
                mode='markers',
                name='Dent'
        ))
    fig = add_unity_range(fig, string)

    fig.update_layout(
        xaxis_title = col1,
        yaxis_title = col2
    )
    st.plotly_chart(fig)
    return fig

def distribution_plot(df, col1, col2, string, bins, histnorm, show_hist=True, col3 = 'Metal Loss Class'):
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
        show_hist=show_hist)
    
    fig.update_layout(
        title = f'Distribution Plot - {string}',
        xaxis_title = f'{string} Depth (%)',
        yaxis_title = f'{"Count" if histnorm == "" else histnorm}',
        width=900,
        height=700,
        xaxis = dict(
            tick0 = 0,
            dtick = bins
            ),
    bargap = 0.01,
    showlegend = True
    )
    st.plotly_chart(fig)
    return None


uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

wallthickness_measurement_error_in = get_inputs('wall thickness measurement error in')
metalloss_measurement_error_in_ml = get_inputs('metalloss measurement error in metal loss')
metalloss_measurement_error_in_dent = get_inputs('Metalloss measurement error in Dent')

confidence_interval = get_inputs('Confidence interval')

if uploaded_file is not None:
    data = read_data(uploaded_file)
    data = clean_data(data)
    tool_tolerance_data =  read_data('tool_tolerance_data/tool_tolerance.csv')
    # print(len(data))
    dent_df = filter_data(data, 'ILI_Anomaly Type', 'Dent')
    metalloss_df = data[data['ILI_Anomaly Type'] != 'Dent']
    metalloss_df = metalloss_df[metalloss_df['F_Metal Loss Depth (%)'].notnull()]

    metalloss_df['F_Measured Metal Loss Depth (in)'] = metalloss_df['F_Metal Loss Depth (%)']*metalloss_df['F_Wall Thickness (in)']/100
    metalloss_df['ML Diff ILI_Depth - F_Depth'] = metalloss_df['ILI_Metal Loss Depth (%)'] - metalloss_df['F_Metal Loss Depth (%)']

    metalloss_df['Wall Thickness Measurement Error (in)'] = wallthickness_measurement_error_in
    metalloss_df['Metal Loss Measurement Error (in)'] = metalloss_measurement_error_in_ml

    metalloss_df['Total Metal Loss Depth Error (in)'] = metalloss_df.apply(
        lambda row:
        combined_measurement_error(
            row['Wall Thickness Measurement Error (in)'],
            row['Metal Loss Measurement Error (in)']),
        axis=1)
    
    metalloss_df['Actual Measurement Tolerance_with_confidence'] = metalloss_df.apply(
        lambda row:
        measurement_tolerance_within_confidence_metalloss(
            row['Metal Loss Measurement Error (in)'],
            row['F_Measured Metal Loss Depth (in)'],
            row['Wall Thickness Measurement Error (in)'],
            row['F_Wall Thickness (in)'],
            row['F_Metal Loss Depth (%)'],
            confidence_interval),
        axis=1)

    metalloss_df['Actual Measurement WT loss with Measurement Tolerance'] = metalloss_df.apply(
        lambda row:
        measured_wt_loss_with_measured_tolerance(
            row['F_Metal Loss Depth (%)'],
            row['Actual Measurement Tolerance_with_confidence']),
        axis=1)

    metalloss_df['WT Loss Difference'] = metalloss_df.apply(
        lambda row:
        wt_loss_difference(
            row['ILI_Metal Loss Depth (%)'],
            row['F_Metal Loss Depth (%)']),
        axis=1)

    metalloss_df['Tool Tolerance'] = metalloss_df.apply(
        lambda row:
        get_tolerance(
            row['ILI_Pipe Type'],
            row['ILI_Metal Loss Class']),
        axis=1)

    metalloss_df['Measurement Error Combined Tolerance'] = metalloss_df.apply(
        lambda row:
        measurement_error_combined_tolerance(
            row['Actual Measurement Tolerance_with_confidence'],
            row['Tool Tolerance']),
        axis=1)

    metalloss_df['ML Violates Confidence Criterion Out of Tolerance'] = metalloss_df.apply(
        lambda row:
        is_violates_confidence(
            row['WT Loss Difference'],
            row['Measurement Error Combined Tolerance']),
        axis=1)
    
    ml_dataframe = st.checkbox('Show Metal loss Dataframe')
    if ml_dataframe:
        st.header('Metalloss Dataframe')
        st.write(metalloss_df)

    ml_stats = st.checkbox("Show Metal Loss Statistics")
    if ml_stats:
        statistics(metalloss_df, 'ML Diff ILI_Depth - F_Depth', 'ML Violates Confidence Criterion Out of Tolerance', 'Metal Loss')
    
    ml_unity_plot = st.checkbox('Show Metal Loss Unity Plot')
    if ml_unity_plot:
        ml_unity = unity_plot(data, 'F_Metal Loss Depth (%)', 'ILI_Metal Loss Depth (%)', 'Metal Loss')

    ml_distplot = st.checkbox('Show Metal Loss Distribution Plot')
    if ml_distplot:
        bin_size = st.slider('Bin Size', 1, 10, 1, key='ml')
        show_hist = st.checkbox("Show Histogram", key='ml')
        histnorm = st.selectbox("Histogram Normalization", ['', 'probability'], key='ml')
        distribution_plot(metalloss_df, 'ILI_Metal Loss Depth (%)', 'F_Metal Loss Depth (%)', 'Metal Loss', bin_size, histnorm, show_hist)
    
    export_ml_df = st.checkbox('Export Metal Loss Dataframe')
    if export_ml_df:
        export_data(metalloss_df, 'Calculated Metal Loss dataframe')
    
    try:
        dent_df['ILI_Dent Depth (in)'] = dent_df['ILI_Dent Depth (%)']*dent_df['ILI_Nominal Diameter (in)']/100
        dent_df['F_Measured Dent Depth  (in)'] = dent_df['F_Dent Depth (%)']*dent_df['ILI_Nominal Diameter (in)']/100
        dent_df['Dent Diff ILI_Depth - F_Depth'] = dent_df['ILI_Dent Depth (%)'] - dent_df['F_Dent Depth (%)']

        dent_df['Metal Loss Measurement Error'] = metalloss_measurement_error_in_dent
        dent_df['Actual Measurement Tolerance_with_confidence'] = dent_df.apply(
            lambda row: 
            measurement_tolerance_within_confidence(
                row['Metal Loss Measurement Error'],
                row['ILI_Nominal Diameter (in)'],
                confidence_interval), 
            axis=1)

        dent_df['Actual Measurement WT loss with Measurement Tolerance'] = dent_df.apply(
            lambda row:
            measured_wt_loss_with_measured_tolerance(
                row['F_Dent Depth (%)'],
                row['Actual Measurement Tolerance_with_confidence']),
            axis=1)

        dent_df['WT Loss Difference'] = dent_df.apply(
            lambda row:
            wt_loss_difference(
                row['ILI_Dent Depth (%)'],
                row['F_Dent Depth (%)']),
            axis=1)

        dent_df['Tool Tolerance'] = dent_df.apply(
            lambda row:
            get_tolerance(
                row['ILI_Pipe Type'],
                row['ILI_Anomaly Type']),
            axis=1)

        dent_df['Measurement Error Combined Tolerance'] = dent_df.apply(
            lambda row:
            measurement_error_combined_tolerance(
                row['Actual Measurement Tolerance_with_confidence'],
                row['Tool Tolerance']),
            axis=1)

        dent_df['Dent Violates Confidence Criterion Out of Tolerance'] = dent_df.apply(
            lambda row:
            is_violates_confidence(
                row['WT Loss Difference'],
                row['Measurement Error Combined Tolerance']),
            axis=1)

        dent_dataframe = st.checkbox('Show Dent Dataframe')
        if dent_dataframe:
            st.header('Dent Dataframe')
            st.write(dent_df)

        dent_statistics = st.checkbox('Show Dent Statistics')
        if dent_statistics:
            statistics(dent_df, 'Dent Diff ILI_Depth - F_Depth', 'Dent Violates Confidence Criterion Out of Tolerance', 'Dent')

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
            export_data(dent_df, 'Calculated Dent dataframe')


        
        export_combined_df = st.checkbox('Export Combined Dataframe')
        if export_combined_df:
            combined_df = pd.concat([dent_df, metalloss_df], ignore_index=True)
            st.write(combined_df)
            # print(len(combined_df))
            export_data(combined_df, 'Calculated Combined dataframe')
    except:
        st.write('No data to show')