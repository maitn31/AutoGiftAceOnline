import PyQt5.uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
import sys
import subprocess
import webbrowser
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid
import platform


def is_paid(key, dictionary):
    for value in dictionary.values():
        if isinstance(value, dict):
            if is_paid(key, value):
                return True
        elif isinstance(value, str):
            if key in value:
                return True
    return False


def search_name(my_dict, search_str):
    for key, value in my_dict.items():
        if value == search_str:
            return key
        elif isinstance(value, dict):
            sub_key = search_name(value, search_str)
            if sub_key is not None:
                return key
    return None


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        PyQt5.uic.loadUi("AutoGift.ui", self)
        self.setWindowTitle("Auto Tang Qua")
        self.init_file_watcher()

        appdata_path = os.getenv('APPDATA')
        directory_path = os.path.join(appdata_path, 'AutoCry', 'AutoTangQua')
        file_path = os.path.join(directory_path, 'config.txt')
        count_path = os.path.join(directory_path, "count.txt")
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("")  # Create an empty file
        if not os.path.exists(file_path):
            with open(count_path, 'w') as file:
                file.write("") # Create an empty file
        count_path = os.path.join(directory_path, "count.txt")

        def copy_button_clicked():
            App.clipboard().setText(str(my_uuid))

        def facebook_button_clicked():
            webbrowser.open("https://www.facebook.com/CryAway")

        def start_button_clicked():
            if not os.path.exists(count_path):
                with open(count_path, 'w') as count_file:
                    count_file.write("")  # Create an empty file

            with open(file_path, 'w') as f:
                f.write("")

            with open(file_path, 'a') as f:
                f.write(f"{item.value()}\n")  # Create an empty file
                f.write(f"{amount.value()}\n")
                f.write(f"{receiver.text()}\n")
                f.write(f"{speed.currentText()}")

            if authentication:
                subprocess.call(['java', '-jar', 'config', '-r', './build/'])

        authentication = False
        namespace = uuid.uuid5(uuid.NAMESPACE_DNS, f"{platform.node()}-{uuid.getnode()}")
        my_uuid = uuid.uuid5(namespace, "unique_identifier_for_device")
        cred = credentials.Certificate("./auth")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://pythonprojecttest-4a5f6-default-rtdb.firebaseio.com'
        })
        ref = db.reference("/users/AutoTangQua")
        print("Checking....")
        try:
            if is_paid(str(my_uuid), ref.get()):
                print("Checked okay")
                authentication = True
                print("Hello", search_name(ref.get(), str(my_uuid)))
                # subprocess.call(['java', '-jar', 'config', '-r', './build/'])
            else:
                print("Vui long lien he fb.com/CryAway de duoc cap ban quyen")
                print("Ma dang nhap cua ban la ", my_uuid)
        except (ValueError, Exception):
            print("Vui long lien he fb.com/CryAway de duoc cap ban quyen")
            print("Ma dang nhap cua ban la ", my_uuid)

        copy_button = self.findChild(QPushButton, "copy_button")
        copy_button.clicked.connect(copy_button_clicked)
        id_label = self.findChild(QLabel, "id_label")
        id_label.setText(f"Your user ID is: {str(my_uuid)}")
        if authentication:
            id_label.setText(f"Hello {search_name(ref.get(), str(my_uuid))}")
        facebook_button = self.findChild(QPushButton, "facebook_button")
        facebook_button.clicked.connect(facebook_button_clicked)
        start_button = self.findChild(QPushButton, "start_button")
        start_button.clicked.connect(start_button_clicked)
        item = self.findChild(QSpinBox, "item_box")
        amount = self.findChild(QSpinBox, "amount_box")
        receiver = self.findChild(QLineEdit, "receiver_text")
        speed = self.findChild(QComboBox, "speed_box")

        self.show()

    def init_file_watcher(self):

        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(count_path)
        self.watcher.fileChanged.connect(self.fileChangedHandler)

    def fileChangedHandler(self):
        appdata_path = os.getenv('APPDATA')
        directory_path = os.path.join(appdata_path, 'AutoCry', 'AutoTangQua')
        count_path = os.path.join(directory_path, "count.txt")
        with open(count_path, 'r') as count_read:
            count_path_content = count_read.read().strip()
            print(count_path_content)
        self.findChild(QLabel, "count_label").setText(str(count_path_content))


# create pyqt5 app


if __name__ == '__main__':
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()

    # start the app
    sys.exit(App.exec())
