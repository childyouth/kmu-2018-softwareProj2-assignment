class Guess:
    def __init__(self, word):
        self.numTries = 0   # 추리한 횟수
        self.secretWord = word
        self.guessedChars = list()
        self.currentStatus = ['_']*len(self.secretWord)

    def display(self):
        print("You Tried: " + ", ".join(self.guessedChars))
        print("Current: " + "".join(self.currentStatus))
        print("Tries: " + str(self.numTries))
        print("Select a letter: ",end="")

    def guess(self, character):
        self.guessedChars.append(character)
        self.guessedChars.sort()
        if character in self.secretWord:
            start = self.secretWord.find(character)
            while start != -1:
                self.currentStatus[start] = character
                start = self.secretWord.find(character,start+1)
        else:
            self.numTries += 1
        return "".join(self.currentStatus) == self.secretWord
