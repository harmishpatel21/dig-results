import os
import pandas as pd
import numpy as np
import streamlit as st
import scipy.stats as stats
import math
import plotly.graph_objects as go
import plotly.figure_factory as ff

def read_data(path):
    data = pd.read_csv(path)
    return data

def export_data(df):
    path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # filename = f'{path}/{str(uploaded_file["name"].split(".")[0])}_export.csv'
    filename = f'{path}/abc_export.csv'
    df.to_csv(filename, index=False)
    return None

def export_plot(fig, string):
    path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filename = f'{path}/{string}.jpeg'
    print('ahia ayu')
    # st.plotly_chart(fig)
    # fig.to_image(format='jpeg')
    # fig.write_image()
    # fig.write_image('filename')
    return None

def get_inputs(string):
    user_input = st.text_input(string)
    return float(user_input)

vendor_dent_tolerance_erw = get_inputs("Vendor dent tolerance for ERW")
vendor_dent_tolerance_smls = get_inputs("Vendor dent tolerance for SMLS")

metal_loss_tolerance_erw = get_inputs("Metal loss tolerance for ERW")
metal_loss_tolerance_smls = get_inputs("Metal loss tolerance for SMLS")

wallthickness_measurement_error_in = get_inputs("Wallthickness measurement error in")
metalloss_measurement_error_in_dent = get_inputs("Metalloss measurement error in Dent")
metalloss_measurement_error_in_metal = get_inputs("Metalloss measurement error in Metal Loss")

confidence_interval = get_inputs("Confidence interval")

def wt_measurement_error(x):
    return wallthickness_measurement_error_in if x != 'Dent' else None

def ml_measurement_error(x):
    return metalloss_measurement_error_in_dent if x == 'Dent' else metalloss_measurement_error_in_metal

def combined_measurement_error(wt_error, ml_error, C):
    if 'Dent' in C:
        return None
    else:
        return round(np.sqrt(wt_error**2 + ml_error**2),6)

def z_value(confidence_interval, n_sided=2):
    return stats.norm.ppf(1-(1-confidence_interval/100)/n_sided)

def measurement_tolerance_within_confidence(T, S, L, K, M, O, C, confidence_interval):
    if 'Dent' in C:
        return T*z_value(confidence_interval)/O*100
    else:
        return z_value(confidence_interval)*math.sqrt((T/L)**2 + (S/K)**2)*M

def measured_wt_loss_with_measurement_tolerance(M, P, V, C):
    if 'Dent' in C:
        return P+V
    else:
        return M+V

def wt_loss_difference(F, M, I, P, C):
    if 'Dent' in C:
        return abs(I-P)
    else:
        return abs(F-M)

def measurement_error_combined_tolerance(V, C, metal_loss_tolerance_erw=metal_loss_tolerance_erw, vendor_dent_tolerance_erw=vendor_dent_tolerance_erw):
    if 'Dent' in C:
        return np.sqrt(vendor_dent_tolerance_erw**2 + V**2)
    else:
        return np.sqrt(metal_loss_tolerance_erw**2 + V**2)

def is_violates_confidence(X, Y, C, string):
    if string in C:
        if X > Y:
            return 'Yes'
        else:
            return 'No'

def clean_data(df):
    for i in df.columns:
        if '%' in i:
            df[i] = df[i].apply(lambda x: int(str(x).replace('%', '')) if '%' in str(x) else x)
    return df

