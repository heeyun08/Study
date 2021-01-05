import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Canvas(QLabel):
    def __init__(self, size):
        super().__init__()

        self.initUI()

        self.ImgLabel = QLabel(self)
        self.ImgLabel.move(30, 30)

        self.dirlabel = QLabel(self)
        self.dirlabel.resize(500, 50)
        self.dirlabel.move(150, 650)
        self.dirlabel.setStyleSheet('background:white')
        
    def initUI(self):
        dirbtn = QPushButton('디렉터리 선택', self)
        dirbtn.resize(100, 50)
        dirbtn.move(30, 650)
        dirbtn.setStyleSheet('background:white')
        dirbtn.clicked.connect(self.LoadDir)

        prebtn = QPushButton('<', self)
        prebtn.resize(100, 50)
        prebtn.move(670, 650)
        prebtn.setStyleSheet('background:white')
        prebtn.clicked.connect(self.BtnClickedPre)

        nextbtn = QPushButton('>', self)
        nextbtn.resize(100, 50)
        nextbtn.move(770, 650)
        nextbtn.setStyleSheet('background:white')
        nextbtn.clicked.connect(self.BtnClickedNext)

        dog = QRadioButton('Dog', self)
        dog.move(800, 30)
        dog.clicked.connect(self.DogChecked)

        cat = QRadioButton('Cat', self)
        cat.move(800, 60)
        cat.clicked.connect(self.CatChecked)

    def LoadDir(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open File', '', QFileDialog.ShowDirsOnly)
        
        if fname:
            pixmap = QPixmap(fname)
            pixmap = pixmap.scaled(700, 600)

            self.ImgLabel.setPixmap(pixmap)
            self.ImgLabel.resize(pixmap.width(), pixmap.height())

            self.show()

            self.dirlabel.setText(fname)

    def BtnClickedPre(self):
        pass

    def BtnClickedNext(self):
        pass

    def DogChecked(self):
        pass

    def CatChecked(slef):
        pass

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
