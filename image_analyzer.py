import numpy as np
import pandas as pd

def compute_pixel_counts(dicom_files):
    """Computes counts based on pixel data and rescale function"""
    sums = []

    # Rescale function (Output units = mx+b, where x is stored value)
    def rescale(file, x):
        return file.RescaleSlope * x + file.RescaleIntercept

    # Loop through the given files, rescale, and calculate sums
    for ds in dicom_files:
        pixel_array = rescale(ds, ds.pixel_array)
        sums.append(int(pixel_array.sum()))

    return sums


def enumerate_indices(files):
    """Enumerates indices over the range of slice locations"""
    return np.arange(files[0].SliceLocation,
                     files[len(files) - 1].SliceLocation + 1,
                     files[0].SliceThickness)


def create_dataframe(*args):
    """Creates Pandas DataFrame

    Args:
        *args: A variable number of tuples, where each tuple is (name, value)
    """
    df = pd.DataFrame()

    for tup in args:
        df[tup[0]] = tup[1]

    return df
