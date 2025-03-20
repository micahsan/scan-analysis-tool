from pathlib import Path


class ExportManager:
    def __init__(self, folder_path, file_name):
        self.path = Path(folder_path)
        self.file_name = file_name

    def save_csv(self, df):
        df.to_csv(f'{str(self.path)}/{self.file_name}_counts.csv', index=False)

    def save_plot(self, plt):
        plt.savefig(f'{str(self.path)}/{self.file_name}_counts.png')
