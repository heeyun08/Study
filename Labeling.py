import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Canvas(QLabel):
    def __init__(self, size):
        super().__init__()
        self.initUI()

    def initUI(self):
        dirbtn = QPushButton('디렉터리 선택', self)
        dirbtn.resize(100, 50)
        dirbtn.move(30, 650)
        dirbtn.setStyleSheet('background:white')
        #dirbtn.clicked.connect(self.BtnClickedPen)

        prebtn = QPushButton('<', self)
        prebtn.resize(100, 50)
        prebtn.move(670, 650)
        prebtn.setStyleSheet('background:white')
        #prebtn.clicked.connect(self.BtnClickedPen)

        nextbtn = QPushButton('>', self)
        nextbtn.resize(100, 50)
        nextbtn.move(770, 650)
        nextbtn.setStyleSheet('background:white')
        #nextbtn.clicked.connect(self.BtnClickedPen)

        dirlabel = QLabel('C:/CatAndDog', self)
        dirlabel.resize(500, 50)
        dirlabel.move(150, 650)
        dirlabel.setStyleSheet('background:white')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.Canvas = Canvas((900, 720))
        self.setFixedSize(900, 720)
        
        self.setCentralWidget(self.Canvas)
        self.setWindowTitle('Labeling program')
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    app.exec_()
