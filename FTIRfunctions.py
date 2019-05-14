"""Functions used for FTIR spectra procesing."""
import matplotlib.pyplot as plt
import numpy as np
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
    return a, b, x1, x2


def procesing_biodiesel_FTIR(alcohols, concentrations, dir_path):
    """Process FTIR data and returns the maximum of absorbance for
    the coresponding concentration of diosiesel in the wavenumber
    range of 1690-1780.
    """
    for alcohol in alcohols:
        results = []
        for concentration in concentrations:
            three_bd_abs = []
            three_bd_abs_wn = []
            for i in range(3):
                file = alcohol + '-' + concentration + '-' + str(i) + '.asc'
                path = dir_path + file
                df = openFTIR(path)

                # BASELINE - slope (a), intercept(b)
                a, b, x1, x2 = baseline(df)
                bd_abs = df.loc[(df['Wave_number'] > x1) &
                                (df['Wave_number'] < x2)
                                ]['Absorbance'].max()
                bd_abs_wn = float(df.loc[(df['Absorbance'] == bd_abs) &
                                         ((df['Wave_number'] < x2) &
                                          ((df['Wave_number'] > x1)))
                                         ]['Wave_number'].mean())

                # Corrected absorbance
                bd_abs = bd_abs - (a * bd_abs_wn + b)

                conc = float(concentration) / 100
                three_bd_abs.append(bd_abs)
                three_bd_abs_wn.append(bd_abs_wn)

            res = [alcohol, conc,
                   np.mean(three_bd_abs_wn),
                   three_bd_abs[0],
                   three_bd_abs[1],
                   three_bd_abs[2],
                   np.mean(three_bd_abs),
                   np.std(three_bd_abs)]
            results.append(res)
        df2 = pd.DataFrame(results, columns=['Alcohol', 'Concentrations',
                                          'Wave number', 'Absorption 1',
                                          'Absorption 2', 'Absorption 3',
                                          'Absorption average',
                                          'Standard deviation'])
        plt.scatter(df2['Concentrations'].values,
                        df2['Absorption average'].values,
                        s=15, c='r', alpha=0.9)
        '''plt.plot(df2['Concentrations'].values,
                     (df2['Absorption average'].values),
                     "--")'''
        plt.xlabel('Concentration, vol. %')
        plt.ylabel('Absorbance')
        plt.ylim(ymin=0)
        plt.xlim(xmin=0)
        plt.title(alcohol)
        plt.grid(False)
            #plt.savefig(folder_path +'Results/'+ alcohol + '-results.png')
        plt.show()
    return df2
