from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import res
from pymongo import MongoClient
from config import Config
from threading import Timer
import time
import re
from loginUi import *
from helper import *
import globalvar
from threading import *


class Register(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def check_Register(self):
        if self.lineEdit.text() == "":
            self.label_animation.setHidden(True)
            self.label_9.setText("email is required")
            self.label_9.setHidden(False)
            r = Timer(5.0, lambda: self.label_9.setHidden(True))
            r.start()
            return

        if self.lineEdit_2.text() == "":
            self.label_animation.setHidden(True)

            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.label_10.setFont(font)

            self.label_10.setText("password is required")
            self.label_10.setHidden(False)
            r = Timer(5.0, lambda: self.label_10.setHidden(True))
            r.start()
            return

        user = {
            "email": self.lineEdit.text(),
            "password": self.lineEdit_2.text()
        }

        config = Config()
        resultUser = config.get_Data_By_Specific_Field(
            "Users", "email", user['email'])
        if len(resultUser) != 0:
            self.label_animation.setHidden(True)
            self.label_9.setText("Email already exist")
            self.label_9.setHidden(False)
            r = Timer(5.0, lambda: self.label_9.setHidden(True))
            r.start()
            return

        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{6,}$"

        if re.match(password_pattern, user['password']) is None:  # Returns None
            self.label_animation.setHidden(True)

            font = QtGui.QFont()
            font.setPointSize(8)
            font.setBold(True)
            font.setWeight(75)
            self.label_10.setFont(font)
            self.label_10.setText(
                "Must be minimum 6 digit\nalphanumeric string with\natleast 1 capital letter")
            self.label_10.setHidden(False)
            r = Timer(5.0, lambda: self.label_10.setHidden(True))
            r.start()
            return

        config.create_collection('Users')
        config.insert_data('Users', user)
        globalvar.ismain = True
        globalvar.isloggedin = 1
        globalvar.email = user['email']
        settings = QtCore.QSettings('CPN-Detector', 'CPN-Detector')
        settings.setValue('loggedin', 1)
        settings.setValue('email', user['email'])
        self.switch_window.emit()

    def register(self):
        self.label_animation.setHidden(False)
        self.movie.start()
        t1 = Thread(target=self.check_Register)
        t1.start()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(625, 565)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(40, 30, 550, 500))
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
        self.label_4.setGeometry(QtCore.QRect(340, 70, 130, 40))
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
        self.lineEdit.setGeometry(QtCore.QRect(300, 130, 190, 40))
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
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 210, 190, 40))
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
        self.pushButton.setGeometry(QtCore.QRect(300, 310, 190, 40))
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
        font.setPointSize(7)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:rgba(255, 255, 255, 210);")
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setGeometry(QtCore.QRect(440, 390, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_8.setStyleSheet("color:rgba(255, 255, 255, 210);")
        self.label_8.setWordWrap(False)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setGeometry(QtCore.QRect(310, 180, 191, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color:rgba(255, 0, 0, 200);")
        self.label_9.setWordWrap(False)
        self.label_9.setObjectName("label_9")

        self.label_animation = QtWidgets.QLabel(self.widget)
        self.label_animation.setGeometry(QtCore.QRect(367, 240, 191, 80))
        self.movie = QtGui.QMovie("loading.gif")
        self.label_animation.setMovie(self.movie)

        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setGeometry(QtCore.QRect(300, 247, 225, 60))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color:rgba(255, 0, 0, 200);")
        self.label_10.setWordWrap(False)
        self.label_10.setObjectName("label_10")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Register"))
        self.lineEdit.setPlaceholderText(_translate("Form", "  Email"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "  Password"))
        self.pushButton.setText(_translate("Form", "R e g i s t e r"))
        self.pushButton.clicked.connect(self.register)
        self.label_5.setText(_translate(
            "Form", "Forgot your User Name or password?"))
        self.label_7.setText(_translate("Form", "CPN Detector"))
        self.label_6.setText(_translate("Form", "Already have an account ?"))
        self.label_8.setText(_translate("Form", "Login"))
        clickable(self.label_8).connect(self.goToLogin)
        self.label_9.setText(_translate("Form", "Email already exist"))
        self.label_10.setText(_translate("Form", "Must be minimum 6 digit\n"
                                         "alphanumeric string with atleast\n1 capital letter"))
        self.label_9.setHidden(True)
        self.label_10.setHidden(True)

    def goToLogin(self):
        time.sleep(0.3)
        # self.LoginForm = QtWidgets.QWidget()
        # self.ui = Login()
        # self.ui.setupUi(self.LoginForm)
        # self.LoginForm.show()
        # RegisterForm.hide()
        self.switch_window.emit()
