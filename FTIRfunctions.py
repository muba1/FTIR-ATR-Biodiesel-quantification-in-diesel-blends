"""Functions used for FTIR spectra procesing."""
import pandas as pd


def open_ascii(path):
    """Opening ASCII to a DataFrame: columns Wave_number and Absorbance."""
    with open(path) as f:
        lines = f.readlines()[56:-2]
        new_lines = []
        for line in lines:
            splited_line = line.split('\t')
            splited_line[0] = int(float(splited_line[0]))
            splited_line[1] = float(splited_line[1])
            new_lines.append(splited_line)
        df = pd.DataFrame(new_lines, columns=['Wave_number', 'Absorbance'])
    return df


def baseline(df):
    """Linear baseline parameters for a wavenumber range (x1-x2)."""
    x1 = 1690
    x2 = 1780
    y1 = float(df.loc[(df['Wave_number'] == x1)]['Absorbance'])
    y2 = float(df.loc[(df['Wave_number'] == x2)]['Absorbance'])
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b
