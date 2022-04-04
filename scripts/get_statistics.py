
import streamlit as st

def average_bias(df, col):
    return df[col].mean()

def standard_deviation(df, col):
    return df[col].std()

def conclusion_from_bias(avg):
    return 'Positive bias indicates -- ILI tool over-estimates depths on average' if avg > 0 else 'Negative bias indicates -- ILI tool under-estimates depths on average'


def statistics(df, col1, col2, string, confidence_interval):
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
