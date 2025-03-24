from pathlib import Path

from pydicom import dcmread
from pydicom.errors import InvalidDicomError

SERIES_DESCRIPTION = 'PET AC'
VALID_EXTENSIONS = {'.ima', '.dcm'}


class DICOMProcessor:
    def __init__(self, folder_path):
        self.path = Path(folder_path)
        self.folder_name = str(self.path.parts[-1])
        self.dicom_files = []
        self.dataset_series = []

    def load_dicom_files(self):
        """Loads all DICOM files in the given folder"""
        self.dicom_files = [f for f in self.path.iterdir() if f.is_file()
                            and f.suffix.lower() in VALID_EXTENSIONS]
        return len(self.dicom_files) > 0

    def extract_images(self):
        """Gets list of pydicom datasets"""
        try:
            self.dataset_series = [dcmread(str(f)) for f in self.dicom_files]
        except InvalidDicomError or TypeError:
            return False
        return len(self.dataset_series) > 0

    def filter_images(self):
        """Filters for 'PET AC' as series description (0008,103E) and sorts"""
        self.dataset_series = [ds for ds in self.dataset_series if
                               ds.SeriesDescription == SERIES_DESCRIPTION]
        self.dataset_series.sort(key=lambda ds: ds.SliceLocation)
        return len(self.dataset_series) > 0
