# import calculations as calc
import components as comp
from scripts import calculations as calc

def ml_operations(metalloss_df, wallthickness_measurement_error_in, metalloss_measurement_error_in_ml, confidence_interval):
    metalloss_df['F_Measured Metal Loss Depth (in)'] = metalloss_df['F_Metal Loss Depth (%)']*metalloss_df['F_Wall Thickness (in)']/100
    metalloss_df['ML Diff ILI_Depth - F_Depth'] = metalloss_df['ILI_Metal Loss Depth (%)'] - metalloss_df['F_Metal Loss Depth (%)']

    metalloss_df['Wall Thickness Measurement Error (in)'] = wallthickness_measurement_error_in
    metalloss_df['Metal Loss Measurement Error (in)'] = metalloss_measurement_error_in_ml

    metalloss_df['Total Metal Loss Depth Error (in)'] = metalloss_df.apply(
        lambda row:
        calc.combined_measurement_error(
            row['Wall Thickness Measurement Error (in)'],
            row['Metal Loss Measurement Error (in)']),
        axis=1)

    metalloss_df['Actual Measurement Tolerance_with_confidence'] = metalloss_df.apply(
        lambda row:
        calc.measurement_tolerance_within_confidence_metalloss(
            row['Metal Loss Measurement Error (in)'],
            row['F_Measured Metal Loss Depth (in)'],
            row['Wall Thickness Measurement Error (in)'],
            row['F_Wall Thickness (in)'],
            row['F_Metal Loss Depth (%)'],
            confidence_interval),
        axis=1)

    metalloss_df['Actual Measurement WT loss with Measurement Tolerance'] = metalloss_df.apply(
        lambda row:
        calc.measured_wt_loss_with_measured_tolerance(
            row['F_Metal Loss Depth (%)'],
            row['Actual Measurement Tolerance_with_confidence']),
        axis=1)

    metalloss_df['WT Loss Difference'] = metalloss_df.apply(
        lambda row:
        calc.wt_loss_difference(
            row['ILI_Metal Loss Depth (%)'],
            row['F_Metal Loss Depth (%)']),
        axis=1)

    metalloss_df['Tool Tolerance'] = metalloss_df.apply(
        lambda row:
        calc.get_tolerance(
            row['ILI_Pipe Type'],
            row['ILI_Metal Loss Class']),
        axis=1)

    metalloss_df['Measurement Error Combined Tolerance'] = metalloss_df.apply(
        lambda row:
        calc.measurement_error_combined_tolerance(
            row['Actual Measurement Tolerance_with_confidence'],
            row['Tool Tolerance']),
        axis=1)

    metalloss_df['ML Violates Confidence Criterion Out of Tolerance'] = metalloss_df.apply(
        lambda row:
        calc.is_violates_confidence(
            row['WT Loss Difference'],
            row['Measurement Error Combined Tolerance']),
        axis=1)

    return metalloss_df

def dent_operations(dent_df, metalloss_measurement_error_in_dent, confidence_interval):
    dent_df['ILI_Dent Depth (in)'] = dent_df['ILI_Dent Depth (%)']*dent_df['ILI_Nominal Diameter (in)']/100
    dent_df['F_Measured Dent Depth  (in)'] = dent_df['F_Dent Depth (%)']*dent_df['ILI_Nominal Diameter (in)']/100
    dent_df['Dent Diff ILI_Depth - F_Depth'] = dent_df['ILI_Dent Depth (%)'] - dent_df['F_Dent Depth (%)']

    dent_df['Metal Loss Measurement Error'] = metalloss_measurement_error_in_dent
    dent_df['Actual Measurement Tolerance_with_confidence'] = dent_df.apply(
        lambda row: 
        calc.measurement_tolerance_within_confidence(
            row['Metal Loss Measurement Error'],
            row['ILI_Nominal Diameter (in)'],
            confidence_interval), 
        axis=1)

    dent_df['Actual Measurement WT loss with Measurement Tolerance'] = dent_df.apply(
        lambda row:
        calc.measured_wt_loss_with_measured_tolerance(
            row['F_Dent Depth (%)'],
            row['Actual Measurement Tolerance_with_confidence']),
        axis=1)

    dent_df['WT Loss Difference'] = dent_df.apply(
        lambda row:
        calc.wt_loss_difference(
            row['ILI_Dent Depth (%)'],
            row['F_Dent Depth (%)']),
        axis=1)

    dent_df['Tool Tolerance'] = dent_df.apply(
        lambda row:
        calc.get_tolerance(
            row['ILI_Pipe Type'],
            row['ILI_Anomaly Type']),
        axis=1)

    dent_df['Measurement Error Combined Tolerance'] = dent_df.apply(
        lambda row:
        calc.measurement_error_combined_tolerance(
            row['Actual Measurement Tolerance_with_confidence'],
            row['Tool Tolerance']),
        axis=1)

    dent_df['Dent Violates Confidence Criterion Out of Tolerance'] = dent_df.apply(
        lambda row:
        calc.is_violates_confidence(
            row['WT Loss Difference'],
            row['Measurement Error Combined Tolerance']),
        axis=1)

    return dent_df