from classes.AcmPreset import AcmPreset
from classes.FileExplorer import FileExplorer
from classes.XlsReader import XlsReader


def main():
    acm_preset = AcmPreset()
    acm_preset.select_preset()

    file_explorer = FileExplorer()
    if not file_explorer.select_file():
        print("No file was selected\n")
        return 1

    print("Selected file:\n{}\n".format(file_explorer.selected_file_path))

    xls_reader = XlsReader()
    xls_reader.load_file(file_explorer.selected_file_path)
    xls_reader.convert_file(acm_preset, file_explorer.output_path)


if __name__ == '__main__':
    main()
