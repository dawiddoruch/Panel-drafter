import xlrd
from classes.PanelPreset import PanelPreset
from classes.Panel import Panel


class XlsReader:
    xlsx = None
    __selected_sheet_name = ""

    def __init__(self):
        return

    # Load XLS file
    def load_file(self, file_path):
        self.xlsx = xlrd.open_workbook(file_path)

        # read list of available sheets and let user select which one to use if there's more than one in the file
        sheets = self.xlsx.sheet_names()
        if len(sheets) == 1:
            self.__selected_sheet_name = sheets[0]
            print("There is only one sheet in the file: {}".format(self.__selected_sheet_name))
        else:
            self.__selected_sheet_name = self.__select_sheet(sheets)
        return True

    # Method must be explicitly called with PanelPreset parameter
    def convert_file(self, panel_preset: PanelPreset, output_path):
        if self.__selected_sheet_name == "":
            return False
        return self.__convert_sheet(panel_preset, output_path)

    # convert selected sheet to ACM panels drawings
    def __convert_sheet(self, panel_preset: PanelPreset, output_path):
        sheet = self.xlsx.sheet_by_name(self.__selected_sheet_name)
        column_name = 0
        column_width = 1
        column_height = 2
        column_tab_t = 3
        column_tab_r = 4
        column_tab_b = 5
        column_tab_l = 6
        column_quantity = 9     # Left panels in nest
        column_angle = 15

        priority = 1
        error_rows_count = 0
        error_rows_list = []
        row_number = 0

        # iterate all rows in open sheet
        for row in range(1, sheet.nrows):
            panel = Panel(panel_preset)
            row_number += 1

            # Try to read panel data from spreadsheet
            try:
                panel.name = str(sheet.cell_value(row, column_name))
                panel.width = float(sheet.cell_value(row, column_width))
                panel.height = float(sheet.cell_value(row, column_height))
                panel.quantity = int(sheet.cell_value(row, column_quantity))
                panel.priority = priority
                if str(sheet.cell_value(row, column_tab_t)).lower() != "":
                    panel.tab_t = float(sheet.cell_value(row, column_tab_t))
                if str(sheet.cell_value(row, column_tab_r)).lower() != "":
                    panel.tab_r = float(sheet.cell_value(row, column_tab_r))
                if str(sheet.cell_value(row, column_tab_b)).lower() != "":
                    panel.tab_b = float(sheet.cell_value(row, column_tab_b))
                if str(sheet.cell_value(row, column_tab_l)).lower() != "":
                    panel.tab_l = float(sheet.cell_value(row, column_tab_l))
                if str(sheet.cell_value(row, column_angle)).lower() != "":
                    panel.angle = float(sheet.cell_value(row, column_angle))
                priority += 1
            except (ValueError, IndexError) as e:
                if panel.name != "":
                    error_rows_list.append(row_number)

            # Only draft if qtty is non-zero
            if panel.quantity > 0:
                panel.draft(output_path)

        if len(error_rows_list) != 0:
            print("Could not read values from rows:")
            print(error_rows_count)

        return True

    # Let user select which sheet to convert
    def __select_sheet(self, sheets, loop=True):
        print("Select sheet to convert:\n")
        selection_range = range(0, len(sheets))

        for i in selection_range:
            print("{:d}. {:s}".format(i+1, sheets[i]))

        print("E. Exit\n")

        raw_input = input("Select sheet...").lower()

        if raw_input == 'e':
            print("Exit")
            exit()

        int_input = int(raw_input) - 1
        if int_input in selection_range:
            return sheets[int_input]
        else:
            print("Selection out of range.\n")
            if loop:
                return self.select_sheet(sheets, loop)
            else:
                exit()
