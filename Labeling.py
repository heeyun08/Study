import sys, os
import natsort  # 숫자 정렬용 라이브러리
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Canvas(QLabel):
    def __init__(self, size):
        super().__init__()

        self.initUI()

        self.cnt = 0                # 이미지 이동에 필요한 변수
        self.num = 0                # 레이블 구별 번호
        self.pixmap = QPixmap()
        self.begin = QPoint()
        self.color = Qt.black
        self.draw = False

    def initUI(self):
        # 이미지 판
        label = QLabel(self)
        label.resize(700, 600)
        label.move(30, 30)
        label.setStyleSheet('background:white; border-style:solid; border-width:2px; border-color:black')

        # 이미지 레이블
        self.ImgLabel = QLabel(self)
        self.ImgLabel.move(35, 35)
        self.ImgLabel.setCursor(Qt.CrossCursor)

        # 디렉터리 경로 표시 레이블
        self.dirlabel = QLabel(self)
        self.dirlabel.resize(510, 50)
        self.dirlabel.move(150, 650)
        self.dirlabel.setStyleSheet('background:white; border-style:solid; border-width:2px; border-color:black')

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
        self.dog = QRadioButton('Dog', self)
        self.dog.move(770, 40)
        self.dog.clicked.connect(self.Checked)
        
        dogcolor = QLabel(self)
        dogcolor.move(830, 40)
        dogcolor.resize(20,20)
        dogcolor.setStyleSheet('background:red')

        self.cat = QRadioButton('Cat', self)
        self.cat.move(770, 80)
        self.cat.clicked.connect(self.Checked)

        catcolor = QLabel(self)
        catcolor.move(830, 80)
        catcolor.resize(20,20)
        catcolor.setStyleSheet('background:blue')

    def mousePressEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.draw = True
            self.begin = e.pos() - QPoint(35, 35)
            self.ImgLabel.update()

        elif e.buttons() & Qt.RightButton:
            self.Delete()

    def mouseMoveEvent(self, e):
        pass

    def Box(self, e):
        if self.draw:
            t_pixmap = self.ImgLabel.pixmap()
            t_pixmap = t_pixmap.copy(0, 0, t_pixmap.width(), t_pixmap.height())
            painter = QPainter(self.ImgLabel.pixmap())
            painter.setPen(QPen(QColor(self.color), 5))
            painter.drawRect(QRect(self.begin, e.pos() - QPoint(35, 35)))
            painter.end()        
            self.ImgLabel.repaint()
            self.ImgLabel.setPixmap(t_pixmap)

    def mouseReleaseEvent(self, e):
        if self.draw:
            self.draw = False
            painter = QPainter(self.ImgLabel.pixmap())
            painter.setPen(QPen(QColor(self.color), 5))
            painter.setFont(QFont('Arial', 15))
            painter.drawRect(QRect(self.begin, e.pos() - QPoint(35, 35)))

            if self.num == 1:
                painter.drawText(self.begin.x(), self.begin.y() - 10, "Dog")
                painter.end()
                self.ImgLabel.repaint()

            elif self.num == 2:
                painter.drawText(self.begin.x(), self.begin.y() - 10, "Cat")
                painter.end()
                self.ImgLabel.repaint()

    # 디렉터리 선택
    def LoadDir(self):
        fpath = QFileDialog.getExistingDirectory(self, 'Open File', '', QFileDialog.ShowDirsOnly)

        if fpath:
            fileList = natsort.natsorted(os.listdir(fpath))
            self.pixmap = [QPixmap(fpath+'/'+img).scaled(690, 590) for img in fileList]
            self.pixmap[0] = self.pixmap[0].scaled(690,590)

            self.ImgLabel.setPixmap(self.pixmap[0])
            self.ImgLabel.resize(self.pixmap[0].width(), self.pixmap[0].height())

            self.show()

            # 디렉터리 경로 출력
            self.dirlabel.setText(fpath)

    # 바운딩 박스 삭제
    def Delete(self):
        pass

    # 저장
    def Save(self):
        pass

    # 이전 이미지로 이동
    def BtnClickedPre(self):
        try:
            self.Save()
            if self.cnt < 0:
                self.cnt = len(self.pixmap) - 1

            self.cnt -= 1
            self.ImgLabel.setPixmap(self.pixmap[self.cnt])
        except:
            pass

    # 다음 이미지로 이동
    def BtnClickedNext(self):
        try:
            self.Save()
            self.cnt += 1

            if self.cnt == len(self.pixmap):
                self.cnt = 0

            self.ImgLabel.setPixmap(self.pixmap[self.cnt])
        except:
            pass

    # radio 버튼 체크 이벤트 함수
    def Checked(self):
        sender = self.sender()
        if sender == self.dog:
            self.color = Qt.red
            self.num = 1
        elif sender == self.cat:
            self.color = Qt.blue
            self.num = 2

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
