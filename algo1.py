import sys
import numpy
import random
import string

# ==============================================================================
#   Open the file and load datafile
# ==============================================================================
def readPassword(inputfile):
    realPasswordList = []
    with open(inputfile) as infile:
        for line in infile:
            line = line.replace("\n", "")
            realPasswordList.append(line.strip())
    return realPasswordList    


# ==============================================================================
#  Write to file with data
# ==============================================================================
def storeHoneyWord(honeyWordLists, outputfile):
    with open(outputfile, 'w') as output:
        for honeyWords in honeyWordLists:
            line = ','.join(honeyWords)
            output.write(line + '\n')    

# ==============================================================================
#   Helper functions
# ==============================================================================
#pass all digits password to check if it's in sequence
def isNumSequence(seq):
    if len(seq) < 3:
        return False
    increment = seq[1] - seq[0]
    for k in range(len(seq) - 2):
        if (seq[k+2] - seq[k+1]) != increment:
            return False
    return True

#input: all digits password, output: randomly generted sweeetword in sequence as well
def mutateSequence(seq):
    increment = seq[1] - seq[0]
    new_start = random.randint(0,8)
    sweetword = "" + str(new_start)
    for i in range(len(seq)-1):
        if int(sweetword[i]) + increment < 10:
            if int(sweetword[i]) + increment < 0 :
                sweetword += str(random.randint(0,9))
            else:
                sweetword += str(int(sweetword[i]) + increment)
        else:
            sweetword += '0'
    return sweetword

# find the first occurence of a subword within the password
def findsubword(password):
    totalen = len(password)
    start = 0
    end = totalen - 1
    for i in range(totalen):
        if password[i].isalpha():
            start = i
            break
    for j in range(start,totalen):
        if not password[j].isalpha():
            end = j - 1
            break
    word =  password[start:end+1]
    return [start,end,word]

# input: a character of password, output: a character    
def flipCapitalizition(word):
    if word.isupper():
        word = word.lower()
    else:
        word = word.upper()
    return word

# input: a character or digit of password, output: a leet letter
def replaceWithLeet(word):
    leetMap = {
        'a': '@',
        'b': '6',
        'B': '8',
        'e': '3',
        'g': '9',
        'G': '&',
        'i': '1',
        'o': '0',
        'O': '0',
        's': '$',
        'l': '1',
        'p': '9',
        'P': '9',
        'u': 'v',
        'U': 'V',
        'w': 'vv',
        'W': 'VV',
        'z': '2',
        'Z': '2',
        '1': 'l',
        '2': 'z',
        '3': 'E',
        '6': 'b',
        '8': 'B',
        '9': 'q',
        '0': 'O'
    }
    if word in leetMap:
        word = leetMap[word]
    return word

def appendNumber():
    numberChoice = ['123','1234','000','456','789','111',str(random.randint(0,9))]
    return random.choice(numberChoice)

def replaceSymbol():
    symbolChoice = ['~','!','@','#','*','%','?','.','-']
    return random.choice(symbolChoice)    

def shortDigit():
    nineties = '19'
    twenties = '20'
    nineties += (random.choice(list('0123456789')))
    nineties += (random.choice(list('0123456789')))
    twenties += (random.choice(list('0123456789')))
    twenties += (random.choice(list('0123456789')))
    
    samplelist = ['1111','1234','111','234','456','789','741','852','963','000','0000',nineties,twenties]
    return random.choice(samplelist)

# ==============================================================================
#   Base Cases
# ==============================================================================
# flip first word's capitalization
# input: password, output: sweetword
def flipFirstCapitalizition(password):
    for i in range(len(password)):
        if password[i].isalpha():
            start = i
            break
    word = password[i]
    if word.isupper():
        word = word.lower()
    else:
        word = word.upper()
    password = password.replace(password[i], word)
    return password

# replace a random vowel
# input: password, output: sweetword
def replaceVowel(password):
    vowelListLower = ['a','e','i','o','u']
    vowelListCap = ['A','E','I','O','U']
     
    vowel_pos = [ i for i,v in enumerate(password) if v.lower() in ('aeiou') ]
    numVowel = len(vowel_pos)
    if numVowel > 0:
        replaceIdx = vowel_pos[random.randint(0,numVowel-1)]
        firstVowel = password[replaceIdx]
        if firstVowel.isupper():
            vowelListCap.remove(firstVowel)
            password = password.replace(password[replaceIdx],random.choice(vowelListCap))
        else:
            vowelListLower.remove(firstVowel)
            password = password.replace(password[replaceIdx],random.choice(vowelListLower))
    return password

# randomly add a suffix at the end of the first occurence of word
# input: password, output: sweetword
def addSuffix(password):
    suffixList = ['ed','s','ish']
    digitSec = []
    alphaSec = []
    symbolSec = []
    start,end,word = findsubword(password)
    word += random.choice(suffixList)
    return password[:start] + word + password[end+1:]

