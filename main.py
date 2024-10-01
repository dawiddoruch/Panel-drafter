from classes.PanelPreset import PanelPreset
from classes.FileExplorer import FileExplorer
from classes.XlsReader import XlsReader
from classes.Panel import Panel

DEBUG_DEFAULT_PRESET = 5
DEBUG_DEFAULT_FILE = 4


def main():
    panel_preset = PanelPreset()
    panel_preset.select_preset()
    file_explorer = FileExplorer()
    if not file_explorer.select_file():
        print("No file was selected\n")
        return 1

    print("Selected file:\n{}\n".format(file_explorer.selected_file_path))

    xls_reader = XlsReader()
    xls_reader.load_file(file_explorer.selected_file_path)
    xls_reader.convert_file(panel_preset, file_explorer.output_path)


def test():
    acm_preset = PanelPreset()
    panel = Panel(acm_preset)
    panel.name = "TEST"
    panel.width = 120
    panel.height = 20
    panel.quantity = 1

    panel.tab_t = 0
    panel.tab_r = 4
    panel.tab_b = 0
    panel.tab_l = 6

    panel.draft("D:\\Python Projects\\ACM Drafter\\output_dxf\\")


if __name__ == '__main__':
    main()
    # test()
