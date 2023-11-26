import matplotlib
import matplotlib.axes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas.core.frame
from matplotlib.patches import Rectangle

'''
:param k: valore asse x
:param val:
:param delimiter: delimitatore nel file csv che deve essere usato quando venhono passati i parametri
:param file_name: file csv contenente i dati
:return: axes.Axes
'''


def get_histo_2d_axes(k: str,
                      val: str,
                      delimiter: str = ';',
                      file_name: str = '../../../utilities/actual_result.csv') -> matplotlib.axes.Axes:

    headers = val.split(delimiter)
    headers.append(k)
    df = pd.read_csv(file_name, usecols=headers, sep=delimiter)
    df: pandas.core.frame.DataFrame = df.groupby(k.split(delimiter)).sum().reset_index()
     #print(df)
    ax = df.plot(kind='bar', x=k)
    ax.tick_params(axis='x', labelrotation=20)
    ax.plot()
    #plt.plot()
    return ax


def get_histo_3d_axes(kx: str, ky: str,
                      val: str,
                      delimiter: str = ';',
                      file_name: str = '../../../../utilities/actual_result.csv') -> matplotlib.axes.Axes:
    colors = ['darkblue', 'darkred', 'yellow', 'GREEN, BLUE, RED, BLACK']
    headers = val.split(delimiter)
    headers.append(kx)
    headers.append(ky)
    df = pd.read_csv(file_name, usecols=headers, sep=delimiter)
    df: pandas.core.frame.DataFrame = df.groupby([kx, ky]).sum().reset_index()
    #print(df)
    # Create figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Convert string labels to numerical values
    x_labels = df[kx].unique()
    y_labels = df[ky].unique()
    x_values = np.arange(len(x_labels))
    y_values = np.arange(len(y_labels))

    # Convert string labels to numerical values
    x_indices = [np.where(x_labels == label)[0][0] for label in df[kx]]
    y_indices = [np.where(y_labels == label)[0][0] for label in df[ky]]
    i = 0
    used_colors = []
    labels = []
    for v in val.split(delimiter):

        #print(v)
        ax.bar3d(x_indices, y_indices, 0, 1, 1, df[v], shade=False, alpha=0.3, edgecolor='black', color=colors[i])
        used_colors.append(colors[i])
        labels.append(v)
        i += 1

    # Set x and y axis labels
    ax.set_xticks(x_values + 0.5)
    ax.set_xticklabels(x_labels)
    ax.set_yticks(y_values + 0.5)
    ax.set_yticklabels(y_labels)

    # Set axis labels
    ax.set_xlabel(kx)
    ax.set_ylabel(ky)
    handles = [Rectangle((0, 0), 1, 1, color=c, ec="k") for c in used_colors]

    plt.legend(handles, labels)

    return ax


def get_plot_2d_axes(k: str,
                     val: str,
                     delimiter: str = ';',
                     file_name: str = '../../../utilities/actual_result.csv') -> matplotlib.axes.Axes:

    headers = val.split(delimiter)
    headers.append(k)
    df = pd.read_csv(file_name, usecols=headers, sep=delimiter)
    df: pandas.core.frame.DataFrame = df.groupby(k.split(delimiter)).sum().reset_index()
    print(df)
    ax = df.plot(x=k)
    ax.tick_params(axis='x', labelrotation=30)
    ax.plot()
    plt.plot()
    return ax
