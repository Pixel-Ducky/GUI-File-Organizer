import os
import shutil
from pathlib import Path
import json
import random
import string

#find home directory dynamically
home_path = Path.home()
path_to_json_file = Path("file_extensions.json")


#search for a Folder on my system , mixed_files will be replaced by pyqt6 folder search
def search_for_folder():#if it dosent find a folder it will return None by default , no need to type it.
    for path in home_path.rglob("mixed_files") :
        if path.is_dir():
            found_path = path
            return found_path
        


def read_from_json_file():
    if path_to_json_file.exists():
        read_back = path_to_json_file.read_text()
        data = json.loads(read_back)
        return data
    else:
        return None
    


def select_file_extension(path):
    special_tuple = os.path.splitext(str(path)) #split path & filename from text , returns tuple(name , extension)
    file_extension = special_tuple[1].lower().strip() #select only the extension
    return file_extension

def check_if_extension_in_json(file_extension, extension_table):
    
    if file_extension in extension_table:
            folder_where_file_should_be_stored = extension_table[file_extension]
            final_absolute_path =  Path(os.path.join(home_path, folder_where_file_should_be_stored) )
            return final_absolute_path
    else:
        return None
    


found_path = search_for_folder()
extension_table = read_from_json_file()

if found_path is None :
    print(f'sorry , we havent found any Folder with that name')

else:
    for file in os.listdir(found_path): #list contents of Folder
        filepath_for_file_in_Folder = Path(os.path.join(found_path, file) ) #construct absolute filepath for all contents

        if filepath_for_file_in_Folder.is_file(): # check if content is a file
            file_extension = select_file_extension(filepath_for_file_in_Folder)
            checked = check_if_extension_in_json(file_extension , extension_table)

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



        
   

