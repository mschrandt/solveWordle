import random

def load():
    acceptedWords = []
    possibleWords = []
    letterFrequency = {}

    with open("possibleWords.txt", "r", newline='') as wordFile:
        for word in wordFile:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                #print(word)
                possibleWords.append(word)
                picked = set()
                for c in word:
                    if c not in letterFrequency:
                        letterFrequency[c] = 0
                    if c not in picked:
                        picked.add(c)
                        letterFrequency[c] += 1

    with open("acceptedwords.txt", "r", newline='') as wordFile:
        for word in wordFile:
            word = word.lower().strip()
            if len(word) == 5 and word.isalpha():
                #print(word)
                acceptedWords.append(word)

    return acceptedWords, possibleWords, letterFrequency

def filterWords(acceptedWords, possibleWords, letterFrequency, guess, guessResults):
    if guessResults == "":
        words.remove(guess)
        return words, letterFrequency

    newPossibleWords = [x for x in possibleWords if matchesGuess(x, guess, guessResults)]
    newAcceptedWords = [x for x in acceptedWords if matchesGuess(x, guess, guessResults)]
    newLetterFrequency = {}
    for word in newPossibleWords:
        for i in range(len(guessResults)):
            if guessResults[i] != 'x':
                word.replace(guess[i],'',1)
        picked = set()
        for c in word:
            if c not in newLetterFrequency:
                newLetterFrequency[c] = 0
            if c not in picked:
                picked.add(c)
                newLetterFrequency[c] += 1
    return newAcceptedWords, newPossibleWords, newLetterFrequency

def matchesGuess(word, guess, guessResults):
    for i in range(len(word)):
        if guessResults[i] == 'g' and word[i] != guess[i]:
            return False
        elif guessResults[i] == 'y':
            if word[i] == guess[i]:
                return False

            #find all char indexes of yellow letter
            yellowLetterInstances = findLetterIndexesInWord(word, guess[i])

            #ensure all char indexes are not already green
            foundPotential = False
            for j in yellowLetterInstances:
                if j != i and guessResults[j] != 'g':
                    foundPotential = True
                    break
            if not foundPotential:
                return False
        elif guessResults[i] == 'x':
            if word[i] == guess[i]:
                return False

            #find all char indexes of wrong letter
            wrongLetterInstancesGuess = findLetterIndexesInWord(guess, guess[i])
            okCount = 0
            for j in wrongLetterInstancesGuess:
                if guessResults[j] != 'x':
                    okCount += 1
            wrongLetterInstancesWord = findLetterIndexesInWord(word, guess[i])
            if len(wrongLetterInstancesWord) > okCount:
                return False
    return True


def findLetterIndexesInWord(word, letter):
    return [i for i, ltr in enumerate(word) if ltr == letter]

def pickWord(acceptedWords, possibleWords, letterFrequency, lastGuess, lastGuessResult):
    highestScore = -1
    bestWord = ''

    for word in acceptedWords:
        wordCopy = word
        for i in range(len(lastGuessResult)):
            if lastGuessResult[i] != 'x':
                word.replace(lastGuess[i],'',1)

        frequencySum = 0
        picked = set()
        for letter in word:
            if letter not in picked:
                if letter in letterFrequency:
                    frequencySum += letterFrequency[letter]
                picked.add(letter)
                #frequencySum += letterFrequency[letter] * 0.5

        if frequencySum > highestScore:
            highestScore = frequencySum
            bestWord = wordCopy

    return bestWord

def evaluateGuess(word, guess):
    result = ""
    for i in range(len(word)):
        if word[i] == guess[i]:
            result += 'g'
        else:
            foundLetter = False
            foundIndex = word.find(guess[i])
            while foundIndex != -1:
                if guess[foundIndex] != word[foundIndex]:
                    foundLetter=True
                    break
                foundIndex = word.find(guess[i], foundIndex+1)

            if foundLetter == True:
                result += 'y'
            else:
                result += 'x'
    return result


def play():
    acceptedWords, possibleWords, letterFrequency = load()
    print("Letter frequencies")
    for letter in letterFrequency:
        print(letter + ":", letterFrequency[letter])

    print(len(possibleWords)," words in dictionary.")

    guessResults = ""
    while guessResults != 'ggggg' and len(words) > 0:
        currentGuess = pickWord(acceptedWords, possibleWords, letterFrequency)
        print("Best guess:",currentGuess)
        print("Guess results (gyxgx, blank to get a new word, or word<space>gyxgx for custom guess)")
        guessResults = input(":").lower()

        customGuess = guessResults.split(' ')
        if len(customGuess) > 1:
            currentGuess = customGuess[0]
            guessResults = customGuess[1]

        acceptedWords, possibleWords, letterFrequency = filterWords(acceptedWords, possibleWords, letterFrequency, currentGuess, guessResults)
        print(len(possibleWords)," words remaining in dictionary.")

def playAi(showPlay = True):
    acceptedWords, possibleWords, letterFrequency = load()
    word = random.choice(possibleWords)
    #word = "sauce"
    print("Word is",word)
    if showPlay:
        print("Letter frequencies")
        for letter in letterFrequency:
            print(letter + ":", letterFrequency[letter])

        print(len(possibleWords)," words in dictionary.")
        print("Word is:", word)

    guessResults = ""
    currentGuess = ""
    numGuesses = 0
    while guessResults != 'ggggg' and len(possibleWords) > 0:
        currentGuess = pickWord(acceptedWords, possibleWords, letterFrequency, currentGuess, guessResults)
        #if(numGuesses == 0):
        #    currentGuess = "roate"
        if showPlay:
            print("Best guess:",currentGuess)
            print("Guess results (gyxgx, blank to get a new word, or word<space>gyxgx for custom guess)")

        guessResults = evaluateGuess(word, currentGuess)
        numGuesses += 1

        if showPlay:
            print(guessResults)

        acceptedWords, possibleWords, letterFrequency = filterWords(acceptedWords, possibleWords, letterFrequency, currentGuess, guessResults)

        if showPlay:
            print(len(possibleWords)," words remaining in dictionary.")


    if len(possibleWords) == 0:
        print("Failed to guess word:", word)
    else:
        print("Guessed", word, "in", numGuesses,"guesses")
    return numGuesses

totGuesses = 0
numGames = 100
for _ in range(numGames):
    totGuesses += playAi(False)

print(totGuesses/numGames)
