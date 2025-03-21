import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dicom_processor import DICOMProcessor
from image_analyzer import ImageAnalyzer
from export_manager import ExportManager

WINDOW_TITLE = 'Scan Analysis Tool'
WINDOW_SIZE = '700x700'


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)
        self.folder_path = ''
        self.folder_name = ''
        self.image_series = []
        self.dataframe = None
        self.processor = None
        self.analyzer = None
        self.exporter = None
        self.btn_2 = None
        self.btn_3 = None
        self.canvas = None
        self.setup_ui()

    def setup_ui(self):
        tk.Button(self.root, width=15, text="Select DICOM Folder",
                  command=self.load_dicom_files).pack(pady=5)
        self.btn_2 = tk.Button(self.root, width=15, text="Run Analysis",
                               command=self.analyze_images)
        self.btn_3 = tk.Button(self.root, width=15, text="Export Results",
                               command=self.export_results)

    def clear_ui(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.btn_2.pack_forget()
        self.btn_3.pack_forget()

    def load_dicom_files(self):
        """Prompts user for folder and loads DICOM files"""
        self.clear_ui()

        self.folder_path = fd.askdirectory()
        if not self.folder_path:
            mb.showerror('Error', "Please select a folder")
            return

        self.processor = DICOMProcessor(self.folder_path)
        if not self.processor.load_dicom_files():
            mb.showerror('Error', "No DICOM files found in the selected "
                                  "folder")
            return

        if not self.processor.extract_images():
            mb.showerror('Error', "Error reading DICOM files")
            return

        if not self.processor.filter_images():
            mb.showerror('Error', "No \'PET AC\' files "
                                  "found in the selected folder")
            return

        self.folder_name = self.processor.folder_name
        self.image_series = self.processor.image_series
        self.btn_2.pack(pady=5)

    def analyze_images(self):
        """Performs analysis on image series and displays results"""
        self.analyzer = ImageAnalyzer(self.image_series, self.folder_name)
        self.dataframe = self.analyzer.compute_counts()
        fig = self.analyzer.generate_plot()
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=30, pady=10)
        self.btn_3.pack(pady=5)

    def export_results(self):
        """Exports .PNG of plot and .CSV of DataFrame"""
        export_path = fd.askdirectory()
        if not export_path:
            mb.showerror('Error', "Please select a folder")
            return
        self.exporter = ExportManager(export_path, self.folder_name)
        self.exporter.save_csv(self.dataframe)
        self.exporter.save_plot(self.analyzer.generate_plot())
        mb.showinfo('Success', "Results exported")
        self.clear_ui()
