import cv2 as cv
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

X_LABEL = 'Slice Location (mm)'
Y_LABEL = 'Counts (Bq/ml)'


class ImageAnalyzer:
    def __init__(self, dataset_series, folder_name):
        self.slice_locations = [int(ds.SliceLocation) for ds in dataset_series]
        self.folder_name = folder_name
        self.images = np.array([self.rescale(ds) for ds in dataset_series])
        self.df = self.compute_counts()

        # testing
        # print(f"pixel_array type: {type(dataset_series[0].pixel_array[0,0])}")
        # np.savetxt("pixel_array.txt", dataset_series[0].pixel_array,
        #            fmt="%.1f")

        # print(f"image type: {type(self.images[0][0,0])}")
        # np.savetxt("image.txt", self.images[0], fmt="%.6f")

        # plt.imshow(dataset_series[100].pixel_array, cmap=plt.cm.gray)
        # plt.imshow(self.images[300], cmap=plt.cm.gray)
        #
        # plt.show()

    @staticmethod
    def rescale(ds):
        """DICOM rescale function (output units = mx+b, where x is stored
        value)"""
        return ds.RescaleSlope * ds.pixel_array + ds.RescaleIntercept

    def compute_counts(self):
        """Computes counts based on pixel data and rescale function"""
        counts = [img.sum() for img in self.images]
        return pd.DataFrame({X_LABEL: self.slice_locations, Y_LABEL: counts})

    def generate_plot(self):
        """Generates and returns a MatplotLib Figure object"""
        fig, ax = plt.subplots()
        ax.plot(self.df[X_LABEL], self.df[Y_LABEL])
        ax.set_xlabel(X_LABEL)
        ax.set_ylabel(Y_LABEL)
        ax.set_title(self.folder_name)
        return fig

    @staticmethod
    def segment_object(image):
        """Uses Otsu's method of thresholding to segment image"""
        th_val, th_img = cv.threshold(image, 0, 255,
                                      cv.THRESH_BINARY + cv.THRESH_OTSU)
        return th_img
