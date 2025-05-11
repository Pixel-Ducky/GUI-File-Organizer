# GUI-File-Organizer
this program uses watchdog to monitor the 'Downloads' folder for new files.
every file that end up in Downloads by downloading them from the web will trigger an event.
if the files have the following extensions : '.tmp', '.crdownload', '.part', '.json',  '.ini','.exe','.zip'
they will be ignored.
the below extension will be moved accordingly:

.jpg .png .jpeg .gif  .jfif   --> Pictures\pics  
.pdf .epub --> Desktop\Books  
.docx .pptx .xlsx -->Documents\Folder_Projects  
.txt --> Documents\Folder_Notepad  
.mp4 --> Documents\Folder_Video  
.mp3 .mov-->Documents\Folder_Audio  

If you rename a file in 'Downloads' it will trigger  'finally_organizing()' which will send that renamed file to the according Folder as above.

🌴PRESS  CTRL + C TO STOP WATCHDOG FROM MONITORING🌷

chrome & windows use temporary files and store them before the actual file is completed. 
and when all the data for the file has been downloaded, the temporary file gets RENAMED to for example 'cute_cat.jpg'.

on_created gets triggered  not only for the finished file , but for these temporary files too , and if we try to move these temporary files
the files might get corrupted and the program will crash.
this 'premature' event trigger can be resolved by using 'on_moved' instead.

on_moved gets triggered only when files are RENAMED or MOVED from a folder to another.
because when temporary files are done collecting and putting together all  the neessary data  (that means the file is stable), 
they get RENAMED  and on_moved gets triggered.


on_moved has:
● src_path --> path to temporary file , users/yourname/Downloads/cute_cat.crdownload
● dest_path --> path to stable file , users/yourname/Downloads/cute_cat.jpg


some larger files get renamed BEFORE they become stable (.pptx, .docx , .pdf).
while using on_moved we provide  a check for the stability of the file and only 'organize' the file if its stable.
in this case we will wait for 1.3 * 3 seconds until we decide if the file is stable or not.
we check stability by comparing the size of the file a couple seconds ago , with the size of the file after a few seconds.
if they are equal , that means the file is done being written to and now can be 'organized'.