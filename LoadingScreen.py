import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        
        # self.lebel_animation = QtWidgets.QLabel(self)
        self.centralwidget = QtWidgets.QWidget(FrontWindow)
        self.centralwidget.setObjectName("main-widget")

        # Label Create
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(25, 25, 200, 200))
        self.label.setMinimumSize(QtCore.QSize(250, 250))
        self.label.setMaximumSize(QtCore.QSize(250, 250))
        self.label.setObjectName("lb1")
        FrontWindow.setCentralWidget(self.centralwidget)
        
        self.movie = QtGui.QMovie("loading.gif")
        self.label.setMovie(self.movie)
        
        timer = QtCore.QTimer(self)
        self.startAnimation()
        timer.singleShot(3000, self.stopAnimation)

        self.show()
        
    def startAnimation(self):
        self.movie.start()
        
    def stopAnimation(self):
        self.movie.stop()
        self.close()
