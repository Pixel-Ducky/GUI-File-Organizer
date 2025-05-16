import os
import shutil
from pathlib import Path
import json
import sys
import logging
#hello


logger = logging.getLogger(__name__) #This gets a named logger based on the module name where it’s called. it lets me create different logging systems for different files.
logging.basicConfig(filename='moved_files.log', encoding='utf=8',level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S %p')


class FileOrganizingYey:
    def __init__(self,path_to_downloads,file_path, file_extension ):

#find home directory dynamically
        self.home_path = Path.home()
        
        #self.path_to_json_file = Path("file_extensions.json")
        self.path_to_json_file = Path(self.resource_path("file_extensions.json"))
        self.extension_table = self.read_from_json_file()

        self.path_to_downloads = path_to_downloads
        self.file_path = file_path
        self.file_extension = file_extension



   
        

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
    


    # def select_file_extension(self, path):
    #     special_tuple = os.path.splitext(str(path)) #split path & filename from text , returns tuple(name , extension)
    #     file_extension = special_tuple[1].lower().strip() #select only the extension
    #     return file_extension

    def check_if_extension_in_json(self,file_extension, extension_table):
        if extension_table:
            if file_extension in extension_table:
                    folder_where_file_should_be_stored = extension_table[file_extension]
                    final_absolute_path =  Path(os.path.join(self.home_path, folder_where_file_should_be_stored) )
                    return final_absolute_path
            else:
                return None
        else:
             return 'sorry , there is something wrong with the JSON file'
    



    def finally_organizing(self):

        if self.path_to_downloads is None :
            print(f'sorry , make sure watchdog monitors an existing directory')

        else:
            checked_if_ext_in_json = self.check_if_extension_in_json(self.file_extension , self.extension_table)
            
            if checked_if_ext_in_json == 'sorry , there is something wrong with the JSON file':
                 #print(checked_if_ext_in_json)
                 logger.error('There is something wrong with the JSON file')

            elif checked_if_ext_in_json:                
                        try:
                             if checked_if_ext_in_json.exists():
                                 shutil.move(self.file_path ,checked_if_ext_in_json ) 
                                 path = Path(self.file_path)
                                 filename = path.name #pathlib function to get name of file from path
                                 logger.info('moved "%s" to "%s" ',filename , checked_if_ext_in_json)   
                             else:
                                 os.makedirs(checked_if_ext_in_json, exist_ok=True)
                                 #print('creating directories')
                                 logger.debug('creating directories')  
                                 shutil.move(self.file_path ,checked_if_ext_in_json )
                                 logger.info('moved "%s" to "%s" ',filename , checked_if_ext_in_json)
                        except shutil.Error  :
                                 #print(f'this file : "{self.file_path}"\n is already in the destination folder. change the name manually , we wont move it.\n') 
                                 logger.warning('this file : "%s" is already in the destination folder. change the name manually , we wont move it.\n',filename)             
            else: 
                    #print(f'{self.file_extension} is not inside json filetable')
                    logger.info('%s is not inside json filetable',self.file_extension)


         



   

