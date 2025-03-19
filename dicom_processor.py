# Utilities for dicom processing

from pathlib import Path
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
