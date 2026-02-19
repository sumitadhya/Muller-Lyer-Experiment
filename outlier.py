import pandas as pd

def remove_outliers_excel(input_path, output_path, factor=1.5):
    df = pd.read_excel(input_path)
    numeric_cols = [
        'Control Error',
        'Baseline Error',
        'Length 200 Error',
        'Length 400 Error',
        'Thick 1px Error',
        'Thick 5px Error',
        'Fins 2 Error',
        'Angle 30 Error',
        'Angle 150 Error',
        'Brentano Error'
    ]
    mask = pd.Series(True, index=df.index)
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        mask &= (df[col] >= lower) & (df[col] <= upper)
    cleaned_df = df[mask]
    cleaned_df.to_excel(output_path, index=False)
    return cleaned_df