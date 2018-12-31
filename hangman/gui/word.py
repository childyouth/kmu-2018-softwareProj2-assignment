import random

class Word:

    def __init__(self, filename):
        self.words = []
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        self.count = 0
        for line in lines:
            word = line.rstrip()
            self.words.append(word)
            self.count += 1

        print('%d words in DB' % self.count)


    def test(self):
        return 'default'


    def randFromDB(self):
        r = random.randrange(self.count)
        return self.words[r]
    def randFromDB(self, minLength):
        tmp_words = self.words
        random.shuffle(tmp_words)
        word = ""
        for w in tmp_words:
            if len(w) >= minLength:
                word = w
                break
            else:
                if len(word) < len(w):
                    word = w
        return word