def operations(df1):  
    df1['ILI_Dent Depth (in)'] = df1['ILI_Dent Depth (%)']*df1['ILI_Nominal Diameter (in)']/100        
    
    df1['F_Measured Metal Loss Depth (in)'] = df1['F_Metal Loss Depth (%)']*df1['F_Wall Thickness (in)']/100
    
    df1['F_Measured Dent Depth (in)'] = df1['F_Dent Depth (%)']*df1['ILI_Nominal Diameter (in)']/100

    df1['ML Diff ILI_Depth - F_Depth'] = df1['ILI_Metal Loss Depth (%)'] - df1['F_Metal Loss Depth (%)']
    
    df1['Dent Diff ILI_Depth - F_Depth'] = df1['ILI_Dent Depth (%)'] - df1['F_Dent Depth (%)']

    df1['Wall Thickness Measurement Error (in)'] = df1['ILI_Anomaly Type'].apply(wt_measurement_error)
    df1['Metal Loss Measurement Error (in)'] = df1['ILI_Anomaly Type'].apply(ml_measurement_error)

    df1['Total Metal Loss Depth Error (in)'] = df1.apply(lambda x: 
                                                combined_measurement_error(
                                                    x['Wall Thickness Measurement Error (in)'], 
                                                    x['Metal Loss Measurement Error (in)'], 
                                                    x['ILI_Anomaly Type']), axis=1)

    df1['Actual Measurement Tolerance_with_confidence'] = df1.apply(lambda x: 
                                                            measurement_tolerance_within_confidence(
                                                                x['Metal Loss Measurement Error (in)'],
                                                                x['Wall Thickness Measurement Error (in)'],
                                                                x['F_Measured Metal Loss Depth (in)'],
                                                                x['F_Wall Thickness (in)'],
                                                                x['F_Metal Loss Depth (%)'],
                                                                x['ILI_Nominal Diameter (in)'],
                                                                x['ILI_Anomaly Type'], 
                                                                confidence_interval), axis=1)

    df1['Actual Measurement WT loss with Measurement Tolerance'] = df1.apply(lambda x:
                                                                            measured_wt_loss_with_measurement_tolerance(
                                                                                x['F_Metal Loss Depth (%)'],
                                                                                x['F_Dent Depth (%)'],
                                                                                x['Actual Measurement Tolerance_with_confidence'],
                                                                                x['ILI_Anomaly Type']
                                                                            ), axis=1)

    df1['WT Loss Difference'] = df1.apply(lambda x:
                                        wt_loss_difference(
                                            x['ILI_Metal Loss Depth (%)'],
                                            x['F_Metal Loss Depth (%)'],
                                            x['ILI_Dent Depth (%)'],
                                            x['F_Dent Depth (%)'],
                                            x['ILI_Anomaly Type']
                                        ), axis=1)

    df1['Measurement Error Combined Tolerance'] = df1.apply(lambda x:
                                                            measurement_error_combined_tolerance(
                                                                x['Actual Measurement Tolerance_with_confidence'],
                                                                x['ILI_Anomaly Type']
                                                            ), axis=1)

    df1['ML Violates Confidence Criterion Out of Tolerance'] = df1.apply(lambda x:
                                                                    is_violates_confidence(
                                                                        x['WT Loss Difference'],
                                                                        x['Measurement Error Combined Tolerance'],
                                                                        x['ILI_Anomaly Type'],
                                                                        'Ext ML'
                                                                    ), axis=1)

    df1['Dent Violates Confidence Criterion Out of Tolerance'] = df1.apply(lambda x:
                                                                    is_violates_confidence(
                                                                        x['WT Loss Difference'],
                                                                        x['Measurement Error Combined Tolerance'],
                                                                        x['ILI_Anomaly Type'],
                                                                        'Dent'
                                                                    ), axis=1)
    return df1

def average_bias(df, column):
    return df[column].mean()

def standard_deviation(df, column):
    return df[column].std()

def conclusion_from_bias(avg):
    if avg > 0:
        return 'Positive bias indicates -- ILI tool over-estimates depths on average'
    else:
        return 'Negative bias indicates -- ILI tool under-estimates depths on average'

