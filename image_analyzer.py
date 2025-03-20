import pandas as pd
from matplotlib import pyplot as plt

X_LABEL = 'Slice Location (mm)'
Y_LABEL = 'Counts (Bq/ml)'


class ImageAnalyzer:
    def __init__(self, image_series, folder_name):
        self.image_series = image_series
        self.folder_name = folder_name
        self.df = None

    def compute_counts(self):
        """Computes counts based on pixel data and rescale function"""
        # DICOM rescale function (Output units = mx+b, where x is stored value)
        def rescale(ds):
            return ds.RescaleSlope * ds.pixel_array + ds.RescaleIntercept

        slice_locations = [int(f.SliceLocation) for f in self.image_series]
        counts = [rescale(ds).sum() for ds in self.image_series]
        self.df = pd.DataFrame({X_LABEL: slice_locations, Y_LABEL: counts})
        return self.df

    def generate_plot(self):
        """Generates and returns a MatplotLib Figure object"""
        fig, ax = plt.subplots()
        ax.plot(self.df[X_LABEL], self.df[Y_LABEL])
        ax.set_xlabel(X_LABEL)
        ax.set_ylabel(Y_LABEL)
        ax.set_title(self.folder_name)
        return fig
