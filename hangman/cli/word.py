import random

class Word:

    def __init__(self, filename):
        self.words = []
        f = open(filename, 'r')     # word 파일 가져오기
        lines = f.readlines()       # word 전체 라인 읽기(list)
        f.close()                   # 파이썬은 가져오고 바로 닫아서 메모리 소모 적게하는걸 선호

        self.count = 0
        for line in lines:
            word = line.rstrip()    # strip 처리(쓸데없는 공백제거)
            self.words.append(word) # words 리스트에 추가
            self.count += 1

        print('%d words in DB' % self.count)    #단어 갯수

    def randFromDB(self):   # 랜덤 단어 선택
        r = random.randrange(self.count)
        return self.words[r]

