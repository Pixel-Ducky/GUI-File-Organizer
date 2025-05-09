import os
import shutil
from pathlib import Path
import json
import sys


class FileOrganizingYey:
    def __init__(self,file_path ):

#find home directory dynamically
        self.home_path = Path.home()
        
        #self.path_to_json_file = Path("file_extensions.json")
        self.path_to_json_file = Path(self.resource_path("file_extensions.json"))
        self.extension_table = self.read_from_json_file()
        self.found_path = file_path


    #search for a Folder on my system , mixed_files will be replaced by pyqt6 folder search
    #if it dosent find a folder it will return None by default , no need to type it.

    #----------------------------------------------------------------------------------------
    #THIS CODE WILL BE USELESS IF PYQT6 GETS THE FULL PATH FOR US
    #def search_for_folder(self):
       # for path in self.home_path.rglob("mixed_files") :
            #if path.is_dir():
                #found_path = path
                #return found_path
    #----------------------------------------------------------------------------------------
        

    def resource_path(self,relative_path):
         try:
             # If running as .exe, use _MEIPASS to access the bundled resource
             base_path = sys._MEIPASS
         except Exception:
             # Otherwise, use the current directory (when running as script)
             base_path = os.path.dirname(os.path.abspath(__file__))
            
         return os.path.join(base_path, relative_path)




    def read_from_json_file(self):
        if self.path_to_json_file.exists():
            read_back = self.path_to_json_file.read_text()
            data = json.loads(read_back)
            return data
        else:
            return None
    


    def select_file_extension(self, path):
        special_tuple = os.path.splitext(str(path)) #split path & filename from text , returns tuple(name , extension)
        file_extension = special_tuple[1].lower().strip() #select only the extension
        return file_extension

    def check_if_extension_in_json(self,file_extension, extension_table):
        
        if file_extension in extension_table:
                folder_where_file_should_be_stored = extension_table[file_extension]
                final_absolute_path =  Path(os.path.join(self.home_path, folder_where_file_should_be_stored) )
                return final_absolute_path
        else:
            return None
    



    def finally_organizing(self):

        if self.found_path is None :
            print(f'sorry , we havent found any Folder with that name')

        else:
            for file in os.listdir(self.found_path): #list contents of Folder
                filepath_for_file_in_Folder = Path(os.path.join(self.found_path, file) ) #construct absolute filepath for all contents

                if filepath_for_file_in_Folder.is_file(): # check if content is a file
                    file_extension = self.select_file_extension(filepath_for_file_in_Folder)
                    checked = self.check_if_extension_in_json(file_extension , self.extension_table)

                    if checked:                
                        try:
                            if checked.exists():
                                shutil.move(filepath_for_file_in_Folder ,checked )    
                            else:
                                os.makedirs(checked, exist_ok=True)
                                print('creating directories')
                        except shutil.Error  :
                                print(f'this file "{file}" is already in the destination folder.\n change the name manually , we wont move it.\n')              
                    else: 
                        print(f'{file_extension} is not inside json filetable')




   

