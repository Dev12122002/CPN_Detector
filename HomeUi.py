from PyQt5 import QtCore, QtGui, QtWidgets
import resource
import sys
from PyQt5.QtWidgets import *
from helper import *
import pandas as pd
import tensorflow as tf
from keras.models import load_model
import numpy as np
from config import Config
from fpdf import FPDF
import time
from threading import *
import globalvar
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot


class Worker(QObject):
    completed = Signal(int)

    @Slot(int)
    def do_work(self, n):
        globalvar.uploaded_files = []
        config = Config()
        config.fetch_pdf()
        self.completed.emit(1)

    @Slot(int)
    def worker_predict_diseases(self, n):

        filepaths = []
        img_path = globalvar.selected_image_path
        filepaths.append(img_path)
        labels = list(map(lambda x: 'x', filepaths))
        # prediction = ['Covid-19', 'Normal', 'Pneumonia']

        filepaths = pd.Series(filepaths, name='Filepath',
                              dtype=pd.StringDtype()).astype(str)
        labels = pd.Series(labels, name='Label', dtype=pd.StringDtype())

        test1 = pd.concat([filepaths, labels], axis=1)
        size = 224
        color_mode = 'rgb'
        batch_size = 32

        test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
            preprocessing_function=tf.keras.applications.vgg19.preprocess_input,
            rescale=1./255
        )

        predict_image = test_generator.flow_from_dataframe(
            dataframe=test1,
            x_col='Filepath',
            y_col='Label',
            target_size=(size, size),
            color_mode=color_mode,
            class_mode='categorical',
            batch_size=batch_size,
            shuffle=False
        )

        best_model = load_model(
            'CPN_Model/best_model.h5')
        y_pred = best_model.predict(predict_image)

        globalvar.y_pred = y_pred

        self.completed.emit(1)


