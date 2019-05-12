"""Functions used for FTIR spectra procesing."""
import pandas as pd


def openFTIR(path):
    """Opening ASCII to a DataFrame: columns Wave_number and Absorbance."""
    with open(path) as f:
        lines = f.readlines()[56:-2]
        spectra = []
        for line in lines:
            splited_line = line.split('\t')
            splited_line = int(float(splited_line[0])), float(splited_line[1])
            spectra.append(splited_line)
        return pd.DataFrame(spectra, columns=['Wave_number', 'Absorbance'])


def baseline(df):
    """Linear baseline parameters for a wavenumber range (x1-x2)."""
    x1 = 1690
    x2 = 1780
    y1 = float(df.loc[(df['Wave_number'] == x1)]['Absorbance'])
    y2 = float(df.loc[(df['Wave_number'] == x2)]['Absorbance'])
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return [a, b]
