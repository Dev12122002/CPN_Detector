from loginUi import *
from RegisterUi import *
from HomeUi import *
from PyQt5 import QtCore, QtGui, QtWidgets
import globalvar

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
        # self.ui.switch_window.connect(registerVar)
        self.home.show()

cnt = Controller()
loginVar = cnt.show_Register
registerVar = cnt.show_login
globalvar.initialize()

def main():
    app = QtWidgets.QApplication(sys.argv)
    # controller = Controller()
    cnt.show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
