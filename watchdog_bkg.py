import time 
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main_organiser import FileOrganizingYey
import os

path_to_folder_i_want_to_monitor =  os.path.join(Path.home(), 'Downloads')
bad_ext = ['.tmp', '.crdownload', '.part', '.json',  '.ini','.exe','.zip']
#here we tell python what to do if it sees changes

class MyHandler(FileSystemEventHandler):

    def is_file_stable(self, path, checks=3, delay=1.3):   #current size needs to be == to previous size , for the file to be stable
        previous_size = -1                                 #we put -1 because its impossible for a file to have -1 bytes , if we started by 0  ,and we catch a file at 0 bytes that needs to be written to , ouch.
                                                           #its gonna think its stable when in fact its not.
        for _ in range(checks): #_ means 'idk about this value'

            try:
                current_size = os.path.getsize(path)   #returns size of a file in bytes , we need to specify the path ex : "users/buzzer tea/downloads/current_file.txt"

            except FileNotFoundError:
                return False #return False if file dosent exist , exit function.
            
            if current_size != previous_size:
                previous_size = current_size
                time.sleep(delay)

            else:
                return True
        return False  #if after 1.3 * 3 seconds ,current_size != previous_size , the file is taking too long and we give up on it.


    def on_moved(self, event):              #this method makes it so easy because i dont have to check myself if a file is created, it does this for me
       
       if event.is_directory:
           return
       
       
       if os.path.dirname(event.dest_path) != path_to_folder_i_want_to_monitor:
            return
              
       _,extension = os.path.splitext(event.dest_path)
       if extension.lower() in bad_ext :
           print(f"Ignored file: {event.dest_path}")
           return

       if self.is_file_stable(event.dest_path) == False:
           return


       print(f"_______________________-{event.dest_path}_______________________________")
       meme = FileOrganizingYey(path_to_folder_i_want_to_monitor,event.dest_path ,extension )
       meme.finally_organizing()



    



if __name__ == "__main__":
    
    event_handler = MyHandler()
    observer = Observer() #we initialize the observer to watch the folder

    observer.schedule(event_handler, path=path_to_folder_i_want_to_monitor, recursive=False)   #here we link the eventhandler & observer

    observer.start() #now the observer starts watching , starting its own BACKGROUND THREAD and triggers the corresponding methods of FileSystemHnandler



    #this while loop is just to keep the observer alive because this is a mainthread and background thread cant run without this mainthread
    try:
        while True:
            time.sleep(1) #waits for 1 second between running the loop again in order not to overload the CPU

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt______________________________")
    except Exception as e:
        print(f"Unexpected error: {e}___________________________________")
    finally:
        observer.stop()#requests the observer to stop
        observer.join()#safety net , makes sure it truly stops , waits for the observer to finish its work and actually stop.

    