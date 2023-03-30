import os
import datetime


class FileExplorer:

    input_path = ""  # os.path.dirname(os.path.abspath(__file__)) + '\\input_xls\\'
    output_path = ""  # os.path.dirname(os.path.abspath(__file__)) + '\\output_dxf\\'
    current_path_listing = []
    selected_file_path = ""
    selected_file_name = ""
    valid_file_extensions = ['.xls']

    def __init__(self):
        self.input_path = os.getcwd() + "\\input_xls\\"
        self.output_path = os.getcwd() + "\\output_dxf\\"
        self.current_path = ""
        return

    # Lists both directories and files in given path and returns list of dictionaries with item type, name and full path
    def __list_files(self, current_path=""):
        files_list = []
        folders_list = []

        if current_path == "":
            current_path = self.input_path

        print("Current path:\n{}\n".format(current_path))

        files = os.listdir(current_path)

        for file in files:
            full_path = current_path + file
            if os.path.isdir(full_path):
                folders_list.append({'type': 'dir', 'name': file, 'path': full_path})
            elif os.path.isfile(full_path) and full_path[-4:].lower() in self.valid_file_extensions:
                files_list.append({'type': 'file', 'name': file, 'path': full_path})

        self.current_path_listing = folders_list + files_list

    # Allows user to select file from stored path listing
    def select_file(self, current_path="", previous_path=()):
        if current_path == "":
            current_path = self.input_path

        # list all the files in current_path
        self.__list_files(current_path)

        # if we are in main directory and there is no files to list then it's empty
        list_length = len(self.current_path_listing)
        if list_length == 0 and len(previous_path) == 0:
            print("Directory is empty")
            return False

        selection_range = range(0, list_length)
        valid_options = []

        print("Select file:\n")

        # if we are not in main directory we add an option to go one dir UP
        if len(previous_path) != 0:
            print("U  ..")
            valid_options.append('u')

        for i in selection_range:
            file = self.current_path_listing[i]
            index = i + 1
            valid_options.append(str(index))
            print("{:d}. {:s}".format(index, file['name']))

        # add option to terminate selection
        print("E. Exit\n")
        valid_options.append('e')

        # get user input and make sure it's a valid one
        user_selection = self.__make_selection("Select file to convert...", valid_options)

        # if user choose to terminate
        if user_selection == 'e':
            print("\nEXIT\n")
            return False
        # or go back to previous folder
        elif user_selection == 'u':
            if len(previous_path) >= 2:
                return self.select_file(previous_path[-1], previous_path[:-1])
            else:
                return self.select_file(previous_path[-1])

        # if neither E nor U was selected user must have selected an item from possible indexes
        # but let's make sure it is withing the range
        user_index = int(user_selection) - 1
        if user_index not in selection_range:
            print("Selection out of range")
            return False
        selected_file = self.current_path_listing[user_index]

        # if selected item as a directory we must list all the items in it and let user select again
        if selected_file['type'] == 'dir':
            previous_path_mutable = list(previous_path)
            previous_path_mutable.append(current_path)
            return self.select_file(selected_file['path'] + "\\", previous_path_mutable)
        # if file was selected the selection process is finished, and we can return True
        elif selected_file['type'] == 'file':
            self.selected_file_path = selected_file['path']
            self.selected_file_name = selected_file['name']
            self.__set_output_path()
            return True

        # if everything fails we return False
        return False

    # Set and create output path for DXF files
    def __set_output_path(self):
        pos = self.selected_file_name.rfind('.')
        name = self.selected_file_name[:pos]
        self.output_path = self.output_path + "{} {}\\".format(name, datetime.date.today())

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        print("\nOutput path:\n{}\n".format(self.output_path))

    # Wait for user input and make sure it is withing valid selection options
    def __make_selection(self, message, valid_options, loop=True):
        raw_input = input(message).lower()
        if raw_input in valid_options:
            return raw_input

        print("Selection out of range.")
        if loop:
            return self.__make_selection(message, valid_options, loop)

        return -1
