import numpy as np
import scipy.stats as stats
from scripts import data_preparation as dp

tool_tolerance_data =  dp.read_data('tool_tolerance_data/tool_tolerance.csv')

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