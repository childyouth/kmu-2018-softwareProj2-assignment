from cli.guess import Guess
from cli.hangman import Hangman
from cli.word import Word


def gameMain():
    word = Word('words.txt')
    guess = Guess(word.randFromDB())    # 디스플레이에 올리기위해 문자 갯수등의 정보 주는것

    finished = False
    hangman = Hangman()
    maxTries = hangman.getLife()    # 목숨

    while guess.numTries < maxTries:

        display = hangman.get(maxTries - guess.numTries)     # 현재 행맨 상태
        print(display)
        guess.display()     # 비밀글자 정보들출력

        guessedChar = input('Select a letter: ')
        if len(guessedChar) != 1:   # 여러 글자 적엇는지 확인
            print('One character at a time!')
            continue
        if guessedChar in guess.guessedChars:   # 중복된 글자인지
            print('You already guessed \"' + guessedChar + '\"')
            continue

        finished = guess.guess(guessedChar)     # 끝났는지(안에서 guess 처리 완료)
        print("\n"*10)
        if finished == True:
            break

    if finished == True:    # 성공시
        print('Success')
    else:   # 실패시
        print(hangman.get(0))
        print('word [' + guess.secretWord + ']')
        print('guess [' + "".join(guess.currentStatus) + ']')
        print('Fail')

if __name__ == '__main__':
    gameMain()
