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
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        # TODO: this is ugly
        self.df = None
        self.title = None
        self.import_dir = None
        self.export_dir = None
        self.selected_import_dir_lbl = None
        self.canvas_widget = None
        self.plot_btn = None
        self.figure = None
        self.canvas = None
        self.sel_export_dir_lbl = None
        self.sel_export_dir_btn = None
        self.selected_export_dir_lbl = None
        self.export_btn = None
        self.exported_lbl = None

        self.create_widgets()

    def create_widgets(self):
        """Create and place all widgets"""
        sel_import_dir_lbl = self.create_label("Select Import Directory", 0, 0)
        sel_import_dir_btn = self.create_button("Open", 0, 1, self.open_import_dir)
        self.selected_import_dir_lbl = self.create_label("", 1, 0, 2)

        self.plot_btn = self.create_button("Plot", 1, 1, self.plot, hidden=True)

        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=0, columnspan=1, padx=5, pady=5)

        self.sel_export_dir_lbl = self.create_label("Select directory to export data to:", 3, 0, hidden=True)
        self.sel_export_dir_btn = self.create_button("Open", 3, 1, self.open_export_dir, hidden=True)

        self.selected_export_dir_lbl = self.create_label("", 4, 0, 2)

        self.export_btn = self.create_button("Export", 4, 1, self.export, hidden=True)

        self.exported_lbl = self.create_label("Files exported successfully", 5, 0, hidden=True)

    def create_label(self, text, row, col, colspan=1, hidden=False):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=col, columnspan=colspan, sticky=tk.W, padx=5, pady=5)
        if hidden:
            label.grid_remove()
        return label

    def create_button(self, text, row, col, command, hidden=False):
        button = tk.Button(self.root, text=text, command=command)
        button.grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
        if hidden:
            button.grid_remove()
        return button

    def open_import_dir(self):
        # Open a directory selection dialog
        self.import_dir = fd.askdirectory(initialdir="/", title="Select file")

        # Clear selected directories label and canvas
        self.selected_import_dir_lbl.config(text='')
        self.canvas.figure.clear()
        self.sel_export_dir_lbl.grid_remove()
        self.sel_export_dir_btn.grid_remove()
        self.plot_btn.grid_remove()
        self.selected_export_dir_lbl.grid_remove()
        self.export_btn.grid_remove()
        self.exported_lbl.grid_remove()

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
            self.plot_btn.grid_remove()
            return

        # Display selected directory
        self.selected_import_dir_lbl.config(
            text=f"You selected: {self.import_dir}")

        # Present plot button
        self.plot_btn.grid()

    def plot(self):
        self.df, self.figure, self.title = main_plot(self.import_dir)

        self.canvas.figure.clear()
        self.canvas.figure = self.figure
        self.canvas.draw()

        self.sel_export_dir_lbl.grid()
        self.sel_export_dir_btn.grid()

    def open_export_dir(self):
        # Open a directory selection dialog
        self.export_dir = fd.askdirectory(initialdir="/", title="Select file")

        # Clear selected directory label
        self.exported_lbl.grid_remove()

        # Check if the directory was selected
        if not self.export_dir:
            self.selected_export_dir_lbl.config(text="No directory selected")
            self.selected_export_dir_lbl.grid()
            self.export_btn.grid_remove()
            return

        # Display selected directory
        self.selected_export_dir_lbl.config(
            text=f"You selected: {self.export_dir}")
        self.selected_export_dir_lbl.grid()

        # Present export button
        self.export_btn.grid()

    def export(self):
        main_export(self.df, self.figure, self.title, self.export_dir)
        self.exported_lbl.grid()


# Main Execution Block
if __name__ == '__main__':
    # Create root window
    root = tk.Tk()

    # Create and run the application
    MainApplication(root)

    # Start main event loop
    root.mainloop()
