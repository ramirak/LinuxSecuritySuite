from tools.json_handler import *
import os

class Table:
    table_name = ""
    path = ""
    data = []
    
    def __init__(self, path):
        self.path = path
        self.table_name = os.path.basename(path)

    def add_row(self, keys, values):
        json = dict(zip(keys,values))
        self.data.append(json)

    def replace_row(self, keys, values, row_id):
        if(len(self.data) == 0):
            return
        try:  
            json = dict(zip(keys,values))
            self.data[row_id] = json
        except Exception as e:
            print("Failed to replace row - " + str(e))       
    
    def edit_col(self, key, val, col, new_val):
        if(len(self.data) == 0):
            return
        try:
            row, i = self.get_row_by_key_val(key,val)
            self.data[i][col] = new_val
        except Exception as e:
            print("Failed to edit column - " + str(e))

    def remove_row(self, key, val):
        if(len(self.data) == 0):
            return
        try:
            row, i = self.get_row_by_key_val(key, val)
            self.data.remove(row)
        except Exception as e:
            print("Failed to remove row - " + str(e))
    
    def remove_row_by_index(self, index): 
        if(len(self.data) == 0):
            return
        try:
            self.data.pop(index)
        except Exception as e:
            print("Failed to remove row by index - " + str(e))

    def reload_data(self):
        try:
            self.data = retrieve_from_file(self.path)
        except Exception as e:
            print("Failed to reload data - " + str(e))

    def save_data(self):
        try:
            save_to_file(self.path, self.get_data())
        except Exception as e:
            print("Failed to save data - " + str(e))
        pass

    def get_data(self):
        return self.data

    def get_name(self):
        return self.table_name

    def get_row_by_key_val(self, key, val):
        i = 0
        for row in self.data: 
            if (row[key] == val):
                return row, i
            i+=1