def statstics(df, col1, col2, string):
    st.header(f'Adjusted Tool Tolerance - {string}')
    # st.subheader('Average Bias')
    avg_bias = average_bias(df, col1).round(2)
    avg_bias_string = f'{avg_bias:.2f}'
    bias_conclusion = conclusion_from_bias(avg_bias)
    std = standard_deviation(df, col1).round(2)
    std_string = f'Standard Deviation: **{std}%**'
    outlier = (std/100)*2.5 if std/100 > 0.1 else (std/100)*3
    outlier_string = f'Outliers: ± **{outlier.round(2)}**'
    sample_size = df[col1].count()
    sample_size_string = f'Sample Size: **{sample_size}** # Number of features with completed evaluations'
    data_comparison = len(df[df[col2] == 'No'])
    st.markdown(sample_size_string)
    st.markdown(f'**{data_comparison}** of **{sample_size}** features are within the vendor stated **{confidence_interval}%** confidence interval')
    st.markdown(f'**{avg_bias_string}%** for each depth measurement in the tool; **{bias_conclusion}**')
    st.markdown(f'{std_string} & {outlier_string}')
    return None

def unity_plot(df, col1, col2, string, col3 = 'Metal Loss Class'):
    fig = go.Figure()

    if string == "Metal Loss":
        range_x = np.arange(0, 91, 1)
        range_y = np.arange(10, 91, 1)
        range_mid = np.arange(0, 91, 1)
        tick0 = 10
        dtick = 10
        u_metalloss_classes = np.unique(df[col3].values)
        d = dict(zip(u_metalloss_classes, np.arange(len(u_metalloss_classes))))
        for i in df[col3].unique():
            fig.add_trace(go.Scatter(
                x=df[df[col3] == i][col1],
                y=df[df[col3] == i][col2],
                mode='markers',
                marker=dict(
                    color=d[i],
                    # line=dict(width=1, color='rgb(0, 0, 0)'),
                    opacity=0.8
                ),
                name=i
            ))
    else:
        range_x = np.arange(0, 11, 1)
        range_y = np.arange(1, 11, 1)
        range_mid = np.arange(0, 11, 1)
        tick0 = 1
        dtick = 1
        fig.add_trace(go.Scatter(
                x=df[col1],
                y=df[col2],
                mode='markers',
                name='Dent'
        ))

    fig.add_trace(
        go.Scatter(
            x = range_mid,
            y = range_mid,
            mode = 'lines',
            line = dict(color='black', width=1),
            opacity = 0.5,
            name = 'Unity Line'
        )
    )

    fig.add_trace(
        go.Scatter(
            y = range_y,
            x = range_x,
            mode = 'lines',
            line = dict(color='green', width=1),
            name = '± 10%'
        )
    )
    fig.add_trace(
        go.Scatter(
            y = range_x,
            x = range_y,
            mode = 'lines',
            line = dict(color='green', width=1),
            showlegend=False
        )
    )
    
    fig.update_layout(
        title=f'Unity Plot - {string}',
        xaxis_title= col1,
        yaxis_title= col2,
        width=900,
        height=700,
        xaxis = dict(
            tick0 = tick0,
            dtick = dtick
        ),
        yaxis = dict(
            tick0 = tick0,
            dtick = dtick
        )
    )
    st.plotly_chart(fig)
    return fig

