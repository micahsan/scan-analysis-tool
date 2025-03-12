# Main script for controlling process

from dicom_utils import *
from output_utils import *


def main(in_directory, out_directory):
    df, figure, title = main_plot(in_directory)
    main_export(df, figure, title, out_directory)


def main_plot(in_directory):
    # Load DICOM files from the given directory
    dicom_files, title = load_dicom_files(in_directory)

    # Filter DICOM files for 'PET AC'
    filtered_files = filter_dicom_files(dicom_files)

    # Sort DICOM files by ascending slice location
    sorted_files = sorted(filtered_files, key=lambda x: x.SliceLocation)

    # Compute counts
    pixel_counts = compute_pixel_counts(sorted_files)

    # Enumerate indices
    indices = enumerate_indices(sorted_files)

    # Create Pandas DataFrame for (location, count) tuples
    col1_name = 'Location (mm)'
    col2_name = 'Counts (Bq/ml)'
    df = create_dataframe((col1_name, indices), (col2_name, pixel_counts))

    # Plot data
    figure = plot_data(df, title, col1_name, col2_name)

    return df, figure, title


def main_export(df, figure, title, out_directory):
    # Export data
    export_data(df, figure, out_directory, title)


if __name__ == '__main__':
    in_dir = input("Enter the path to the input directory: ")
    out_dir = input("Enter the path to the output directory: ")

    main(in_dir, out_dir)