# ==============================================================================
#   Generate Honeywords
# ==============================================================================
def honeyWordGenerator(realpasswordList, n):
    honeyWordLists = []
    # generate honeyword for each password in the dictionary
    for password in realpasswordList:
        honeyWordList = []
        # add the original password to the list
        honeyWordList.append(password)
        passLen = len(password)
        maxMutation = passLen/3
        isSequence = False
        # pure digits password
        if password.isdigit():
            i = 0
            seq = [int(digit) for digit in password]
            if isNumSequence(seq):
                isSequence = True
                seqnum = 0
            while i < n:
                # add a few sequence of numbers for passwords in sequence
                if isSequence:
                    while seqnum < min(n/2,8):
                        # if digits in sequence, generate other sequence as well
                        sweetword = mutateSequence(seq)
                        if sweetword != password and sweetword not in honeyWordList:
                            honeyWordList.append(sweetword)
                            i += 1
                            seqnum += 1
                numMutate = 0
                sweetword = password
                for j in range(passLen):
                    # 20% chance of replacing digit with a leet letter
                    if random.randint(0,100) > 70 and numMutate < maxMutation:
                        leetDigit = replaceWithLeet(sweetword[j])
                        sweetword = sweetword.replace(sweetword[j], leetDigit)
                        numMutate += 1
                    else:
                        # 40% chance of replacing a digit with a random digit
                        if random.randint(0,100) > 60 and numMutate < maxMutation:
                            sweetword = sweetword.replace(sweetword[j], str(random.randint(0,9)))
                            numMutate += 1
                # 50% chance of having one more digit
                if (bool(random.getrandbits(1))):
                    sweetword = sweetword + str(random.randint(0,9))
                if random.randint(0,100) > 60:
                    sweetword += shortDigit()
                # make sure no replication
                if sweetword != password and sweetword not in honeyWordList:
                    honeyWordList.append(sweetword)
                    i += 1
        else:   
            i = 0
            # for small N: 1) only capitalize the first letter 2) change the vowel 3) add suffix
            baseCases = {'1':flipFirstCapitalizition, '2': replaceVowel, '3': addSuffix}
            cases = ['1','2','3']
            numBase = 3
            # if the password only consists digits and symbols, no letters
            if not any(c.isalpha() for c in password):
                while i < n:
                    sweetword = password
                    numMutate = 0
                    for j in range(passLen):
                        # 25% chance of replacing letter with a leet letter
                        if random.randint(0,100) > 75 and numMutate < maxMutation:
                            leetWord = replaceWithLeet(sweetword[j])
                            sweetword = sweetword.replace(sweetword[j], leetWord)
                            numMutate += 1
                        else:
                            # 25% chance of make a letter lower or uppercase
                            if random.randint(0,100) > 75 and sweetword[j].isalpha() and numMutate < maxMutation:
                                word = flipCapitalizition(sweetword[j])
                                sweetword = sweetword.replace(sweetword[j], word)
                                numMutate += 1
                            # 40% chance of replace the special characters
                            if random.randint(0,100) > 60 and (not (sweetword[j].isalnum())) and numMutate < maxMutation:
                                sweetword = sweetword.replace(sweetword[j], replaceSymbol())
                                numMutate += 1
                    # 30% chance of adding some numbers at the end
                    if random.randint(0,100) > 70:
                        sweetword = sweetword + appendNumber()
                    # make sure no replication
                    if sweetword != password and sweetword not in honeyWordList:
                        honeyWordList.append(sweetword)
                        i += 1
            # passwords with letters
            if n < 4:
                while i < n:
                    sweetword = password
                    sweetword = baseCases[cases[i]](sweetword)
                    # add to the honeyword list
                    if sweetword != password and sweetword not in honeyWordList:
                        honeyWordList.append(sweetword)
                        i += 1
            else: 
                for  k in range(0,3):
                    sweetword = password
                    sweetword = baseCases[cases[k]](sweetword)
                    # add to the honeyword list
                    if sweetword != password and sweetword not in honeyWordList:
                        honeyWordList.append(sweetword)
                        i += 1
                while i < n:
                    sweetword = password
                    numMutate = 0
                    for j in range(passLen):
                        # 25% chance of replacing letter with a leet letter
                        if random.randint(0,100) > 75 and numMutate < maxMutation:
                            leetWord = replaceWithLeet(sweetword[j])
                            sweetword = sweetword.replace(sweetword[j], leetWord)
                            numMutate += 1
                        else:
                            # 25% chance of make a letter lower or uppercase
                            if random.randint(0,100) > 75 and sweetword[j].isalpha() and numMutate < maxMutation:
                                word = flipCapitalizition(sweetword[j])
                                sweetword = sweetword.replace(sweetword[j], word)
                                numMutate += 1
                            # 40% chance of replace the special characters
                            if random.randint(0,100) > 60 and (not (sweetword[j].isalnum())) and numMutate < maxMutation:
                                sweetword = sweetword.replace(sweetword[j], replaceSymbol())
                                numMutate += 1
                    # 30% chance of adding some numbers at the end
                    if random.randint(0,100) > 70:
                        sweetword = sweetword + appendNumber()
                    # make sure no replication
                    if sweetword != password and sweetword not in honeyWordList:
                        honeyWordList.append(sweetword)
                        i += 1
        # shuffle all the sweetwords
        random.shuffle(honeyWordList)
        honeyWordLists.append(honeyWordList)
    return honeyWordLists

# ==============================================================================
#   Main function
# ==============================================================================

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("missing arguments. Please try with: python algorithm1.py n input_filename output_filename")
    n = int(sys.argv[1]) - 1
    inputfile = sys.argv[2]
    outputfile = sys.argv[3]
    # parse input file
    realPasswordList = readPassword(inputfile)
    # generate n honey words
    honeyWordLists = honeyWordGenerator(realPasswordList, n)
    # output to desired file
    storeHoneyWord(honeyWordLists, outputfile)
