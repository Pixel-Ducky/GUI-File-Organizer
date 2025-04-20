from main_organiser import FileOrganizingYey

from PyQt6.QtWidgets import QApplication,QMainWindow,QPushButton , QLabel , QWidget,QVBoxLayout,QFileDialog,QScrollArea
from PyQt6.QtCore  import QSize , Qt
from PyQt6.QtGui import QPalette, QColor , QPixmap, QPainter,QCursor


# organizer = FileOrganizingYey(r'C:\Users\Buzzer Tea\Desktop\mixed_files')
# organizer.finally_organizing()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle('File Organizer')
        self.setMaximumHeight(600)
        self.setMinimumHeight(350)
        self.setMaximumWidth(900)
        self.setMinimumWidth(350)

        self.selected_path = None  # 👈 Store the folder path here

        self.label = QLabel("No Folder selected.", self)
        self.button = QPushButton("Choose a folder", self)
        self.organize_button = QPushButton("Organize", self)
        self.done_message = QLabel("", self)

        self.button.setMinimumSize(100, 35)
        self.label.setMaximumHeight(30)
        self.done_message.setMaximumSize(350, 30)


        self.button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.organize_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.organize_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.done_message, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setCentralWidget(central_widget)

        # ✅ Connect properly
        self.button.clicked.connect(self.open_folder_dialog)
        self.organize_button.clicked.connect(self.organize)

        # Styling
        self.label.setObjectName("show_path_label")
        self.button.setObjectName("button")
        self.setStyleSheet("""
            QLabel {
                font-size:17px;
                color:white;
                border: 2px solid gray;
                padding: 4px;
                margin-top: 0;
                font-family:Comic Sans MS;
                background-color:black;
            }
            QMainWindow {
                background-color:black;
            }
            QPushButton {
                font-family:Comic Sans MS;
                color:blue;
                font-size:20px;
                border: 2px solid blue;
                border-radius:10px;
                background-color:white;
            }
                           
            QPushButton:hover{
                    background-color:#d4f1f4;    
                           }
        """)

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose Folder", "")
        if folder:
            self.selected_path = folder  # ✅ Save the path
            self.label.setText(folder)
        else:
            self.selected_path = None
            self.label.setText("No folder selected.")

    def organize(self):
        if self.selected_path:
            self.done_message.setText("Organizing...")
            y = FileOrganizingYey(self.selected_path)
            y.finally_organizing()
            self.done_message.setText("Done organizing!")
        else:
            self.done_message.setText("❌ No folder selected.")


        
  

        



app = QApplication([])
window = MainWindow()
window.show()
app.exec()