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
for path in home_path.rglob("mixed_files") :
    if path.is_dir():
        found_path = path
        #print(found_path)
        break

# extensions ={
#     ".jpg" :"Pictures\\pics",
#     ".png" :"Pictures\\pics",
#     ".jpeg" :"Pictures\\pics",
#     ".gif" :"Pictures\\pics",
#     ".jfif" :"Pictures\\pics",
#     ".pdf" :"Desktop\\Books",
#     ".epub" :"Desktop\\Books",
#     ".docx" :"Documents\\Folder_Projects",
#     ".pptx" :"Documents\\Folder_Projects",
#     ".xls" :"Documents\\Folder_Projects",
#     ".txt" :"Documents\\Folder_Notepad",
#     ".mp4" :"Documents\\Folder_Video",
#     ".mp3" :"Documents\\Folder_Audio",
#     ".wav" :"Documents\\Folder_Audio",
# }


#file_name.txt




def read_from_json_file():
    if path_to_json_file.exists():
        read_back = path_to_json_file.read_text()
        data = json.loads(read_back)
        return data
    else:
        return None
    

extension_table = read_from_json_file()

for file in os.listdir(found_path): #list contents of Folder
    filepath_for_file_in_Folder = Path(os.path.join(found_path, file) ) #construct absolute filepath for all contents

    if filepath_for_file_in_Folder.is_file(): # check if content is a file
        special_tuple = os.path.splitext(str(filepath_for_file_in_Folder)) #split path & filename from text , returns tuple(name , extension)
        file_extension = special_tuple[1].lower().strip() #select only the extension

        if file_extension in extension_table:
            folder_where_file_should_be_stored = extension_table[file_extension]
            final_absolute_path =  Path(os.path.join(home_path, folder_where_file_should_be_stored) )

            try:
                if final_absolute_path.exists():
                    shutil.move(filepath_for_file_in_Folder ,final_absolute_path )
                    
                else:
                    os.makedirs(final_absolute_path, exist_ok=True)
                    print('creating directories')
            except shutil.Error  :
                    print(f'this file "{file}" is already in the destination folder.\n change the name manually , we wont move it.\n')
                
        
           
        else: 
            print(f'{file_extension} is not inside json filetable')



        
   

