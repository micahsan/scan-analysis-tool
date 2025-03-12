# Utilities for plotting and exporting

from matplotlib import pyplot as plt
from pathlib import Path


def plot_data(df, title, x_label, y_label):
    """Plots the computed values"""
    figure = plt.figure()
    plot = figure.add_subplot()
    plot.plot(df[x_label], df[y_label])
    plot.set_title(title)
    plot.set_xlabel(x_label)
    plot.set_ylabel(y_label)

    return figure


def export_data(df, figure, folder_path, title):
    """Exports the data to a csv file at the specified location"""
    path = Path(folder_path)

    if not path.is_dir():
        print('Output folder does not exist')
        return

    # Save .csv of data
    df.to_csv(str(path) + '/' + title + '_counts.csv')

    # Save .png of plot
    figure.savefig(str(path) + '/' + title + '_counts.png')
