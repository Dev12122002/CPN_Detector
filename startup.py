from loginUi import *
from RegisterUi import *
from HomeUi import *
from PyQt5 import QtCore, QtGui, QtWidgets
import globalvar
from config import Config


class Controller:

    def __init__(self):
        self.flag = 0
        pass

    def show_login(self):
        if globalvar.ismain == True:
            self.register.close()
            globalvar.ismain = False
            self.show_Home()
            return

        if self.flag == 1:
            self.register.close()
            self.flag = 0

        if globalvar.isloggedin == 1:
            self.home.close()
            globalvar.isloggedin = 0
            globalvar.email = ''

        self.login = QtWidgets.QWidget()
        self.ui = Login()
        self.ui.setupUi(self.login)
        self.ui.switch_window.connect(loginVar)
        self.login.show()

    def show_Register(self):
        if globalvar.ismain == True:
            self.login.close()
            globalvar.ismain = False
            self.show_Home()
            return

        self.flag = 1
        self.login.close()
        self.register = QtWidgets.QWidget()
        self.ui = Register()
        self.ui.setupUi(self.register)
        self.ui.switch_window.connect(registerVar)
        self.register.show()

    def show_Home(self):
        self.home = QtWidgets.QWidget()
        self.ui = Home()
        self.ui.setupUi(self.home)
        self.ui.switch_window.connect(self.show_login)

        with open("style.qss", "r") as f:
            self.home.setStyleSheet(f.read())

            self.home.setStyleSheet("""
                border-radius: 20px;
                opacity: 100;
                border: 2px solid #ff2025;
            """)

        self.home.show()


cnt = Controller()
loginVar = cnt.show_Register
registerVar = cnt.show_login
globalvar.initialize()


def main():
    app = QtWidgets.QApplication(sys.argv)
    settings = QtCore.QSettings('CPN-Detector', 'CPN-Detector')
    # print(settings.fileName())

    globalvar.logged_user()

    if settings.contains("loggedin") and settings.contains("email"):
        globalvar.isloggedin = settings.value("loggedin")
        globalvar.email = settings.value("email")
        # print("key is there")
        config = Config()
        config.fetch_pdf()
        if settings.value("loggedin") == 1:
            # print("Logged in")
            globalvar.ismain = False
            cnt.show_Home()
        else:
            cnt.show_login()
    else:
        settings.setValue('loggedin', 0)
        settings.setValue('email', '')
        globalvar.isloggedin = settings.value("loggedin")
        globalvar.email = settings.value("email")
        config = Config()
        config.fetch_pdf()
        cnt.show_login()

    keys = settings.allKeys()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