def distplot_plot(df, col1, col2, string, bins, histnorm, show_hist=True, col3 = 'Metal Loss Class'):
    x1 = df[col1]
    x2 = df[col2]
    hist_data = [x1, x2]
    group_labels = [col1, col2]
    # ILI_mean = np.mean(df[col1])
    # ILI_std_plus = ILI_mean + np.std(df[col1])
    # ILI_std_minus = ILI_mean - np.std(df[col1])
    # print(ILI_mean, ILI_std_plus, ILI_std_minus)
    # F_mean = np.mean(df[col2])
    # F_std_plus = F_mean + np.std(df[col2])
    # F_std_minus = F_mean - np.std(df[col2])
    fig = ff.create_distplot(
        hist_data,
        group_labels,
        curve_type='normal',
        bin_size=bins,
        show_rug=False,
        show_hist=show_hist,
        histnorm=histnorm,
    )
    # fig.add_shape(type="line",x0=ILI_mean, x1=ILI_mean, y0 =0, y1=0.4 , xref='x', yref='y',
    #            line = dict(color = '#175f9a', dash = 'dash'), name='ILI Mean')
    # fig.add_shape(type="line",x0=F_mean, x1=F_mean, y0 =0, y1=0.4 , xref='x', yref='y',
    #            line = dict(color = '#975326', dash = 'dash'), name='Field Measured Mean')
    # fig.add_shape(type="line",x0=ILI_std_plus, x1=ILI_std_plus, y0 =0, y1=0.4 , xref='x', yref='y',
    #            line = dict(color = '#7ab7ea', dash = 'dash'))
    # fig.add_shape(type="line",x0=ILI_std_minus, x1=ILI_std_minus, y0 =0, y1=0.4 , xref='x', yref='y',
    #            line = dict(color = '#7ab7ea', dash = 'dash'))
    # fig.add_shape(type="line",x0=F_std_plus, x1=F_std_plus, y0 =0, y1=0.4 , xref='x', yref='y',
    #            line = dict(color = '#e39f73', dash = 'dash'))
    # fig.add_shape(type="line",x0=F_std_minus, x1=F_std_minus, y0 =0, y1=0.4 , xref='x', yref='y',
    #            line = dict(color = '#e39f73', dash = 'dash'))

    fig.update_layout(
        title = f'{string} Distribution Plot',
        xaxis_title = f'{string} Depth (%)',
        yaxis_title = f'{histnorm}',
        width=900,
        height=700,
        xaxis = dict(
            tick0 = 0,
            dtick = bins
        ),
        bargap = 0.01,
        showlegend=True
    )
    st.plotly_chart(fig)
    return None

uploaded_file = st.file_uploader("Upload your file", type=["csv"])

if uploaded_file is not None:
    data = read_data(uploaded_file)
    tool_tolerance_data =  read_data('tool_tolerance_data/tool_tolerance.csv')



    # data = data[data['F_Metal Loss Depth (%)'].notnull()]
    data = clean_data(data)                                     
    data = operations(data)
    st.dataframe(data)

    
    export_dataframe = st.checkbox('Export Dataframe')
    if export_dataframe:
        export_data(data)

    ml_stats = st.checkbox("Show Metal Loss Statistics")
    if ml_stats:
        statstics(data, 'ML Diff ILI_Depth - F_Depth', 'ML Violates Confidence Criterion Out of Tolerance', 'Metal Loss')
    
    ml_unity = st.checkbox("Show Metal Loss Unity Plot")
    if ml_unity:
        unity_fig = unity_plot(data, 'F_Metal Loss Depth (%)', 'ILI_Metal Loss Depth (%)', 'Metal Loss')
    
    # export_unity_plot = st.checkbox("Export Metal Loss Unity Plot")
    # if export_unity_plot:
    #     export_plot(unity_fig, 'Metal Loss Unity Plot')

    ml_histogram = st.checkbox("Show Metal Loss Histogram")
    if ml_histogram:
        bin_size = st.slider('Bin Size', 1, 10, 1, key='ml')
        show_hist = st.checkbox("Show Histogram")
        histnorm = st.selectbox("Histogram Normalization", ['', 'probability'])
        # histogram_plot(data, 'ILI_Metal Loss Depth (%)', 'F_Metal Loss Depth (%)', 'Metal Loss')
        distplot_plot(data, 'ILI_Metal Loss Depth (%)', 'F_Metal Loss Depth (%)', 'Metal Loss', bin_size, histnorm, show_hist)

    dent_stats = st.checkbox("Show Dent Statistics")
    if dent_stats:
        statstics(data, 'Dent Diff ILI_Depth - F_Depth', 'Dent Violates Confidence Criterion Out of Tolerance', 'Dent')

    dent_unity = st.checkbox("Show Dent Unity Plot")
    if dent_unity:
        unity_plot(data, 'F_Dent Depth (%)', 'ILI_Dent Depth (%)', 'Dent')
