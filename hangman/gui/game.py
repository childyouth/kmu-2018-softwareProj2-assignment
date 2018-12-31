#-*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton

from hangman import Hangman
from guess import Guess
from word import Word


class HangmanGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize word database        
        self.word = Word('words.txt')

        # Hangman display window
        self.hangmanWindow = QTextEdit()
        self.hangmanWindow.setReadOnly(True)
        self.hangmanWindow.setAlignment(Qt.AlignLeft)
        font = self.hangmanWindow.font()
        font.setFamily('Courier New')
        self.hangmanWindow.setFont(font)

        # Layout
        hangmanLayout = QGridLayout()
        hangmanLayout.addWidget(self.hangmanWindow, 0, 0)

        # Status Layout creation
        statusLayout = QGridLayout()

        # Display widget for current status
        self.currentWord = QLineEdit()
        self.currentWord.setReadOnly(True)
        self.currentWord.setAlignment(Qt.AlignCenter)
        font = self.currentWord.font()
        self.FONTSIZE = font.pointSize() + 8
        font.setPointSize(font.pointSize() + 8)
        self.currentWord.setFont(font)
        statusLayout.addWidget(self.currentWord, 0, 0, 1, 2)

        # Display widget for already used characters
        self.guessedChars = QLineEdit()
        self.guessedChars.setReadOnly(True)
        self.guessedChars.setAlignment(Qt.AlignLeft)
        self.guessedChars.setMaxLength(52)
        statusLayout.addWidget(self.guessedChars, 1, 0, 1, 2)

        # Display widget for message output
        self.message = QLineEdit()
        self.message.setReadOnly(True)
        self.message.setAlignment(Qt.AlignLeft)
        self.message.setMaxLength(52)
        statusLayout.addWidget(self.message, 2, 0, 1, 2)

        # Input widget for user selected characters
        self.charInput = QLineEdit()
        self.charInput.setMaxLength(1)
        statusLayout.addWidget(self.charInput, 3, 0)

        # Button for submitting a character
        self.guessButton = QToolButton()
        self.guessButton.setText('Guess!')
        self.guessButton.clicked.connect(self.guessClicked)
        statusLayout.addWidget(self.guessButton, 3, 1)

        # Button for a new game
        self.newGameButton = QToolButton()
        self.newGameButton.setText('New Game')
        self.newGameButton.clicked.connect(self.startGame)
        statusLayout.addWidget(self.newGameButton, 4, 0)

        # Layout placement
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(hangmanLayout, 0, 0)
        mainLayout.addLayout(statusLayout, 0, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle('Hangman Game')

        # Start a new game on application launch!
        self.startGame()


    def startGame(self):
        self.hangman = Hangman()
        self.guess = Guess(self.word.randFromDB(30))
        self.gameOver = False

        self.charInput.setDisabled(False)
        self.guessButton.setDisabled(False)
        self.hangmanWindow.setPlaceholderText(self.hangman.currentShape())
        self.currentWord.setText(self.guess.displayCurrent())
        self.guessedChars.setText(self.guess.displayGuessed())
        self.message.clear()
        self.message.setText("새 게임!")
        font = self.currentWord.font()
        if len(self.currentWord.text()) > 20:
            font.setPointSize(self.FONTSIZE - (int((len(self.currentWord.text()) - 20)/4)+3))
            self.currentWord.setFont(font)
        else:
            font.setPointSize(self.FONTSIZE)
            self.currentWord.setFont(font)
        self.currentWord.setText(self.guess.displayCurrent())


    def guessClicked(self):
        guessedChar = self.charInput.text()
        self.charInput.clear()
        self.message.clear()

        if self.gameOver:
            # 메시지 출력하고 - message.setText() - 리턴
            self.message.setText("이미 끝난 게임입니다.")
            return

        # 입력의 길이가 1 인지를 판단하고, 아닌 경우 메시지 출력, 리턴
        elif len(guessedChar) != 1:
            self.message.setText("알파벳 한글자만 입력하세요.")
            return
        # 이미 사용한 글자인지를 판단하고, 아닌 경우 메시지 출력, 리턴
        elif guessedChar in self.guess.guessedChars:
            self.message.setText("이미 입력된 단어 " + guessedChar)
            return
        success = self.guess.guess(guessedChar)
        if not success:
            # 남아 있는 목숨을 1 만큼 감소
            # 메시지 출력
            self.hangman.decreaseLife()
            self.message.setText(guessedChar + " 는 단어에 없습니다.")

        # hangmanWindow 에 현재 hangman 상태 그림을 출력
        # currentWord 에 현재까지 부분적으로 맞추어진 단어 상태를 출력
        # guessedChars 에 지금까지 이용한 글자들의 집합을 출력

        self.hangmanWindow.setPlaceholderText(self.hangman.currentShape())
        self.currentWord.setText(self.guess.displayCurrent())
        self.guessedChars.setText(self.guess.displayGuessed())

        if self.guess.finished():
            # 메시지 ("Success!") 출력하고, self.gameOver 는 True 로
            self.message.setText("축하합니다!")
            self.charInput.setDisabled(True)
            self.guessButton.setDisabled(True)
            self.gameOver = True

        elif self.hangman.getRemainingLives() == 0:
            # 메시지 ("Fail!" + 비밀 단어) 출력하고, self.gameOver 는 True 로
            self.message.setText("졌습니다. 정답은 " + self.guess.secretWord)
            self.charInput.setDisabled(True)
            self.guessButton.setDisabled(True)
            self.gameOver = True


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec_())

