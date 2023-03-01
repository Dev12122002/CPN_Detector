from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import res
from pymongo import MongoClient
from config import Config
from helper import *
import time
from RegisterUi import *
from startup import *


class Home(QtWidgets.QWidget):
    # switch_window = QtCore.pyqtSignal()

    def login(self):
        loginVar = cnt.show_Home

    def setupUi(self, Form):
        Form.setObjectName("LoginForm")
        Form.resize(625, 565)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 550, 500))
        self.widget.setStyleSheet("QPushButton#pushButton{\n"
                                  "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
                                  "    color:rgba(255, 255, 255, 210);\n"
                                  "    border-radius:5px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton:hover{\n"
                                  "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(85, 98, 112, 226), stop:1 rgba(11, 131, 120, 219));\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton:pressed{\n"
                                  "    padding-left:5px;\n"
                                  "    padding-top:5px;\n"
                                  "    background-color:rgba(150, 123, 111, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton_2, #pushButton_3, #pushButton_4, #pushButton_5{\n"
                                  "    background-color: rgba(0, 0, 0, 0);\n"
                                  "    color:rgba(85, 98, 112, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover{\n"
                                  "    color: rgba(131, 96, 53, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed{\n"
                                  "    padding-left:5px;\n"
                                  "    padding-top:5px;\n"
                                  "    color:rgba(91, 88, 53, 255);\n"
                                  "}\n"
                                  "\n"
                                  "")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 280, 430))
        self.label_2.setStyleSheet("background-image: url(:/images/x-ray1.png);\n"
                                   "background-color:rgba(0, 0, 0, 80);\n"
                                   "border-top-left-radius: 50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(270, 30, 245, 430))
        self.label_3.setStyleSheet("background-color:rgba(80, 80, 80, 255);\n"
                                   "border-bottom-right-radius: 50px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(340, 80, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:rgba(255, 255, 255, 170);")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(295, 150, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                    "border:none;\n"
                                    "border-bottom:2px solid qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
                                    "color:rgba(255, 255, 255, 240);\n"
                                    "padding-bottom:7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(295, 215, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(255, 255, 255, 0);\n"
                                      "border:none;\n"
                                      "border-bottom:2px solid  qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
                                      "color:rgba(255, 255, 255, 240);\n"
                                      "padding-bottom:7px;")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(295, 295, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(290, 360, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:rgba(255, 255, 255, 210);")
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName("label_5")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(50, 40, 180, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:rgba(0, 70, 100, 200);")
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(290, 390, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:rgba(255, 255, 255, 210);")
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setGeometry(QtCore.QRect(380, 390, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_8.setStyleSheet("color:rgba(255, 255, 255, 210);")
        self.label_8.setWordWrap(False)
        self.label_8.setObjectName("label_8")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Log In"))
        self.lineEdit.setPlaceholderText(_translate("Form", "  User Name"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "  Password"))
        self.pushButton.setText(_translate("Form", "L o g  I n"))
        self.pushButton.clicked.connect(self.login)
        self.label_5.setText(_translate(
            "Form", "Forgot your User Name or password?"))
        self.label_7.setText(_translate("Form", "Home Page"))
        self.label_6.setText(_translate("Form", "New User ?"))
        self.label_8.setText(_translate("Form", "Register"))
        clickable(self.label_8).connect(self.goToRegister)

    def goToRegister(self):
        time.sleep(0.3)
        print("call")
        # self.register = QtWidgets.QMainWindow()
        # RegisterForm = QtWidgets.QWidget()
        # self.ui = Register()
        # self.ui.setupUi(RegisterForm)
        # RegisterForm.show()
        # LoginForm.hide()
        # cnt = Controller()
        # cnt.login.close()
        self.switch_window.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # client = MongoClient('mongodb+srv://devoza:12345@x-ray-cluster.wlwm3cu.mongodb.net/?retryWrites=true&w=majority')
    # db = client.CPN
    # user = {
    #         "username" : "dev",
    #         "password" : "12345"
    # }
    config = Config()
    config.create_collection('Users')
    # config.insert_data('Users', user)
    HomeForm = QtWidgets.QWidget()
    ui = Home()
    ui.setupUi(HomeForm)
    HomeForm.show()
    sys.exit(app.exec_())
