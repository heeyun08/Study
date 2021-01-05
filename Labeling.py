import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Canvas(QLabel):
    def __init__(self, size):
        super().__init__()

        self.initUI()
        self.cnt = 0
        self.fPixmap = QPixmap()

        # 이미지 레이블
        self.ImgLabel = QLabel(self)
        self.ImgLabel.move(30, 30)

        # 디렉터리 경로 표시 레이블
        self.dirlabel = QLabel(self)
        self.dirlabel.resize(500, 50)
        self.dirlabel.move(150, 650)
        self.dirlabel.setStyleSheet('background:white')
        
    def initUI(self):
        # 버튼
        dirbtn = QPushButton('디렉터리 선택', self)
        dirbtn.resize(110, 50)
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

        # 레이블
        dog = QRadioButton('Dog', self)
        dog.move(800, 30)
        dog.clicked.connect(self.DogChecked)

        dogcolor = QLabel(self)
        dogcolor.move(860, 30)
        dogcolor.resize(20,20)
        dogcolor.setStyleSheet('background:red')

        cat = QRadioButton('Cat', self)
        cat.move(800, 70)
        cat.clicked.connect(self.CatChecked)

        catcolor = QLabel(self)
        catcolor.move(860, 70)
        catcolor.resize(20,20)
        catcolor.setStyleSheet('background:blue')

    # 디렉터리 선택
    def LoadDir(self):
        fpath = QFileDialog.getExistingDirectory(self, 'Open File', '', QFileDialog.ShowDirsOnly)

        if fpath:
            pixmap = [QPixmap(fpath+'/'+img).scaled(700, 600) for img in os.listdir(fpath)]
            pixmap[0] = pixmap[0].scaled(700,600)
            self.fPixmap = pixmap

            self.ImgLabel.setPixmap(pixmap[0])
            self.ImgLabel.resize(pixmap[0].width(), pixmap[0].height())

            self.show()

            # 디렉터리 경로 출력
            self.dirlabel.setText(fpath)

    def BtnClickedPre(self):
        pass

    def BtnClickedNext(self):
        self.cnt += 1

        # 이미지 로드 하지 않고 누르면 오류남
        if self.cnt == len(self.fPixmap):
            self.cnt = 0

        self.ImgLabel.setPixmap(self.fPixmap[self.cnt])

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
