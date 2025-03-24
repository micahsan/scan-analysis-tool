import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

X_LABEL = 'Slice Location (mm)'
Y_LABEL = 'Counts (Bq/ml)'


class ImageAnalyzer:
    def __init__(self, dataset_series, folder_name):
        self.slice_locations = [int(f.SliceLocation) for f in dataset_series]
        self.folder_name = folder_name
        self.df = None

        # DICOM rescale function (Output units = mx+b, where x is stored value)
        def rescale(ds):
            return ds.RescaleSlope * ds.pixel_array + ds.RescaleIntercept

        self.images = np.array([rescale(ds) for ds in dataset_series])

    def compute_counts(self):
        """Computes counts based on pixel data and rescale function"""
        counts = [i.sum() for i in self.images]
        self.df = pd.DataFrame({X_LABEL: self.slice_locations, Y_LABEL:
                                counts})
        return self.df

    def generate_plot(self):
        """Generates and returns a MatplotLib Figure object"""
        fig, ax = plt.subplots()
        ax.plot(self.df[X_LABEL], self.df[Y_LABEL])
        ax.set_xlabel(X_LABEL)
        ax.set_ylabel(Y_LABEL)
        ax.set_title(self.folder_name)
        return fig
