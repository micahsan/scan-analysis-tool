# Launches GUI

import tkinter as tk
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from main import *

# Configuration Constants
WINDOW_TITLE = 'Scan Analysis Tool'
WINDOW_SIZE = '1000x800'


# Main GUI Class
class MainApplication:
    def __init__(self, root):
        # Store the root window
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        self.df = None
        self.title = None
        self.import_dir = None
        self.export_dir = None
        self.selected_import_dir_lbl = None
        self.plot_btn = None
        self.figure = None
        self.canvas = None
        self.sel_export_dir_lbl = None
        self.sel_export_dir_btn = None
        self.selected_export_dir_lbl = None
        self.export_btn = None
        self.exported_lbl = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        """Create and place all widgets"""
        # Label: select import directory
        sel_import_dir_lbl = tk.Label(
            root, text="Select the directory containing scans:")
        sel_import_dir_lbl.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        # Button: browse import directories
        sel_import_dir_btn = tk.Button(
            root, text="Open", width=5, command=self.open_import_dir)
        sel_import_dir_btn.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Label: selected import directory
        self.selected_import_dir_lbl = tk.Label(root, text='')
        self.selected_import_dir_lbl.grid(row=1, column=0, columnspan=2,
                                          sticky=tk.W,
                                          padx=5, pady=5)

        # Button: plot button
        self.plot_btn = tk.Button(
            self.root, text="Plot", width=5, command=self.plot)

        # Canvas: blank canvas
        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=1, padx=5,
                                         pady=5)
        self.canvas.draw()

        # Label: select export directory
        self.sel_export_dir_lbl = tk.Label(root, text='')

        # Button: browse export directories
        self.sel_export_dir_btn = tk.Button(
            root, text="Open", width=5, command=self.open_export_dir)

        # Label: selected export directory
        self.selected_export_dir_lbl = tk.Label(root, text='')
        self.selected_export_dir_lbl.grid(row=5, column=0, columnspan=2,
                                          sticky=tk.W,
                                          padx=5, pady=5)

        # Button: export button
        self.export_btn = tk.Button(self.root, text="Export", width=5,
                                    command=self.export)

        # Label: data exported successfully
        self.exported_lbl = tk.Label(root, text='')
        self.exported_lbl.grid(
            row=6, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

    def create_label(self, text, row, col, colspan=1):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=col, columnspan=colspan, sticky=tk.W, padx=5, pady=5)
        return label

    def create_button(self, text, row, col, command):
        button = tk.Button(self.root, text=text, command=command)
        button.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
        return button

    def open_import_dir(self):
        # Open a directory selection dialog
        self.import_dir = fd.askdirectory(initialdir="/", title="Select file")

        # Clear selected directories label and canvas
        self.selected_import_dir_lbl.config(text='')
        self.figure.clear()
        self.canvas.draw()
        self.sel_export_dir_lbl.config(text='')
        self.sel_export_dir_btn.grid_forget()
        self.plot_btn.grid_forget()
        self.selected_export_dir_lbl.config(text='')
        self.export_btn.grid_forget()
        self.exported_lbl.config(text='')

        # Check if the directory was selected
        if not self.import_dir:
            self.selected_import_dir_lbl.config(text="No directory selected")
            return

        # Check that directory contains .ima or .dcm files
        path = Path(self.import_dir)
        if not any(f.is_file() and (f.suffix.lower() == '.ima' or f.suffix.lower() == '.dcm')
                   for f in path.iterdir()):
            self.selected_import_dir_lbl.config(text="Selected directory doesn't "
                                                "contain .ima or .dcm files")
            self.plot_btn.grid_forget()
            return

        # Display selected directory
        self.selected_import_dir_lbl.config(
            text=f"You selected: {self.import_dir}")

        # Present plot button
        self.plot_btn.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

    def plot(self):
        # Retrieve plot and associated data
        self.df, self.figure, self.title = main_plot(self.import_dir)

        # Create tkinter canvas with the figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)

        # Place the canvas on the window
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Label: select export directory
        self.sel_export_dir_lbl = tk.Label(
            root, text="Select directory to export data to:")
        self.sel_export_dir_lbl.grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5)

        # Button: browse export directories
        self.sel_export_dir_btn.grid(
            row=3, column=1, sticky=tk.W, padx=5, pady=5)

    def open_export_dir(self):
        # Open a directory selection dialog
        self.export_dir = fd.askdirectory(initialdir="/", title="Select file")

        # Clear selected directory label
        self.selected_export_dir_lbl.config(text='')
        self.exported_lbl.config(text='')

        # Check if the directory was selected
        if not self.export_dir:
            self.selected_export_dir_lbl.config(text="No directory selected")
            self.export_btn.grid_forget()
            return

        # Display selected directory
        self.selected_export_dir_lbl.config(
            text=f"You selected: {self.export_dir}")

        # Present export button
        self.export_btn.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

    def export(self):
        main_export(self.df, self.figure, self.title, self.export_dir)
        self.exported_lbl.config(text='Files exported successfully')


# Main Execution Block
if __name__ == '__main__':
    # Create root window
    root = tk.Tk()

    # Create and run the application
    MainApplication(root)

    # Start main event loop
    root.mainloop()