class Home(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal()
    work_requested = Signal(int)
    completed = Signal(int)

    def setupUi(self, HomePage):

        HomePage.setObjectName("HomePage")
        HomePage.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # HomePage.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        HomePage.resize(1318, 849)
        # HomePage.setStyleSheet("padding : 0px;")
        self.titlebar = QtWidgets.QWidget(HomePage)
        self.titlebar.setGeometry(QtCore.QRect(0, 0, 1318, 61))
        self.titlebar.setStyleSheet("padding : 10%; margin: 0px;")
        self.titlebar.setObjectName("titlebar")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setColor(QtGui.QColor(100, 100, 100).lighter())
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        self.titlebar.setGraphicsEffect(shadow)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.titlebar)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.title = QtWidgets.QLabel(self.titlebar)
        font = QtGui.QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.horizontalLayout_2.addWidget(self.title)
        spacerItem = QtWidgets.QSpacerItem(
            977, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.minimize_btn = QtWidgets.QPushButton(self.titlebar)
        self.minimize_btn.setStyleSheet("padding:20%;\n"
                                        "border: none;\n"
                                        "outline: none;")
        self.minimize_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icons/minimize24.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minimize_btn.setIcon(icon)
        self.minimize_btn.setCheckable(True)
        self.minimize_btn.setAutoExclusive(True)
        self.minimize_btn.setObjectName("minimize_btn")
        self.horizontalLayout.addWidget(self.minimize_btn)
        self.close_btn = QtWidgets.QPushButton(self.titlebar)
        self.close_btn.setStyleSheet("padding:20%;\n"
                                     "border: none;\n"
                                     "outline: none;")
        self.close_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icons/close-24.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close_btn.setIcon(icon1)
        self.close_btn.setCheckable(True)
        self.close_btn.setAutoExclusive(True)
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.icon_only = QtWidgets.QWidget(HomePage)
        self.icon_only.setGeometry(QtCore.QRect(0, 65, 81, 784))
        self.icon_only.setObjectName("icon_only")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.menu_btn = QtWidgets.QPushButton(self.icon_only)
        self.menu_btn.setStyleSheet("padding:10%;\n"
                                    "border: none;\n"
                                    "outline: none;")
        self.menu_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/icons/menu-4-24.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu_btn.setIcon(icon2)
        # self.menu_btn.setCheckable(True)
        self.menu_btn.setAutoExclusive(True)
        self.menu_btn.setObjectName("menu_btn")
        self.verticalLayout.addWidget(self.menu_btn)
        self.house_btn = QtWidgets.QPushButton(self.icon_only)
        self.house_btn.setStyleSheet("padding:10%;\n"
                                     "border: none;\n"
                                     "outline: none;")
        self.house_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/icons/house-24.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(
            ":/icon/icons/house-24-light.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.house_btn.setIcon(icon3)
        self.house_btn.setCheckable(True)
        self.house_btn.setAutoExclusive(True)
        self.house_btn.setObjectName("house_btn")
        self.verticalLayout.addWidget(self.house_btn)
        self.pdf_btn = QtWidgets.QPushButton(self.icon_only)
        self.pdf_btn.setStyleSheet("padding:10%;\n"
                                   "border: none;\n"
                                   "outline: none;")
        self.pdf_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/icons/pdf-24.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(
            ":/icon/icons/pdf-24-light.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pdf_btn.setIcon(icon4)
        self.pdf_btn.setCheckable(True)
        self.pdf_btn.setAutoExclusive(True)
        self.pdf_btn.setObjectName("pdf_btn")
        self.verticalLayout.addWidget(self.pdf_btn)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 554, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.setting_btn = QtWidgets.QPushButton(self.icon_only)
        self.setting_btn.setStyleSheet("padding:10%;\n"
                                       "border: none;\n"
                                       "outline: none;")
        self.setting_btn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(
            ":/icon/icons/settings-9-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(
            ":/icon/icons/settings-9-24-light.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setting_btn.setIcon(icon5)
        self.setting_btn.setCheckable(True)
        self.setting_btn.setAutoExclusive(True)
        self.setting_btn.setObjectName("setting_btn")
        self.verticalLayout_2.addWidget(self.setting_btn)
        self.logout_btn = QtWidgets.QPushButton(self.icon_only)
        self.logout_btn.setStyleSheet("padding:10%;\n"
                                      "border: none;\n"
                                      "outline: none;")
        self.logout_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icon/icons/logout-24.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logout_btn.setIcon(icon6)
        self.logout_btn.setCheckable(True)
        self.logout_btn.setAutoExclusive(True)
        self.logout_btn.setObjectName("logout_btn")
        self.verticalLayout_2.addWidget(self.logout_btn)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.full_menu = QtWidgets.QWidget(HomePage)
        # QtCore.QRect(10, 80, 0, 761)
        # self.full_menu.setGeometry(QtCore.QRect(80, 65, 181, 784))
        self.full_menu.setGeometry(QtCore.QRect(0, 65, 0, 781))
        self.full_menu.setObjectName("full_menu")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.full_menu)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.close_menu_btn = QtWidgets.QPushButton(self.full_menu)
        self.close_menu_btn.setStyleSheet("padding:20%;\n"
                                          "border: none;\n"
                                          "outline: none;")
        self.close_menu_btn.setText("")
        self.close_menu_btn.setIcon(icon1)
        # self.close_menu_btn.setCheckable(True)
        self.close_menu_btn.setAutoExclusive(True)
        self.close_menu_btn.setObjectName("close_menu_btn")
        self.verticalLayout_4.addWidget(self.close_menu_btn)
        self.home_btn_full = QtWidgets.QPushButton(self.full_menu)
        self.home_btn_full.setStyleSheet("padding:10%;\n"
                                         "border: none;\n"
                                         "outline: none;")
        self.home_btn_full.setIcon(icon3)
        self.home_btn_full.setCheckable(True)
        self.home_btn_full.setAutoExclusive(True)
        self.home_btn_full.setObjectName("home_btn_full")
        self.verticalLayout_4.addWidget(self.home_btn_full)
        self.pdf_btn_full = QtWidgets.QPushButton(self.full_menu)
        self.pdf_btn_full.setStyleSheet("padding:10%;\n"
                                        "border: none;\n"
                                        "outline: none;")
        self.pdf_btn_full.setIcon(icon4)
        self.pdf_btn_full.setCheckable(True)
        self.pdf_btn_full.setAutoExclusive(True)
        self.pdf_btn_full.setObjectName("pdf_btn_full")
        self.verticalLayout_4.addWidget(self.pdf_btn_full)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 554, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.setting_btn_full = QtWidgets.QPushButton(self.full_menu)
        self.setting_btn_full.setStyleSheet("padding:10%;\n"
                                            "border: none;\n"
                                            "outline: none;")
        self.setting_btn_full.setIcon(icon5)
        self.setting_btn_full.setCheckable(True)
        self.setting_btn_full.setAutoExclusive(True)
        self.setting_btn_full.setObjectName("setting_btn_full")
        self.verticalLayout_5.addWidget(self.setting_btn_full)
        self.logout_btn_full = QtWidgets.QPushButton(self.full_menu)
        self.logout_btn_full.setStyleSheet("padding:10%;\n"
                                           "border: none;\n"
                                           "outline: none;")
        self.logout_btn_full.setIcon(icon6)
        self.logout_btn_full.setCheckable(True)
        self.logout_btn_full.setAutoExclusive(True)
        self.logout_btn_full.setObjectName("logout_btn_full")
        self.verticalLayout_5.addWidget(self.logout_btn_full)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.stackedWidget = QtWidgets.QStackedWidget(HomePage)
        self.stackedWidget.setGeometry(QtCore.QRect(260, 60, 1061, 790))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")

        font = QtGui.QFont()
        font.setPointSize(13)

        self.upload_image = QtWidgets.QLabel(self.page)
        self.upload_image.setGeometry(QtCore.QRect(190, 130, 361, 371))
        self.upload_image.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.upload_image.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.upload_image.setStyleSheet("")
        self.upload_image.setText("")
        self.upload_image.setPixmap(QtGui.QPixmap(":/icon/icons/add-file.png"))
        self.upload_image.setScaledContents(True)
        self.upload_image.setObjectName("upload_image")
        self.predict_btn = QtWidgets.QPushButton(self.page)
        self.predict_btn.setGeometry(QtCore.QRect(280, 530, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.predict_btn.setFont(font)
        self.predict_btn.setCheckable(True)
        self.predict_btn.setAutoExclusive(True)
        self.predict_btn.setObjectName("predict_btn")

        self.predict_anim = QtWidgets.QLabel(self.page)
        self.predict_anim.setGeometry(QtCore.QRect(325, 600, 360, 45))
        self.predict_movie = QtGui.QMovie("save_loading.gif")
        self.predict_anim.setMovie(self.predict_movie)

        self.result_cpn_widget = QtWidgets.QWidget(self.page)
        self.result_cpn_widget.setGeometry(QtCore.QRect(610, 45, 0, 700))
        self.result_cpn_widget.setObjectName("result_cpn_widget")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setColor(QtGui.QColor(100, 100, 100).lighter())
        shadow.setOffset(-4, 4)
        self.setGraphicsEffect(shadow)
        self.result_cpn_widget.setGraphicsEffect(shadow)

        self.save_btn = QtWidgets.QPushButton(self.result_cpn_widget)
        self.save_btn.setGeometry(QtCore.QRect(170, 520, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.save_btn.setFont(font)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/icons/pdf-24.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_btn.setIcon(icon7)
        self.save_btn.setCheckable(True)
        self.save_btn.setAutoExclusive(True)
        self.save_btn.setDefault(False)
        self.save_btn.setFlat(False)
        self.save_btn.setObjectName("save_btn")
        self.result_lbl = QtWidgets.QLabel(self.result_cpn_widget)
        self.result_lbl.setGeometry(QtCore.QRect(120, 40, 229, 101))
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(19)
        font.setItalic(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.result_lbl.setFont(font)
        self.result_lbl.setTextFormat(QtCore.Qt.AutoText)
        self.result_lbl.setScaledContents(True)
        self.result_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.result_lbl.setObjectName("result_lbl")
        self.layoutWidget_2 = QtWidgets.QWidget(self.result_cpn_widget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(130, 150, 271, 132))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.cpn_value = QtWidgets.QFormLayout(self.layoutWidget_2)
        self.cpn_value.setContentsMargins(15, 15, 15, 15)
        self.cpn_value.setSpacing(15)
        self.cpn_value.setObjectName("cpn_value")
        self.covid_19 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.covid_19.setFont(font)
        self.covid_19.setObjectName("covid_19")
        self.cpn_value.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.covid_19)
        self.covid_value = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.covid_value.setFont(font)
        self.covid_value.setObjectName("covid_value")
        self.cpn_value.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.covid_value)
        self.pneumonia = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pneumonia.setFont(font)
        self.pneumonia.setObjectName("pneumonia")
        self.cpn_value.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.pneumonia)
        self.pneumonia_value = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pneumonia_value.setFont(font)
        self.pneumonia_value.setObjectName("pneumonia_value")
        self.cpn_value.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.pneumonia_value)
        self.normal_value = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.normal_value.setFont(font)
        self.normal_value.setObjectName("normal_value")
        self.cpn_value.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.normal_value)
        self.normal = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.normal.setFont(font)
        self.normal.setObjectName("normal")
        self.cpn_value.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.normal)
        self.layoutWidget = QtWidgets.QWidget(self.result_cpn_widget)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 320, 229, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.save_form = QtWidgets.QFormLayout(self.layoutWidget)
        self.save_form.setContentsMargins(15, 15, 15, 15)
        self.save_form.setSpacing(15)
        self.save_form.setObjectName("save_form")
        self.age = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.age.setFont(font)
        self.age.setObjectName("age")
        self.save_form.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.age)
        self.age_spinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.age_spinBox.setFixedSize(140, 30)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.age_spinBox.setFont(font)
        self.age_spinBox.setObjectName("age_spinBox")
        self.save_form.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.age_spinBox)
        self.phone = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.phone.setFont(font)
        self.phone.setObjectName("phone")
        self.save_form.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.phone)
        self.phone_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.phone_lineEdit.setFixedSize(135, 30)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.phone_lineEdit.setFont(font)
        self.phone_lineEdit.setObjectName("phone_lineEdit")
        self.save_form.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.phone_lineEdit)
        self.name = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.save_form.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.name)
        self.name_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.name_lineEdit.setFixedSize(140, 30)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_lineEdit.setFont(font)
        self.name_lineEdit.setText("")
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.save_form.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.name_lineEdit)
        self.save_error = QtWidgets.QLabel(self.result_cpn_widget)
        self.save_error.setGeometry(QtCore.QRect(50, 590, 360, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.save_error.setFont(font)
        self.save_error.setAlignment(QtCore.Qt.AlignCenter)
        self.save_error.setObjectName("save_error")

        self.save_animation = QtWidgets.QLabel(self.result_cpn_widget)
        self.save_animation.setGeometry(QtCore.QRect(215, 590, 360, 45))
        self.save_movie = QtGui.QMovie("save_loading.gif")
        self.save_animation.setMovie(self.save_movie)

        self.pushButton_14 = QtWidgets.QPushButton(self.result_cpn_widget)
        self.pushButton_14.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.pushButton_14.setStyleSheet("padding:20%;\n"
                                         "border: none;\n"
                                         "outline: none;")
        self.pushButton_14.setText("")
        self.pushButton_14.setIcon(icon1)
        self.pushButton_14.setCheckable(True)
        self.pushButton_14.setObjectName("pushButton_14")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")

        self.table_header = QtWidgets.QTableWidget(self.page_2)
        self.table_header.setGeometry(QtCore.QRect(0, 130, 901, 600))
        self.table_header.setStyleSheet("background: transparent;")
        self.table_header.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.table_header.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_header.setShowGrid(False)
        self.table_header.setWordWrap(True)
        self.table_header.setRowCount(0)
        self.table_header.setObjectName("table_header")
        self.table_header.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setBackground(QtGui.QColor(199, 204, 210))
        self.table_header.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setBackground(QtGui.QColor(199, 204, 210))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_header.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setBackground(QtGui.QColor(199, 204, 210))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_header.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setBackground(QtGui.QColor(199, 204, 210))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.table_header.setHorizontalHeaderItem(3, item)
        self.table_header.horizontalHeader().setDefaultSectionSize(220)
        self.table_header.horizontalHeader().setSortIndicatorShown(True)
        self.table_header.horizontalHeader().setStretchLastSection(True)
        self.table_header.verticalHeader().setDefaultSectionSize(70)
        self.table_header.verticalHeader().setMinimumSectionSize(30)

        self.refresh_btn = QtWidgets.QPushButton(self.page_2)
        self.refresh_btn.setGeometry(QtCore.QRect(360, 20, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.refresh_btn.setFont(font)
        self.refresh_btn.setCheckable(True)
        self.refresh_btn.setAutoExclusive(True)
        self.refresh_btn.setObjectName("refresh_btn")

        self.download_success = QtWidgets.QLabel(self.page_2)
        self.download_success.setStyleSheet("color: darkgreen")
        self.download_success.setGeometry(QtCore.QRect(260, 75, 360, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.download_success.setFont(font)
        self.download_success.setAlignment(QtCore.Qt.AlignCenter)
        self.download_success.setObjectName("download_success")

        self.download_animation = QtWidgets.QLabel(self.page_2)
        self.download_animation.setGeometry(QtCore.QRect(400, 75, 360, 45))
        self.download_movie = QtGui.QMovie("save_loading.gif")
        self.download_animation.setMovie(self.download_movie)

        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(HomePage)
        self.stackedWidget.setCurrentIndex(0)
        self.close_btn.clicked.connect(HomePage.close)  # type: ignore
        self.house_btn.toggled['bool'].connect(
            self.home_btn_full.setChecked)  # type: ignore
        self.pdf_btn.toggled['bool'].connect(
            self.pdf_btn_full.setChecked)  # type: ignore
        self.setting_btn.toggled['bool'].connect(
            self.setting_btn_full.setChecked)  # type: ignore
        self.logout_btn.toggled['bool'].connect(
            self.logout_btn_full.setChecked)  # type: ignore
        self.home_btn_full.toggled['bool'].connect(
            self.house_btn.setChecked)  # type: ignore
        self.pdf_btn_full.toggled['bool'].connect(
            self.pdf_btn.setChecked)  # type: ignore
        self.setting_btn_full.toggled['bool'].connect(
            self.setting_btn.setChecked)  # type: ignore
        self.logout_btn_full.toggled['bool'].connect(
            self.logout_btn.setChecked)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HomePage)

    def retranslateUi(self, HomePage):
        _translate = QtCore.QCoreApplication.translate
        HomePage.setWindowTitle(_translate("HomePage", "Dialog"))
        self.title.setText(_translate("HomePage", "CPN DETECTOR"))
        self.home_btn_full.setText(_translate("HomePage", "   Home"))
        self.pdf_btn_full.setText(_translate("HomePage", "   PDF\'S"))
        self.setting_btn_full.setText(_translate("HomePage", "   Settings"))
        self.logout_btn_full.setText(_translate("HomePage", "   Logout"))

        self.table_header.verticalHeader().setVisible(False)

        self.predict_btn.setText(_translate("HomePage", "Predict"))
        self.refresh_btn.setText(_translate("HomePage", "Refresh"))
        self.save_btn.setText(_translate("HomePage", "  Save"))
        self.result_lbl.setText(_translate("HomePage", "R e s u l t"))
        self.covid_19.setText(_translate("HomePage", "Covid-19 :"))
        self.covid_value.setText(_translate("HomePage", "TextLabel"))
        self.pneumonia.setText(_translate("HomePage", "Pneumonia :"))
        self.pneumonia_value.setText(_translate("HomePage", "TextLabel"))
        self.normal_value.setText(_translate("HomePage", "TextLabel"))
        self.normal.setText(_translate("HomePage", "Normal :"))
        self.age.setText(_translate("HomePage", "Age :"))
        self.phone.setText(_translate("HomePage", "Phone :"))
        self.phone_lineEdit.setPlaceholderText(
            _translate("HomePage", "Phone Number"))
        self.name.setText(_translate("HomePage", "Name :"))
        self.name_lineEdit.setPlaceholderText(
            _translate("HomePage", "Patient Name"))
        self.save_error.setText(_translate("HomePage", ""))
        self.download_success.setText(_translate(
            "HomePage", "Download Successfully !!!"))
        self.download_success.setHidden(True)

        self.save_animation.setHidden(True)
        self.predict_anim.setHidden(True)

        self.table_header.setSortingEnabled(True)
        item = self.table_header.horizontalHeaderItem(1)
        item.setText(_translate("HomePage", "File Name"))
        item = self.table_header.horizontalHeaderItem(2)
        item.setText(_translate("HomePage", "Date"))
        item = self.table_header.horizontalHeaderItem(3)
        item.setText(_translate("HomePage", "Action"))

        btnlist = []
        for pdf in globalvar.uploaded_files:
            row = self.table_header.rowCount()
            self.table_header.insertRow(row)

            pdfbtn = QtWidgets.QPushButton()

            pdfbtn.setStyleSheet("""
                        QPushButton::pressed{
                                background-color: #fff;
                                border : none;
                                outline : none;
                        }
                """)

            pdficon = QtGui.QIcon(":/icon/icons/pdf-24.png")
            pdfbtn.setIcon(pdficon)

            btnlist.append(pdfbtn)
            self.table_header.setCellWidget(row, 0, pdfbtn)
            item = QTableWidgetItem(pdf['filename'])
            item.setTextAlignment(Qt.AlignCenter)
            self.table_header.setItem(
                row, 1, item)
            item = QTableWidgetItem(str(pdf['date']))
            item.setTextAlignment(Qt.AlignCenter)
            self.table_header.setItem(
                row, 2, item)

            pdfbtn = QtWidgets.QPushButton()

            pdfbtn.setStyleSheet("""
                        QPushButton::pressed{
                                background-color: #fff;
                                border : none;
                                outline : none;
                        }
                """)

            pdficon = QtGui.QIcon(":/icon/icons/download-2-24.png")
            pdfbtn.setIcon(pdficon)
            btnlist.append(pdfbtn)
            self.table_header.setCellWidget(row, 3, pdfbtn)

        j = -1
        i = 0
        for btn in btnlist:
            if i % 2 == 0:
                j += 1
            btn.clicked.connect(
                lambda checked, filename=globalvar.uploaded_files[j]['filename']: self.downloadPdf(filename))
            i += 1

        self.menu_btn.clicked.connect(self.expand_menu)
        self.close_menu_btn.clicked.connect(self.close_menu)
        clickable(self.upload_image).connect(self.select_File_And_Load)
        self.predict_btn.setDisabled(True)
        # self.save_btn.setDisabled(True)
        self.predict_btn.clicked.connect(self.predict)
        self.refresh_btn.clicked.connect(self.refresh_pdfs)
        self.save_btn.clicked.connect(self.savePdf)
        self.logout_btn.clicked.connect(self.logout)
        self.logout_btn_full.clicked.connect(self.logout)
        self.pdf_btn_full.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.pdf_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.home_btn_full.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))
        self.house_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_14.clicked.connect(self.close_result_cpn)
        self.home_btn_full.setChecked(True)
        self.house_btn.setChecked(True)
        # self.minimize_btn.clicked.connect(self.showMinimized)

    def showMinimized(self):
        self.showMinimized()

    def refresh_pdfs(self):
        self.download_animation.setHidden(False)
        self.download_movie.start()

        self.worker = Worker()
        self.worker_thread = QThread()

        self.worker.completed.connect(self.update_table)

        self.work_requested.connect(self.worker.do_work)

        # move worker to the worker thread
        self.worker.moveToThread(self.worker_thread)

        # start the thread
        self.worker_thread.start()
        self.work_requested.emit(1)

    def update_table(self):
        self.worker_thread.quit()
        self.download_movie.stop()
        self.download_animation.setHidden(True)
        self.table_header.setRowCount(0)
        btnlist = []
        row = 0
        for pdf in globalvar.uploaded_files:
            self.table_header.insertRow(row)

            pdfbtn = QtWidgets.QPushButton()

            pdfbtn.setStyleSheet("""
                                QPushButton::pressed{
                                        background-color: #fff;
                                        border : none;
                                        outline : none;
                                }
                        """)

            pdficon = QtGui.QIcon(":/icon/icons/pdf-24.png")
            pdfbtn.setIcon(pdficon)

            btnlist.append(pdfbtn)
            self.table_header.setCellWidget(row, 0, pdfbtn)

            item = QTableWidgetItem(pdf['filename'])
            item.setTextAlignment(Qt.AlignCenter)
            self.table_header.setItem(row, 1, item)
            item = QTableWidgetItem(str(pdf['date']))
            item.setTextAlignment(Qt.AlignCenter)
            self.table_header.setItem(row, 2, item)

            pdfbtn = QtWidgets.QPushButton()

            pdfbtn.setStyleSheet("""
                                QPushButton::pressed{
                                        background-color: #fff;
                                        border : none;
                                        outline : none;
                                }
                        """)

            pdficon = QtGui.QIcon(":/icon/icons/download-2-24.png")
            pdfbtn.setIcon(pdficon)
            btnlist.append(pdfbtn)
            self.table_header.setCellWidget(row, 3, pdfbtn)
            row += 1

        j = -1
        i = 0
        for btn in btnlist:
            if i % 2 == 0:
                j += 1
            btn.clicked.connect(
                lambda checked, filename=globalvar.uploaded_files[j]['filename']: self.downloadPdf(filename))
            i += 1

    def expand_menu(self):
        self.animation = QPropertyAnimation(self.full_menu, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(QtCore.QRect(0, 65, 0, 781))
        self.animation.setEndValue(QtCore.QRect(0, 65, 181, 781))
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def close_menu(self):
        self.animation = QPropertyAnimation(self.full_menu, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(QtCore.QRect(0, 65, 181, 781))
        self.animation.setEndValue(QtCore.QRect(0, 65, 0, 781))
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def select_File_And_Load(self):
        self.fname = QFileDialog.getOpenFileName(
            self, 'Open file', 'C:\\Users\devoz\Pictures', "Image files (*.jpg *.png *.jpeg)")
        # print(self.fname[0])
        if self.fname[0] != "":
            self.img_path = self.fname[0]
            globalvar.selected_image_path = self.fname[0]
            pixmap = QPixmap(self.fname[0])
            self.upload_image.setPixmap(pixmap)
        self.predict_btn.setDisabled(False)

    def logout(self):
        settings = QtCore.QSettings('CPN-Detector', 'CPN-Detector')
        settings.setValue('loggedin', 0)
        settings.setValue('email', '')
        self.switch_window.emit()

    def downloadPdf(self, filename):
        # print(filename)

        self.download_animation.setHidden(False)
        self.download_movie.start()
        t1 = Thread(target=self.thread_downloadPdf, args=(filename,))
        t1.start()

    def thread_downloadPdf(self, filename):
        config = Config()
        config.read_pdf(filename)
        self.download_movie.stop()
        self.download_animation.setHidden(True)
        self.download_success.setHidden(False)
        r = Timer(3.0, lambda: self.download_success.setHidden(True))
        r.start()

    def thread_savePdf(self):

        name = self.name_lineEdit.text()
        age = self.age_spinBox.value()
        phone = self.phone_lineEdit.text()

        config = Config()
        config.uploadPDF(name + '.pdf')
        self.save_error.setStyleSheet("color: darkgreen")
        self.save_movie.stop()
        self.save_animation.setHidden(True)
        self.save_error.setText("Saved Successfully  !!!")
        self.save_error.setHidden(False)
        r = Timer(3.0, lambda: self.save_error.setHidden(True))
        r.start()

    def savePdf(self):

        name = self.name_lineEdit.text()
        age = self.age_spinBox.value()
        phone = self.phone_lineEdit.text()

        self.save_error.setStyleSheet("color: red")

        if name == "":
            self.save_error.setText("Please enter patient name")
            self.save_error.setHidden(False)
            r = Timer(3.0, lambda: self.save_error.setHidden(True))
            r.start()
            return
        elif age == 0:
            self.save_error.setText("Please enter patient age")
            self.save_error.setHidden(False)
            r = Timer(3.0, lambda: self.save_error.setHidden(True))
            r.start()
            return
        elif phone == "":
            self.save_error.setText("Please enter patient phone number")
            self.save_error.setHidden(False)
            r = Timer(3.0, lambda: self.save_error.setHidden(True))
            r.start()
            return

        context = {'name': name, 'age': age, 'phone': phone}

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 10, 'CPN Detector Result', 0, 0, 'C')

        pdf.image(self.fname[0], x=55, y=32.5, w=100, h=100, type='', link='')

        pdf.set_font('Arial', '', 16)
        pdf.set_y(150)
        pdf.set_left_margin(55)
        pdf.cell(95, 10, 'Patient Name : ' + name, 0, 0, 'L')
        pdf.set_y(160)
        pdf.cell(95, 10, 'Age : ' + str(age), 0, 0, 'L')
        pdf.set_y(170)
        pdf.cell(95, 10, 'Phone number : (+91) ' + phone, 0, 0, 'L')

        pdf.set_y(190)
        pdf.cell(95, 10, 'Covid-19 : ' + self.covid_value.text(), 0, 0, 'L')
        pdf.set_y(200)
        pdf.cell(95, 10, 'Pneumonia : ' +
                 self.pneumonia_value.text(), 0, 0, 'L')
        pdf.set_y(210)
        pdf.cell(95, 10, 'Normal : ' + self.normal_value.text(), 0, 0, 'L')

        pdf.set_y(230)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(95, 10, 'Most probable disease : ' +
                 self.predict_result, 0, 0, 'L')

        pdf.output(name + '.pdf', 'F')

        self.save_animation.setHidden(False)
        self.save_movie.start()
        t1 = Thread(target=self.thread_savePdf)
        t1.start()

    def predict(self):
        self.predict_movie.start()
        self.predict_anim.setHidden(False)

        self.worker1 = Worker()
        self.worker_thread1 = QThread()

        # # self.worker.progress.connect(self.update_progress)
        self.worker1.completed.connect(self.show_predict_animation)

        self.work_requested.connect(
            self.worker1.worker_predict_diseases)

        # # move worker to the worker thread
        self.worker1.moveToThread(self.worker_thread1)

        # # start the thread
        self.worker_thread1.start()
        self.work_requested.emit(1)

    def show_predict_animation(self):
        prediction = ['Covid-19', 'Normal', 'Pneumonia']
        y_pred = globalvar.y_pred

        self.covid_value.setText(
            str(float("{:.2f}".format(y_pred[0][0]*100))) + '%')
        self.pneumonia_value.setText(
            str(float("{:.2f}".format(y_pred[0][2]*100))) + '%')
        self.normal_value.setText(
            str(float("{:.2f}".format(y_pred[0][1]*100))) + '%')

        max_pred = np.argmax(y_pred, axis=1)
        self.predict_result = prediction[max_pred[0]]

        self.predict_anim.setHidden(True)
        self.predict_movie.stop()

        self.animation = QPropertyAnimation(
            self.result_cpn_widget, b"geometry")
        self.animation.setDuration(700)
        self.animation.setStartValue(QtCore.QRect(1091, 45, 451, 700))
        self.animation.setEndValue(QtCore.QRect(610, 45, 451, 700))
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def close_result_cpn(self):
        self.animation = QPropertyAnimation(
            self.result_cpn_widget, b"geometry")
        self.animation.setDuration(700)
        self.animation.setStartValue(QtCore.QRect(610, 45, 451, 700))
        self.animation.setEndValue(QtCore.QRect(1091, 45, 451, 700))
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
