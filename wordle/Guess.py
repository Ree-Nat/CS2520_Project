import string

'''
Guess Class:
    - holds guess string
    - holds letter evaluation list (str)
    - checks guess against chosen secret string
'''


class Guess:
    def __init__(self, guess:str, secret:str):
        if isinstance(guess, str):
            self.__guess = guess
        else:
            raise TypeError("Guess must be a string")

        # CORRECT, PRESENT, or ABSENT
        self.__letterEval = ["1", "2", "3", "4", "5"] #list of letter evaluations compared to secret word

        if isinstance(secret, str):
            self.checkWord(secret)
        else:
            raise TypeError("Secret must be a string")

    #populate letter evaluation list
    def checkWord(self, secretWord):
        letterCount = {letter: 0 for letter in string.ascii_lowercase}
        for i in secretWord:
            letterCount[i] += 1

        #first pass - for CORRECT only
        for i in range(5):
            if self.__guess[i] == secretWord[i]:
                self.__letterEval[i] = "CORRECT"
                letterCount[secretWord[i]] -= 1

        #second pass - for PRESENT/ABSENT
        for i in range(5):
            if self.__letterEval[i] == "CORRECT":
                pass
            elif self.__guess[i] in secretWord and letterCount[self.__guess[i]] > 0:
                self.__letterEval[i] = "PRESENT"
                letterCount[self.__guess[i]] -= 1
            else:
                self.__letterEval[i] = "ABSENT"

    #GETTER/SETTER
    def getGuess(self):
        return self.__guess
    def getLetterEval(self, pos:int) -> str:
        return self.__letterEval[pos]

    def __str__(self):
        return f"Guess String: {self.__guess} | FeedBack String: {self.__letterEval}"



#--------------------------------------------------
#testing
def test_guess():
    guessObj1 = Guess("paint", "apple")
    print(guessObj1)
    guessObj2 = Guess("snake", "snake")
    print(guessObj2)
    guessObj3 = Guess("pipes", "plane")
    print(guessObj3)
    guessObj4 = Guess("slept", "sleep")
    print(guessObj4)

# test_guess()