from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QPushButton,QLineEdit
from PyQt5.QtWidgets import (QGridLayout, QLabel)
import sys
import sqlite3
from PyQt5.QtWidgets import *
from PySide2.QtWidgets import QApplication
from collections import Counter

con = sqlite3.connect("sytech korea.db")
cur = con.cursor()

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()


    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(QLabel('제품명:'))
        grid.addWidget(QLabel('제품번호:'))
        grid.addWidget(QLabel('출고가격:'))
        grid.addWidget(QLabel('수익률:'))
        grid.addWidget(QLabel('회사명:'))
        grid.addWidget(QLabel('카테고리:'))
        self.btn1 = QPushButton('저장', self)
        self.btn1.resize(50,70)
        self.btn1.move(10, 170)
        self.btn1.setCheckable(True)
        self.btn1.clicked.connect(self.butten)

        self.btn2 = QPushButton('제품명\n검색', self)
        self.btn2.resize(50,70)
        self.btn2.move(10, 250)
        self.btn2.setCheckable(True)
        self.btn2.clicked.connect(self.butten2)

        self.btn4 = QPushButton('회사명\n검색', self)
        self.btn4.resize(50,70)
        self.btn4.move(10, 330)
        self.btn4.setCheckable(True)
        self.btn4.clicked.connect(self.butten4)

        self.btn3 = QPushButton('카테\n고리\n검색', self)
        self.btn3.resize(50,70)
        self.btn3.move(10, 410)
        self.btn3.setCheckable(True)
        self.btn3.clicked.connect(self.butten3)

        self.le1 = QLineEdit(self)
        grid.addWidget(self.le1, 0,1)
        self.le1.textChanged[str].connect(self.click)

        self.le2 = QLineEdit(self)
        grid.addWidget(self.le2, 1,1)
        self.le2.textChanged[str].connect(self.click2)

        self.le3 = QLineEdit(self)
        grid.addWidget(self.le3, 2,1)
        self.le3.textChanged[str].connect(self.click3)

        self.le4 = QLineEdit(self)
        grid.addWidget(self.le4, 3,1)
        self.le4.textChanged[str].connect(self.click4)

        self.le5 = QLineEdit(self)
        grid.addWidget(self.le5, 4,1)
        self.le5.textChanged[str].connect(self.click5)

        allWords = ['모터', '탱크']
        self.le6 = QLineEdit(self)
        words = Counter(allWords).most_common()
        recommended_words = []
        for i in words:
            recommended_words.append(i[0])
        completer = QCompleter(recommended_words)
        self.le6.setCompleter(completer)
        grid.addWidget(self.le6, 5,1)
        self.le6.textChanged[str].connect(self.click6)

        self.lw = QTableWidget(self)
        grid.addWidget(self.lw, 6,1)
        self.lw.setRowCount(1000000)
        self.lw.setColumnCount(6)
        self.setTableWidgetData()

        self.setWindowTitle('SY TECH KOREA')
        self.setWindowIcon(QIcon('img.png'))
        self.resize(760, 600)
        self.center()
        self.show()

    def setTableWidgetData(self):
        column_headers = ['제품명', '제품번호', '출고가격', '수익율', '회사명','카테고리']
        self.lw.setHorizontalHeaderLabels(column_headers)
        self.lw.setItem(0, 0, QTableWidgetItem("Base Data"))
        self.lw.setItem(0, 1, QTableWidgetItem("Base Data"))

    def change_text(self, txt):
        self.label.setText(txt)
        self.label.adjustSize()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def click(self, le1):
        self.le1 = le1

    def click2(self, le2):
        self.le2 = le2

    def click3(self, le3):
        self.le3 = le3

    def click4(self, le4):
        self.le4 = le4

    def click5(self, le5):
        self.le5 = le5

    def click6(self, le6):
        self.le6 = le6


    def butten(self):
        try:
            cur = con.cursor()
            cur.execute('''INSERT INTO stocks VALUES (:Name, :Number, :Price, :text, :Company, :Category)''',
                    {"Name": self.le1, "Number": self.le2, "Price": self.le3, "text": self.le4, "Company": self.le5, "Category": self.le6})
            con.commit()
            with con:
                with open('SYTECH KOREA BackUpFILE.sql', 'w') as f:
                    for line in con.iterdump():
                        f.write('%s\n' % line)
                    print('Save Completed')
            self.btn1.toggle()
        except:
            self.btn1.toggle()
            pass

    def butten2(self):
        try:
            cur = con.cursor()
            cur.execute("select Name,Number,Price,text,Company,Category from stocks where Name Like ?", (self.le1,))
            self.full = cur.fetchall()

            for i in range(len(self.full)):
                self.full2 = self.full[i]
                for j in range(len(self.full2)):
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
            self.btn2.toggle()
        except:
            self.btn2.toggle()
            pass


    def butten3(self):
        try:
            cur = con.cursor()
            cur.execute("select Name,Number,Price,text,Company,Category from stocks where Category Like ?", (self.le6,))
            self.full = cur.fetchall()
            for i in range(len(self.full)):
                self.full2 = self.full[i]
                for j in range(len(self.full2)):
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
            self.btn3.toggle()
        except:
            self.btn3.toggle()
            pass

    def butten4(self):
        try:
            cur = con.cursor()
            cur.execute("select Name,Number,Price,text,Company,Category from stocks where Company Like ?", (self.le5,))
            self.full = cur.fetchall()
            for i in range(len(self.full)):
                self.full2 = self.full[i]
                for j in range(len(self.full2)):
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
                    self.lw.setItem(i, j, QTableWidgetItem(self.full2[j]))
            self.btn4.toggle()
        except:
            self.btn4.toggle()
            pass

    def ErrorBox(self, title, message):
        ERBOX = QMessageBox(self)
        ERBOX.question(self, title, message, QMessageBox.Ok)

    def box(self):
        self.ErrorBox(title='Error', message='다시한번 확인해주세요.')

    def closeEvent(self, event):
        self.deleteLater()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())