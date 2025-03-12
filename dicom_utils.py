# Utilities for dicom processing

from pathlib import Path
import numpy as np
import pandas as pd
from pydicom import dcmread


def load_dicom_files(folder_path):
    """Loads all DICOM files in the given directory"""
    # TODO: add check that folder isn't empty, return something else if unsuccessful
    dicom_files = []

    # Convert the folder path to a Path object
    path = Path(folder_path)

    # Check that given path is valid
    if not path.is_dir():
        print('Input folder does not exist')
        return dicom_files

    # Loop through the files in the directory
    for file in path.iterdir():
        # Check if it's both a file (not a subdirectory) and .IMA
        if file.is_file() and file.suffix == '.IMA':
            dicom_files.append(dcmread(str(file)))

    return dicom_files, str(path.parts[-1])


def filter_dicom_files(dicom_files):
    """Returns DICOM files with 'PET AC' as series description (0008,103E)"""
    return [file for file in dicom_files if file.SeriesDescription == 'PET AC']


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
