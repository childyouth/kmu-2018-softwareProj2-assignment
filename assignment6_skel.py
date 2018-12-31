import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit, QSizePolicy)
from PyQt5.QtCore import Qt


class Button(QPushButton):
    def __init__(self, text, callback):
        super().__init__()
        self.setText(text)
        self.clicked.connect(callback)

class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()

    def initUI(self):
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Assignment6')

        self.lineedit_name = QLineEdit()
        self.lineedit_age = QLineEdit()
        self.lineedit_score = QLineEdit()
        self.lineedit_amount = QLineEdit()
        self.cb_key = QComboBox()

        self.cb_key.addItem("Name")
        self.cb_key.addItem("Age")
        self.cb_key.addItem("Score")

        inputbox = QHBoxLayout()
        inputbox.addStretch(1)
        inputbox.addWidget(QLabel("Name"))
        inputbox.addWidget(self.lineedit_name)
        inputbox.addWidget(QLabel("Age"))
        inputbox.addWidget(self.lineedit_age)
        inputbox.addWidget(QLabel("Score"))
        inputbox.addWidget(self.lineedit_score)
        inputbox.addWidget(QLabel("Amount"))
        inputbox.addWidget(self.lineedit_amount)
        inputbox.addWidget(QLabel("Key"))
        inputbox.addWidget(self.cb_key)

        self.btn_add = Button("Add",self.buttonClicked)
        self.btn_del = Button("Del",self.buttonClicked)
        self.btn_find = Button("Find",self.buttonClicked)
        self.btn_inc = Button("Inc",self.buttonClicked)
        self.btn_show = Button("Show",self.buttonClicked)


        buttonbox = QHBoxLayout()
        buttonbox.addStretch(1)
        buttonbox.addWidget(self.btn_add)
        buttonbox.addWidget(self.btn_del)
        buttonbox.addWidget(self.btn_find)
        buttonbox.addWidget(self.btn_inc)
        buttonbox.addWidget(self.btn_show)

        self.display = QTextEdit()
        self.display.setReadOnly(True)


        mainbox = QVBoxLayout()
        mainbox.addLayout(inputbox)
        mainbox.addLayout(buttonbox)
        mainbox.addWidget(self.display)

        self.setLayout(mainbox)

        self.show()

    def buttonClicked(self):
        button = self.sender()
        key = button.text()
        if key == "Show":
            self.showScoreDB()
        elif key == "Find":
            self.findScoreDB()
        elif key == "Inc":
            self.incScoreDB()
        elif key == "Del":
            self.delScoreDB()
        elif key == "Add":
            self.addScoreDB()

    def closeEvent(self, event):
        self.writeScoreDB()

    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()


    # write the data into person db
    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    def showScoreDB(self):
        data = ""
        for p in sorted(self.scoredb[:], key=lambda person: person[self.cb_key.currentText()]):  # 람다식/ scdb의 내용을 기준값을 비교해 정렬
            for attr in sorted(p):  # scdb의 아이템 내부 속성들 정렬(알파벳순 age, name, score
                data += attr + " = " + str(p[attr]) + "   \t"
            data += "\n"
        self.display.setText(data)

    def findScoreDB(self):
        nameNotFound = []
        cnt = 0;
        data = ""
        findKey = self.lineedit_name.text().split(" ")
        for k in findKey[:]:                                                                           # 여러명을 찾기 위해 리스트로 받아옴 (0번째는 명령어)
            flagOverlap = False
            for p in sorted(self.scoredb[:], key=lambda person: person[self.cb_key.currentText()]):                                  # 람다식/ scdb의 내용을 기준값을 비교해 정렬
                if p['Name'] == k:
                    for attr in sorted(p):                                                              # scdb의 아이템 내부 속성들 정렬(알파벳순 age, name, score
                        data += attr + " = " + str(p[attr]) + "   \t"
                    data += "\n"
                    cnt += 1;
                    flagOverlap = True
                elif flagOverlap:                                                                        # 같은이름이 끝났을 때 루프 종료
                    break
            if not flagOverlap:                                                                          # else를 쓰지 않은 이유 : for loop의 마지막 요소에서 찾아지는 경우 실행이 되기 때문
                nameNotFound += [k]

        data += "\n\n\n"
        data += "Student name:\n"
        for p in nameNotFound:
            data += (p + "\n")
        data += ("not found ")
        self.display.setText(data)

    def incScoreDB(self):                                                                    # --- 중복된 이름 중 원치않는 인물의 점수가 수정될 수 있기 때문에 매커니즘의 수정 필요 ---
        data = ""
        names = self.lineedit_name.text().split(" ")
        try:
            amount = int(self.lineedit_amount.text())
            if amount == "":
                amount = 0
        except ValueError as e:
            data = ("자료형의 처리에 있어 오류가 발생했습니다. (" + e.args[0] +")")
            print(data)
            self.display.setText(data)
        else:
            nameNotFound = []
            for k in names[:]:
                flagOverlap = False
                for p in sorted(self.scoredb[:], key=lambda person: person[self.cb_key.currentText()]):                             # 람다식/ scdb의 내용을 기준값을 비교해 정렬
                    if p['Name'] == k:
                        p['Score'] += amount
                        flagOverlap = True
                    elif flagOverlap:                                                                   # 같은이름이 끝났을 때 루프 종료
                        break
                if not flagOverlap:                                                                         # else를 쓰지 않은 이유 : for loop의 마지막 요소에서 찾아지는 경우 실행이 되기 때문
                    nameNotFound += [k]
            self.showScoreDB()
            data += "\n\n\n"
            data += "Student name:\n"
            for p in nameNotFound:
                data += (p + "\n")
            data += ("not found ")
            self.display.setText(self.display.toPlainText() + data)

    def delScoreDB(self):
        nameNotFound = []
        nameTotalDel = []
        names = self.lineedit_name.text().split(" ")
        for k in names[:]:  # 여러명을 동시에 지우기 위해
            flagOverlap = False
            cnt = 0
            for p in sorted(self.scoredb[:], key=lambda person: person[self.cb_key.currentText()]):  # add 하면서 정렬이 되지 않았으므로 정렬 추가
                if p['Name'] == k:
                    self.scoredb.remove(p)
                    cnt += 1;
                    flagOverlap = True
                elif flagOverlap:  # 같은이름이 끝났을 때 루프 종료
                    break
            if not flagOverlap:  # else를 쓰지 않은 이유 : for loop의 마지막 요소에서 찾아지는 경우 실행이 되기 때문
                nameNotFound += [k]
            nameTotalDel += [{"Name": k, "Cnt": cnt}]
        self.showScoreDB()
        data = "\n\n\n"
        for t in nameTotalDel:
            data += (t["Name"] + " 총 " + str(t["Cnt"]) + "명 삭제\n")
        for p in nameNotFound:
            data += ("Student Name \"" + p + "\" not found\n")
        self.display.setText(self.display.toPlainText() + data)

    def addScoreDB(self):
        try:
            record = {'Name': self.lineedit_name.text(), 'Age': int(self.lineedit_age.text()), 'Score': int(self.lineedit_score.text())}
        except ValueError as e:
            self.display.setText("자료형의 처리에 있어 오류가 발생했습니다. (" + e.args[0] + ")")
        else:
            self.scoredb += [record]
            self.showScoreDB()


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())

