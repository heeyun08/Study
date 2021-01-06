import sys, os
import natsort # 숫자 정렬용 라이브러리
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Canvas(QLabel):
    def __init__(self, size):
        super().__init__()

        self.initUI()

        self.begin = QPoint()
        self.labelSize = QSize(50, 30)
        self.color = Qt.black
        self.count = 0

        # 이미지 이동에 필요한 변수
        self.cnt = 0
        self.fPixmap = QPixmap()

        # 이미지 레이블
        self.ImgLabel = QLabel(self)
        self.ImgLabel.move(35, 35)

        # 디렉터리 경로 표시 레이블
        self.dirlabel = QLabel(self)
        self.dirlabel.resize(510, 50)
        self.dirlabel.move(150, 650)
        self.dirlabel.setStyleSheet('background:white; border-style:solid; border-width:2px; border-color:black')

        # 레이블 이름
        self.dogLabel = QLabel('Dog', self.ImgLabel)
        self.dogLabel.setFont(QFont('Arial', 14))
        self.dogLabel.setStyleSheet('Color:red')
        self.dogLabel.resize(0, 0)
        self.dogLabel.move(50, 50)

        self.catLabel = QLabel('Cat', self.ImgLabel)
        self.catLabel.setFont(QFont('Arial', 14))
        self.catLabel.setStyleSheet('Color:blue')
        self.catLabel.resize(0, 0)
        self.catLabel.move(50, 50)

    def initUI(self):
        label = QLabel(self)
        label.resize(700, 600)
        label.move(30, 30)
        label.setStyleSheet('background:white; border-style:solid; border-width:2px; border-color:black')

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
        prebtn.setShortcut('LEFT')

        nextbtn = QPushButton('>', self)
        nextbtn.resize(100, 50)
        nextbtn.move(770, 650)
        nextbtn.setStyleSheet('background:white')
        nextbtn.clicked.connect(self.BtnClickedNext)
        nextbtn.setShortcut('RIGHT')

        # 레이블
        dog = QRadioButton('Dog', self)
        dog.move(770, 40)
        dog.clicked.connect(self.DogChecked)
        
        dogcolor = QLabel(self)
        dogcolor.move(830, 40)
        dogcolor.resize(20,20)
        dogcolor.setStyleSheet('background:red')

        cat = QRadioButton('Cat', self)
        cat.move(770, 80)
        cat.clicked.connect(self.CatChecked)

        catcolor = QLabel(self)
        catcolor.move(830, 80)
        catcolor.resize(20,20)
        catcolor.setStyleSheet('background:blue')

    def mouseButtonKind(self, buttons):
        if buttons & Qt.RightButton:
            pass

    def mousePressEvent(self, e):
        self.begin = e.pos() - QPoint(35, 35)

        if self.count == 1:
            self.dogLabel.setGeometry(QRect(self.begin - QPoint(0, 35), self.labelSize))
        
        elif self.count == 2:
            self.catLabel.setGeometry(QRect(self.begin - QPoint(0, 35), self.labelSize))
            
        self.ImgLabel.update()

    def mouseMoveEvent(self, e):
        pass

    def Box(self, e):
        t_pixmap = self.ImgLabel.pixmap()
        t_pixmap = t_pixmap.copy(0, 0, t_pixmap.width(), t_pixmap.height())
        painter = QPainter(self.ImgLabel.pixmap())
        painter.setPen(QPen(QColor(self.color), 5))
        painter.drawRect(QRect(self.begin, e.pos() - QPoint(35, 35)))
        painter.end()        
        self.ImgLabel.repaint()
        self.ImgLabel.setPixmap(t_pixmap)

    def mouseReleaseEvent(self, e):
        if self.count == 1:
            Dog = QPainter(self.ImgLabel.pixmap())
            Dog.setPen(QPen(QColor(self.color), 5))
            Dog.drawRect(QRect(self.begin, e.pos() - QPoint(35, 35)))
            Dog.end()            
            self.ImgLabel.repaint()

        elif self.count == 2:
            Cat = QPainter(self.ImgLabel.pixmap())
            Cat.setPen(QPen(QColor(self.color), 5))
            Cat.drawRect(QRect(self.begin, e.pos() - QPoint(35, 35)))
            Cat.end()
            self.ImgLabel.repaint()

    # 디렉터리 선택
    def LoadDir(self):
        fpath = QFileDialog.getExistingDirectory(self, 'Open File', '', QFileDialog.ShowDirsOnly)

        if fpath:
            fileList = natsort.natsorted(os.listdir(fpath))
            pixmap = [QPixmap(fpath+'/'+img).scaled(690, 590) for img in fileList]
            pixmap[0] = pixmap[0].scaled(690,590)
            self.fPixmap = pixmap

            self.ImgLabel.setPixmap(pixmap[0])
            self.ImgLabel.resize(pixmap[0].width(), pixmap[0].height())

            self.show()

            # 디렉터리 경로 출력
            self.dirlabel.setText(fpath)

    # 저장
    def Save(self):
        pass

    # 이전 이미지로 이동
    def BtnClickedPre(self):
        try:
            if self.cnt < 0:
                self.cnt = len(self.fPixmap) - 1

            self.cnt -= 1

            self.ImgLabel.setPixmap(self.fPixmap[self.cnt])
        except:
            pass

    # 다음 이미지로 이동
    def BtnClickedNext(self):
        try:
            self.cnt += 1

            if self.cnt == len(self.fPixmap):
                self.cnt = 0

            self.ImgLabel.setPixmap(self.fPixmap[self.cnt])
        except:
            pass

    def DogChecked(self):
        self.color = Qt.red
        self.count = 1

        self.mouseMoveEvent = self.Box

    def CatChecked(self):
        self.color = Qt.blue
        self.count = 2

        self.mouseMoveEvent = self.Box

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
