import sys, os
import natsort  # 숫자 정렬용 라이브러리
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Canvas(QLabel):
    def __init__(self, size):
        super().__init__()

        self.initVar()
        self.initUI()
        
    def initVar(self):
        self.cnt = 0                # 이미지 이동에 필요한 변수
        self.type = 0               # 레이블 구별 번호
        self.pixmap = None
        self.begin = QPoint()
        self.color = Qt.black
        self.draw = False
        self.list = []
        self.imageList = []
        self.fileList = []
        self.fname = ''

    def initUI(self):
        # 이미지 레이블
        self.ImgLabel = QLabel(self)
        self.ImgLabel.setGeometry(0, 0, 1280, 720)

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
        self.dog.move(1100, 40)
        self.dog.setStyleSheet('color:red')
        self.dog.clicked.connect(self.Checked)

        self.cat = QRadioButton('Cat', self)
        self.cat.move(1100, 80)
        self.cat.setStyleSheet('color:blue')
        self.cat.clicked.connect(self.Checked)

    def mousePressEvent(self, e):
        if self.pixmap != None:
            if e.buttons() & Qt.LeftButton:
                self.draw = True
                self.begin = e.pos()
                self.ImgLabel.update()
            elif e.buttons() & Qt.RightButton:
                self.draw = False
                self.Delete(e.x(), e.y())

    def mouseMoveEvent(self, e):
        pass

    def Box(self, e):
        if self.draw:
            t_pixmap = self.ImgLabel.pixmap()
            t_pixmap = t_pixmap.copy(0, 0, t_pixmap.width(), t_pixmap.height())
            painter = QPainter(self.ImgLabel.pixmap())
            painter.setPen(QPen(QColor(self.color), 2))
            painter.drawRect(QRect(self.begin, e.pos()))
            painter.end()        
            self.ImgLabel.repaint()
            self.ImgLabel.setPixmap(t_pixmap)

    def mouseReleaseEvent(self, e):
        if self.draw & (self.color != Qt.black):
            self.draw = False
            painter = QPainter(self.ImgLabel.pixmap())
            painter.setPen(QPen(QColor(self.color), 2))
            painter.setFont(QFont('Arial', 15))
            painter.drawRect(QRect(self.begin, e.pos()))
            
            # 바운딩 박스 좌표 list에 저장
            left_x, top_y = str(self.begin.x()), str(self.begin.y())
            right_x, bottom_y = str(e.x()), str(e.y())

            if self.type == 1:
                painter.drawText(self.begin.x(), self.begin.y(), "Dog")
                self.list.append([left_x, top_y, right_x, bottom_y, 'Dog'])

            elif self.type == 2:
                painter.drawText(self.begin.x(), self.begin.y(), "Cat")
                self.list.append([left_x, top_y, right_x, bottom_y, 'Cat'])
            painter.end()
            self.Save()
            self.ImgLabel.repaint()

    # 디렉터리 선택
    def LoadDir(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'Open File', '', QFileDialog.ShowDirsOnly)

        if self.fname:
            self.imageList = natsort.natsorted(os.listdir(self.fname))
            self.fileList = natsort.natsorted(os.listdir(self.fname))
            for i in self.imageList:
                if 'txt' in i:
                    self.imageList.remove(i)

            self.pixmap = QPixmap(self.ImgLabel.width(), self.ImgLabel.height())
            self.pixmap.load("{0}/{1}".format(self.fname, self.imageList[0]))

            self.ImgLabel.setPixmap(self.pixmap)
            self.ImgLabel.setCursor(Qt.CrossCursor)
            self.ImgLabel.resize(self.pixmap.width(), self.pixmap.height())
            
            if self.imageList[self.cnt].split('.')[0] + '.txt' in self.fileList:
                self.LoadBounding(self.imageList[self.cnt].split('.')[0])

            self.show()
            self.dirlabel.setText(self.fname)   # 디렉터리 경로 출력

    # 바운딩 박스, 레이블 저장
    def Save(self):
        if len(self.list) > 0:
            Imgname = self.imageList[self.cnt]
            Imgname = Imgname.split('.')
            f = open("{0}/{1}.txt".format(self.fname, Imgname[0]), 'a')
            
            for i in self.list:
                tmp = ','.join(i)
                f.write(tmp + '\n')
            f.close()

            self.list = [] # list 초기화

    # 바운딩 박스, 레이블 로드
    def LoadBounding(self, txtname):
        list2 = []
        f = open("{0}/{1}.txt".format(self.fname, txtname), 'r')
        info = f.read().split('\n')
        info.pop() # 마지막 공백 삭제
        for i in range(len(info)):
            list1 = str(info[i]).split(',')
            list2.append(list1)
        painter = QPainter(self.ImgLabel.pixmap())
        painter.setFont(QFont('Arial', 15))
        for i in range(len(list2)):
            if list2[i][4] == "Dog":
                painter.setPen(QPen(QColor(Qt.red), 2))
                painter.drawText(int(list2[i][0]), int(list2[i][1]), 'Dog')
            elif list2[i][4] == "Cat":
                painter.setPen(QPen(QColor(Qt.blue), 2))
                painter.drawText(int(list2[i][0]), int(list2[i][1]), 'Cat')

            painter.drawRect(QRect(int(list2[i][0]), int (list2[i][1]),
                                    int(list2[i][2]) - int(list2[i][0]),
                                    int(list2[i][3]) - int(list2[i][1])))
        self.ImgLabel.repaint()
        f.close()

    # 바운딩 박스, 레이블 삭제
    def Delete(self, x, y):
        list2 = []
        list3 = []
        txtname = self.imageList[self.cnt].split('.')[0]
        fr = open(f"{self.fname}/{txtname}.txt", 'r')
        info = fr.read().split('\n')
        info.pop()
        for i in range(len(info)):
            list1 = str(info[i]).split(',')
            list2.append(list1)
        fr.close()

        fw = open(f"{self.fname}/{txtname}.txt", 'w')
        for i in range(len(list2)):
            list3.append(list2[i])
        for i in range(len(list2)):
            a, b, c, d = int(list2[i][0]), int(list2[i][2]), int(list2[i][1]), int(list2[i][3])
            if a <= x <= b and c <= y <= d:
                delinfo = list2[i]
                list3.remove(delinfo)
        for i in list3:
                tmp = ','.join(i)
                fw.write(tmp + '\n')
        fw.close()

        self.pixmap.load("{0}/{1}".format(self.fname, self.imageList[self.cnt]))
        self.ImgLabel.setPixmap(self.pixmap)
        self.ImgLabel.resize(self.pixmap.width(), self.pixmap.height())
        if txtname + '.txt' in self.fileList:
            self.LoadBounding(txtname)

    # 이전 이미지로 이동
    def BtnClickedPre(self):
        try:
            self.Save()
            self.cnt -= 1
            if self.cnt < 0:
                self.cnt = 0
            else:
                self.pixmap.load("{0}/{1}".format(self.fname, self.imageList[self.cnt]))
                self.ImgLabel.setPixmap(self.pixmap)
                self.ImgLabel.resize(self.pixmap.width(), self.pixmap.height())
                if self.imageList[self.cnt].split('.')[0] + '.txt' in self.fileList:
                    self.LoadBounding(self.imageList[self.cnt].split('.')[0])
        except:
            pass

    # 다음 이미지로 이동
    def BtnClickedNext(self):
        try:
            self.Save()
            self.cnt += 1
            if self.cnt == len(self.imageList):
                self.cnt -= 1
            else:
                self.pixmap.load("{0}/{1}".format(self.fname, self.imageList[self.cnt]))
                self.ImgLabel.setPixmap(self.pixmap)
                self.ImgLabel.resize(self.pixmap.width(), self.pixmap.height())
                if self.imageList[self.cnt].split('.')[0] + '.txt' in self.fileList:
                    self.LoadBounding(self.imageList[self.cnt].split('.')[0])
        except:
            pass

    # radio 버튼 체크 이벤트 함수
    def Checked(self):
        if self.dog.isChecked():
            self.color = Qt.red
            self.type = 1
        elif self.cat.isChecked():
            self.color = Qt.blue
            self.type = 2

        self.mouseMoveEvent = self.Box

    def close(self):
        self.Save()
        super().close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.Canvas = Canvas((1200, 720))
        self.setFixedSize(1200, 720)
        
        self.setCentralWidget(self.Canvas)
        self.setWindowTitle('Labeling program')
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    app.exec_()
