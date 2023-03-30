import xlrd
from classes.AcmPreset import AcmPreset
from classes.AcmPanel import AcmPanel


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

    # Method must be explicitly called with AcmPreset parameter
    def convert_file(self, acm_preset: AcmPreset, output_path):
        if self.__selected_sheet_name == "":
            return False
        return self.__convert_sheet(acm_preset, output_path)

    # convert selected sheet to ACM panels drawings
    def __convert_sheet(self, acm_preset: AcmPreset, output_path):
        sheet = self.xlsx.sheet_by_name(self.__selected_sheet_name)
        column_name = 0
        column_width = 1
        column_height = 2
        column_is_corner = 3
        column_corner_width = 4
        column_corner_type = 5
        column_quantity = 11

        # iterate all rows in open sheet
        for row in range(1, sheet.nrows):
            panel = AcmPanel(acm_preset)

            # try to read ACM data from XLS
            try:
                panel.name = str(sheet.cell_value(row, column_name))
                panel.width = float(sheet.cell_value(row, column_width))
                panel.height = float(sheet.cell_value(row, column_height))
                panel.quantity = int(sheet.cell_value(row, column_quantity))
                if str(sheet.cell_value(row, column_is_corner)).lower() in ('yes', 'y', '1'):
                    panel.is_corner = True
                    panel.corner_width = float(sheet.cell_value(row, column_corner_width))
                    if str(sheet.cell_value(row, column_corner_type)).lower() in ('v', 'b'):
                        panel.corner_type = 'v'
                    else:
                        panel.corner_type = 'h'
            except ValueError:
                continue

            panel.draft(output_path)

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
