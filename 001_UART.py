import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import serial
import ports
import codecs


class MainWindow(QWidget):

    ser = serial.Serial()
    counter = 0

    def __init__(self):
        super().__init__()
        self.title_label = QLabel(self)
        self.title_portline = QLabel(self)   # <-
        self.title_dropbox = QLabel(self)
        self.connect_button = QPushButton(self)
        self.clear_button = QPushButton(self)

        self.Red = QCheckBox(self)
        self.Green = QCheckBox(self)
        self.Yellow = QCheckBox(self)

        self.dropbox = QComboBox(self)
        self.port_line = QLineEdit(self)
        self.port_text = QTextEdit(self)
        self.message = QMessageBox(self)
        self.receive_area = QTextEdit(self)

        ports.list_ports()
        self.window_set()
        self.title_set()
        self.connect_button_set()
        self.clear_button_set()
        self.boxs_set()
        self.dropbox_set()
        self.port_area()
        self.data_receive()
        self.message_box_set()
        self.show()

    # Window settings
    def window_set(self):
        self.setWindowTitle("STM - UART Interface")
        self.setWindowIcon(QIcon("python-removebg-preview (1).png"))
        self.setGeometry(1000, 200, 650, 580)
        self.setFixedSize(QSize(650, 580))

    # Label settings
    def title_set(self):
        self.title_label.setText("UART Communication")
        self.title_label.move(220, 10)
        self.title_label.setAlignment(Qt.AlignBottom)
        self.title_label.setFont(QFont("Calibri", 13))

    def connect_button_set(self):
        self.connect_button.setText("Connect")
        self.connect_button.setFont(QFont("Calibri", 10))
        self.connect_button.setStyleSheet("QPushButton{background-color : blue;"
                                          "color:white;"
                                          "border-radius:15;"
                                          "border:2px solid black}"
                                          "QPushButton::hover{background-color:green;}")
        self.connect_button.move(330, 120)
        self.connect_button.resize(100, 30)
        self.connect_button.clicked.connect(self.click_button)

    def clear_button_set(self):
        self.clear_button.setText("Clear")
        self.clear_button.setFont(QFont("Calibri", 10))
        self.clear_button.setStyleSheet("QPushButton{border-radius:15;"
                                        "border:2px solid black;}")
        self.clear_button.move(460, 120)
        self.clear_button.resize(100, 30)
        self.clear_button.clicked.connect(self.clear_stream)

    # Check box settings
    def boxs_set(self):
        self.Red.move(330, 170)
        self.Green.move(330, 190)
        self.Yellow.move(330, 210)
        self.Red.setText("Red")
        self.Red.setFont(QFont("Calibri", 9))
        self.Green.setText("Green")
        self.Green.setFont(QFont("Calibri", 9))
        self.Yellow.setText("Yellow")
        self.Yellow.setFont(QFont("Calibri", 9))
        self.Red.stateChanged.connect(lambda: self.check_box(self.Red))
        self.Green.stateChanged.connect(lambda: self.check_box(self.Green))
        self.Yellow.stateChanged.connect(lambda: self.check_box(self.Yellow))

    # DropBox settings
    def dropbox_set(self):
        self.dropbox.move(330, 75)
        self.dropbox.resize(100, 26)
        self.dropbox.addItems(["",  "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400",
                              "57600", "115200"])
        self.title_dropbox.setText("Baudrate ")
        self.title_dropbox.setFont(QFont("Calibri Bold", 10))
        self.title_dropbox.move(330, 55)

    # Text alani settings
    def port_area(self):
        text_title = QLabel(self)
        text_title.setText("Available Ports")
        text_title.resize(120, 20)
        text_title.setFont(QFont("Calibri Bold", 9))
        text_title.move(10, 27)
        self.port_text.setPlaceholderText("Available Ports")
        self.port_text.setFont(QFont("Calibri Bold", 9))
        self.port_text.setAlignment(Qt.AlignBottom)
        self.port_text.resize(250, 200)
        self.port_text.move(10, 50)
        self.port_text.setEnabled(False)

        for port in ports.result:
            self.port_text.append(port)

        # Line and title of line settings
        self.port_line.move(460, 76)
        self.port_line.resize(100, 24)
        self.title_portline.setText("Port")
        self.title_portline.setFont(QFont("Calibri Bold", 9))
        self.title_portline.move(465, 55)

    def data_receive(self):
        self.receive_area.move(10, 300)
        self.receive_area.resize(630, 250)
        self.receive_area.setStyleSheet("QTextEdit{border:1px solid black;"
                                        "border-radius: 2;}")
        self.receive_area.setFont(QFont("Calibri Bold", 9))

        line = QLineEdit(self)
        line.move(10, 265)
        line.resize(630, 30)
        line.setText("Stream Data")
        line.setFont(QFont("Calibri Bold", 9))
        line.setStyleSheet("QLineEdit{background-color:gray;"
                           "border-radius: 10;"
                           "color:black}")
        line.setEnabled(False)

    def message_box_set(self):
        self.message.setWindowTitle("Message Box")
        self.message.setWindowIcon(QIcon("python-removebg-preview (1).png"))
        self.message.setIcon(QMessageBox.Warning)

    def click_button(self):

        if self.port_line.text() == "" or self.dropbox.currentText() == "":
            self.message.setText("Enter the required information")
            self.message.show()

        elif self.port_line.text() not in ports.result:
            self.message.setText("Invalid port")
            self.message.show()

        else:
            self.counter += 1
            if self.counter == 1:
                self.ser = serial.Serial(self.port_line.text(), self.dropbox.currentText())
                self.connect_button.setStyleSheet("QPushButton{background-color : green;"
                                                  "color:white;"
                                                  "border-radius:15;"
                                                  "border:2px solid black}"
                                                  "QPushButton::hover{background-color:green;}")
            else:
                self.counter = 0
                self.connect_button_set()
                self.ser.close()

    def clear_stream(self):
        self.receive_area.clear()

    def check_box(self, checkbox):

        if self.counter == 1:
            if checkbox.text() == "Red":
                if checkbox.isChecked():
                    self.Red.setStyleSheet("color:red")
                    self.ser.write(b"Red yak")
                    self.receive_area.append(self.ser.readline().decode('utf-8', errors='ignore'))

                else:
                    self.Red.setStyleSheet("color:black")
                    self.ser.write(b"Red son")
                    self.receive_area.append(self.ser.readline().decode('utf-8', errors='ignore'))

            if checkbox.text() == "Green":
                if checkbox.isChecked():
                    self.Green.setStyleSheet("color:Green")
                    self.ser.write(b"Gre yak")
                    self.receive_area.append(self.ser.readline().decode('utf-8', errors='ignore'))

                else:
                    self.Green.setStyleSheet("color:black")
                    self.ser.write(b"Gre son")
                    self.receive_area.append(self.ser.readline().decode('utf-8', errors='ignore'))

            if checkbox.text() == "Yellow":
                if checkbox.isChecked():
                    self.Yellow.setStyleSheet("color:Yellow")
                    self.ser.write(b"Yel yak")
                    self.receive_area.append(self.ser.readline().decode('utf-8', errors='ignore'))

                else:
                    self.Yellow.setStyleSheet("color:black")
                    self.ser.write(b"Yel son")
                    self.receive_area.append(self.ser.readline().decode('utf-8', errors='ignore'))

        else:
            checkbox.setChecked(False)
            self.message.setText("Not Connected port!")
            self.message.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    U_window = MainWindow()
    sys.exit(app.exec())
