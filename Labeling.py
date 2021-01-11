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
        self.num = 0                # 레이블 구별 번호
        self.pixmap = QPixmap()
        self.begin = QPoint()
        self.color = Qt.black
        self.draw = False
        self.list = []
        self.fileList = []
        self.fileList2 = []
        self.fname = ''

    def initUI(self):

        # 이미지 레이블
        self.ImgLabel = QLabel(self)
        self.ImgLabel.setGeometry(0, 0, 850, 600)
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
        self.dog.move(1100, 40)
        self.dog.setStyleSheet('color:red')
        self.dog.clicked.connect(self.Checked)

        self.cat = QRadioButton('Cat', self)
        self.cat.move(1100, 80)
        self.cat.setStyleSheet('color:blue')
        self.cat.clicked.connect(self.Checked)

    def mousePressEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.draw = True
            self.begin = e.pos()
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
            painter.setPen(QPen(QColor(self.color), 1))
            painter.drawRect(QRect(self.begin, e.pos()))
            painter.end()        
            self.ImgLabel.repaint()
            self.ImgLabel.setPixmap(t_pixmap)

    def mouseReleaseEvent(self, e):
        if self.draw:
            self.draw = False
            painter = QPainter(self.ImgLabel.pixmap())
            painter.setPen(QPen(QColor(self.color), 1))
            painter.setFont(QFont('Arial', 15))
            painter.drawRect(QRect(self.begin, e.pos()))
            
            # 바운딩 박스 좌표 list에 저장
            left_x, top_y = str(self.begin.x()), str(self.begin.y())
            right_x, bottom_y = e.x() - 35, e.y() - 35
            right_x, bottom_y = str(right_x), str(bottom_y)

            if self.num == 1:
                painter.drawText(self.begin.x(), self.begin.y(), "Dog")
                self.list.append([left_x, top_y, right_x, bottom_y, 'Dog'])

            elif self.num == 2:
                painter.drawText(self.begin.x(), self.begin.y(), "Cat")
                self.list.append([left_x, top_y, right_x, bottom_y, 'Cat'])

            painter.end()
            self.ImgLabel.repaint()

    # 디렉터리 선택
    def LoadDir(self):
        fpath = QFileDialog.getExistingDirectory(self, 'Open File', '', QFileDialog.ShowDirsOnly)
        self.fname = fpath

        if fpath:
            self.fileList = natsort.natsorted(os.listdir(fpath))
            for i in self.fileList:
                if 'txt' in i:
                    self.fileList.remove(i)
            self.fileList2 = os.listdir(fpath)

            self.pixmap = QPixmap(self.ImgLabel.width(), self.ImgLabel.height())
            self.pixmap.load("{0}/{1}".format(fpath, self.fileList[0]))

            self.ImgLabel.setPixmap(self.pixmap)
            self.ImgLabel.resize(self.pixmap.width(), self.pixmap.height())
           
            if self.fileList[self.cnt].split('.')[0] + '.txt' in self.fileList2:
                self.LoadBounding(self.fileList[self.cnt].split('.')[0])

            self.show()

            # 디렉터리 경로 출력
            self.dirlabel.setText(fpath)

    # 바운딩 박스, 레이블 삭제
    def Delete(self):
        pass

    # 바운딩 박스, 레이블 저장
    def Save(self):
        if len(self.list) > 0:
            Imgname = self.fileList[self.cnt]
            Imgname = Imgname.split('.')
            # Imgname = os.path.split(fname)
            f = open("{0}/{1}.txt".format(self.fname, Imgname[0]), 'w')

            for i in self.list:
                tmp = ','.join(i)
                f.write(tmp + '\n')

            f.close()
            self.list = [] # crdntList 초기화

    # 바운딩 박스, 레이블 로드
    def LoadBounding(self, txtname):
        list2 = []
        f = open("{0}/{1}.txt".format(self.fname, txtname), 'r')
        txt = f.read().split('\n')
        txt.pop() # 마지막 공백 삭제
        for i in range(len(txt)):
            list1 = str(txt[i]).split(',')
            list2.append(list1)
        painter = QPainter(self.ImgLabel.pixmap())
        painter.setFont(QFont('Arial', 15))
        for i in range(len(list2)):
            if list2[i][4] == "Dog":
                painter.setPen(QPen(QColor(Qt.red), 1))
                painter.drawText(int(list2[i][0]), int(list2[i][1]), 'Dog')
            else:
                painter.setPen(QPen(QColor(Qt.blue), 1))
                painter.drawText(int(list2[i][0]), int(list2[i][1]), 'Cat')

            painter.drawRect(QRect(int(list2[i][0]), int (list2[i][1]),
                                    int(list2[i][2]) - int(list2[i][0]),
                                    int(list2[i][3]) - int(list2[i][1])))
        self.ImgLabel.repaint()
        f.close()

    # 이전 이미지로 이동
    def BtnClickedPre(self):
        try:
            self.Save()
            self.cnt -= 1
            if self.cnt < 0:
                self.cnt = 0
            else:
                self.fileList2 = os.listdir(self.fname)
                self.pixmap.load("{0}/{1}".format(self.fname, self.fileList[self.cnt]))
                self.ImgLabel.setPixmap(self.pixmap)
                self.ImgLabel.resize(self.pixmap.width(), self.pixmap.height())
                if self.fileList[self.cnt].split('.')[0] + '.txt' in self.fileList2:
                    self.LoadBounding(self.fileList[self.cnt].split('.')[0])
        except:
            pass

    # 다음 이미지로 이동
    def BtnClickedNext(self):
        try:
            self.Save()
            self.cnt += 1

            if self.cnt == len(self.fileList):
                self.cnt -= 1
            else:
                self.fileList2 = os.listdir(self.fname)
                self.pixmap.load("{0}/{1}".format(self.fname, self.fileList[self.cnt]))
                self.ImgLabel.setPixmap(self.pixmap)
                self.ImgLabel.resize(self.pixmap.width(), self.pixmap.height())
                if self.fileList[self.cnt].split('.')[0] + '.txt' in self.fileList2:
                    self.LoadBounding(self.fileList[self.cnt].split('.')[0])
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
        
        self.Canvas = Canvas((1200, 720))
        self.setFixedSize(1200, 720)
        
        self.setCentralWidget(self.Canvas)
        self.setWindowTitle('Labeling program')
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    app.exec_()
