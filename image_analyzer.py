import pandas as pd
from matplotlib import pyplot as plt

X_LABEL = 'Slice Location (mm)'
Y_LABEL = 'Counts (Bq/ml)'


class ImageAnalyzer:
    def __init__(self, image_series, folder_name):
        self.image_series = image_series
        self.folder_name = folder_name
        self.counts = []

    def compute_counts(self):
        """Computes counts based on pixel data and rescale function"""
        # DICOM rescale function (Output units = mx+b, where x is stored value)
        def rescale(ds):
            return ds.RescaleSlope * ds.pixel_array + ds.RescaleIntercept

        self.counts = [rescale(ds).sum() for ds in self.image_series]
        return self.counts

    def generate_plot(self):
        """Generates and returns a plot of the analysis"""
        slice_locations = [int(f.SliceLocation) for f in self.image_series]
        df = pd.DataFrame({X_LABEL: slice_locations, Y_LABEL: self.counts})

        plt.rcParams['figure.dpi'] = 800
        df.plot(x=X_LABEL, y=Y_LABEL, legend=False)
        plt.xlabel(X_LABEL)
        plt.ylabel(Y_LABEL)
        plt.title(self.folder_name)
        return plt
