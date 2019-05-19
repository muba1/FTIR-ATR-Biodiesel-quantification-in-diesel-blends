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


def baseline(df, x1, x2):
    """Linear baseline parameters for a wavenumber range (x1-x2)."""

    y1 = float(df.loc[(df['Wave_number'] == x1)]['Absorbance'])
    y2 = float(df.loc[(df['Wave_number'] == x2)]['Absorbance'])
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


def max_amplitude_FTIR(alcohol, concentrations, dir_path, plot = True,x1 = 1690,x2 = 1780):
    """Process FTIR data and returns the maximum of absorbance for
    the coresponding concentration of diosiesel in the wavenumber
    range of 1690-1780.
    """
    results = []
    for concentration in concentrations:
        three_bd_abs = []
        three_bd_abs_wn = []
        for i in range(3):
            file = alcohol + '-' + concentration + '-' + str(i) + '.asc'
            path = dir_path + file
            df = openFTIR(path)

            # BASELINE - slope (a), intercept(b)
            a, b = baseline(df, x1, x2)
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
    df2 = pd.DataFrame(
        results, columns=[
            'Alcohol', 'Concentrations','Wave number', 'Absorption 1',
            'Absorption 2', 'Absorption 3','Absorption average',
            'Standard deviation'])
    if plot:
        plt.scatter(
        df2['Concentrations'].values,
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
        # plt.savefig(folder_path +'Results/'+ alcohol + '-results.png')
        plt.show()
    return df2


def absorbance_in_range_FTIR(alcohol, concentrations, dir_path, plot=True, x1=1690, x2=1780):
    results = []
    col = []
    for concentration in concentrations:
        abs_conc = []
        for i in range(3):
            file = alcohol + '-' + concentration + '-' + str(i) + '.asc'
            path = dir_path + file
            df = openFTIR(path)
            # BASELINE - slope (a), intercept(b)
            a, b = baseline(df, x1, x2)
            ''' ispravljanje bazne linije'''
            abs_cor_list = []
            wn_list = []
            for wavenumber in df['Wave_number'].values:
                if wavenumber > x1 * 0.99 and wavenumber < x2 * 1.01:
                    abs_cor = float(
                        df.loc[df[
                                'Wave_number'
                                ].values == wavenumber][
                                    'Absorbance'
                                    ].values) - (a * wavenumber + b)
                    abs_cor_list.append(abs_cor)
                    wn_list.append(wavenumber)
            abs_conc.append(abs_cor_list)
        mean_abs = []

        for a in range(len(abs_conc[0])):
            mean_abs.append(
                np.mean([abs_conc[i][a] for i in range(len(abs_conc))]))
        if results == []:
            results.append(wn_list)
            results.append(mean_abs)
            col.append('Wavenumber')
            col.append(str(float(concentration) / 100) + '%')
        else:
            results.append(mean_abs)
            col.append(str(float(concentration)/100) + '%')
    df2 = pd.DataFrame()

    for i in range(len(col)):
            df2[col[i]] = results[i]
    if plot == True:
        for i in range(1, len(col)):
            plt.plot(df2['Wavenumber'], df2[col[i]], 'k')
        plt.xlabel('Wave number, cm-1')
        plt.ylabel('Absorbance')
        plt.title(alcohol)
        plt.grid(True)
        # plt.savefig(folder_path + 'spektri_mean_slike/' + alcohol + '-svi_spektri.png')
        plt.show()
    return df2


def integrate_FTIR(alcohol, concentrations, dir_path, plot=True, x1=1690, x2=1780):
    """Process FTIR data and returns integrated of absorbance for
    the coresponding concentration of diosiesel in the wavenumber
    range of 1690-1780.
    """

    df2 = absorbance_in_range_FTIR(alcohol, concentrations, dir_path, plot=False, x1=1690, x2=1780)
    columns = list(df2.columns.values)
    x_data = [float(str(i[:-1])) for i in columns[1:]]
    y_data = [df2[i].sum() for i in columns[1:]]
    if plot:
        plt.plot(x_data, y_data, 'k')
        plt.xlabel('Content, %')
        plt.ylabel('Absorbance area')
        plt.title(alcohol)
        plt.grid(True)
        # plt.savefig(folder_path + 'spektri_mean_slike/' + alcohol + '-svi_spektri.png')
        plt.show()
    return df2


if __name__ == '__main__':
    dir_path = 'Test_data/'
    alcohols = ['NB4']
    concentrations = ['0025', '0050', '0100', '0250', '0500', '0750',
                  '1000', '1250', '1500', '1750', '2000', '2500',
                  '3000']
    for alcohol in alcohols:
        df2 = absorbance_in_range_FTIR(alcohol, concentrations, dir_path)
    for alcohol in alcohols:
        df3 = integrate_FTIR(alcohol, concentrations, dir_path)
    for alcohol in alcohols:
        df3 = max_amplitude_FTIR(alcohol, concentrations, dir_path)