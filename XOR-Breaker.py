#Written by Ethan Childerhose on 6/12/2018
#
#XOR-Breaker
#
#Given an encrypted HEX string it will decrypt it given that the answer is an english sentence
# with minimal slang. The program will retain most punctuation and all capitalization.
#
#TODO: allow infinite length key
#TODO: print key after solved
#
#
import threading
import enchant

dictionary = enchant.Dict("en_US")

lookupList = [46, 44, 33, 63, 34, 32,
              65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
              97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110 ,111, 112, 113, 114, 115, 116, 117 ,118, 119, 120, 121, 122]

diagraphs = ["cj", "fq", "gx", "hx", "jf", "jq", "jx", "jz", "qb", "qc", "qj", "qk", "qx", "qz", "sx", "vf", "vj", "vq", "vx", "wx", "xj", "zx"]
#diagraphs = ["bq", "bz", "cf", "cj" "cv", "cx" "fq" "fv" "fx" "fz" "gq" "gv" "gx" "hx" "hz" "jb" "jd" "jf" "jg" "jh" "jl" "jm" "jp" "jq" "js" "jt" "jv" "jw" "jx" "jy" "jz" "kq" "kx" "kz" "mx" "mz" "pq" "pv" "px" "qb" "qc" "qd" "qf" "qg" "qh" "qj" "qk" "ql" "qm qn qp qq qv qw qx qy qz sx tq vb vf vh vj vk vm vp vq vw vx wq wv wx xd xj xk xr xz yq yy zf zr zx]

vowels = ["a", "e", "i", "o", "u", "y",
          "A", "E", "I", "O", "U", "Y"]

commonLetters = ["E","T","A","O","I","N",
                 "e","t","a","o","i","n"]

finalKeyAnswers = []

class keySolverThread (threading.Thread):
   def __init__(self, threadID, name, keyLength):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.keyLength = keyLength
   def run(self):
       solution = solveKey(self.keyLength)

       if(solution != None):
           finalKeyAnswers.append(solution)


def handleIn():
    cipherText = raw_input("Enter in the ciphertext in HEX seperate with space: ").split()

    #cipherText = "05 00 01 09 1c 4d 2c 4d 0b 12 00 00 4d 0c 05 0c 0b".split()
    #fuck the police 0d 10 1a 00 45 0d 03 00 59 1b 0a 15 02 06 1c
    #key

    output = []

    for i in cipherText:
        temp = str(bin(int(i, 16))).split("b")[1]

        while(True):
            if(len(temp) < 8):
                temp = "0" + temp
            else:
                break

        output.append(temp)

    return output


def asciiToBin(ascii):
    binary = bin(ord(ascii)).split("b")[1]

    while (True):
        if (len(binary) < 8):
            binary = "0" + binary
        else:
            break

    return binary

#Will do a XOR given an ascii
def bruteForce(index, binaryCipher):
    binaryTest = asciiToBin(chr(index))

    out = []

    for i in range(8):
        if(int(binaryTest[i]) != int(binaryCipher[i])):
            out.append("1")
        else:
            out.append("0")

    return int(''.join(out), 2)

def xorChar(a, b):
    binA = asciiToBin(a)
    binB = b

    out = []

    for i in range(8):
        if(int(binA[i]) != int(binB[i])):
            out.append("1")
        else:
            out.append("0")

    return int(''.join(out), 2)


def convertToBase(number, base):
    if(number / base < 1):
        return str(number % base)
    else:
        return str(number % base) + "," + str(convertToBase(int(number / base), base))

def genKey(index, list):
    nums = convertToBase(index, len(list)).split(",")

    output = ""

    for i in nums:
        output = output + chr(lookupList[int(i)])

    return output


#08 0d 02 07
#llll

def checkDiagraph(input):
    for i in diagraphs:
        if(i in input):
            return False
    return True

def checkVowel(input):
    for i in vowels:
        if(i in input):
            return True
    return False

def calcWeight(word):
    score = 0

    for letter in word:
        for i in commonLetters:
            if(i == letter):
                score += 1

    return score


#Codes is taken in as an array of binary
def bruteSingleChar(codes, depth):
    possible = []
    scores = []

    for a in lookupList:
        found = True
        word = []

        for b in codes:
            if(len(b) <= depth):
                break

            b = b[depth]

            if(xorChar(chr(a), b) not in lookupList):
                found = False
                break
            else:
                word.append(chr(xorChar(chr(a), b)))

        wordStr = ''.join(word)

        #if(found and checkDiagraph(wordStr) and checkVowel(wordStr)):
        if (found ):
            possible.append(chr(a))
            scores.append(calcWeight(wordStr))

    # if(len(possible) > 1):
    #     highestScore = max(scores)
    #
    #     for i in range(len(scores)):
    #         if(scores[i] == highestScore):
    #             return possible[i]

    return possible

def breakArr(arr, encrypted):
    arrPointer = 0
    decrypt = []

    for letter in encrypted:
        decrypt.append(chr(xorChar(arr[arrPointer], letter)))
        if(arrPointer == len(arr) - 1):
            arrPointer = 0
        else:
            arrPointer += 1

    return ''.join(decrypt)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def goodResult(list):
    for item in list:
        if(len(item) == 0):
            return False
    return True

def testString(wordStr):
    splitWord = wordStr.split(" ")

    #Check word length
    if(len(splitWord) < (len(wordStr)/5)-1):
        return False

    #check if punctution is followed by a space
    if('.' in wordStr and '. ' not in wordStr):
        return False

    #quick check of whole string with a check on "
    if(not checkDiagraph(wordStr) or not checkVowel(wordStr) or wordStr.count('"') % 2 == 1):
        return False

    for word in splitWord:
        if (not checkDiagraph(word) or not checkVowel(word)):
            return False

        upperCaseCount = sum(1 for c in word if c.isupper())

        if (upperCaseCount < len(word) and upperCaseCount > 1):
            return False

        if (upperCaseCount >= 1 and word[0].islower()):
            return False

    return True

def checkDict(sentence):
    sentence = sentence.strip(",")
    sentence = sentence.strip(".")
    sentence = sentence.strip("?")
    sentence = sentence.strip("!")
    sentence = sentence.strip('"')
    words = sentence.split(" ")


    wordCount = 0.0

    for word in words:
        if(dictionary.check(word)):
            wordCount += 1.0

    #print(words, " ", wordCount)

    if(float(wordCount) / float(len(words)) > 0.5):
        return True
    return False

def wordCount(sentence):
    sentence = sentence.strip(",")
    sentence = sentence.strip(".")
    sentence = sentence.strip("?")
    sentence = sentence.strip("!")
    sentence = sentence.strip('"')
    words = sentence.split(" ")


    wordCount = 0

    for word in words:
        if(dictionary.check(word)):
            wordCount += 1.0

    print(words, " ", wordCount)

    return wordCount

def recursiveSolve(keyArr, encrypt):
    solutions = []

    if(len(keyArr) == 2):
        print("KEY LENGTH 2")
        for i in keyArr[0]:
            for k in keyArr[1]:
                if(testString(breakArr([i, k], encrypt)) and testString(i+k)):
                    if (checkDict(breakArr([i, k], encrypt))):
                        #print(breakArr([i, k], encrypt))
                        solutions.append(breakArr([i, k], encrypt))


    if (len(keyArr) == 3):
        print("KEY LENGTH 3")
        for i in keyArr[0]:
            for j in keyArr[1]:
                for k in keyArr[2]:
                    if (testString(breakArr([i, j, k], encrypt)) and testString(i+j+k)):
                        if (checkDict(breakArr([i, j, k], encrypt))):
                            #print(breakArr([i, j, k], encrypt))
                            solutions.append(breakArr([i, j, k], encrypt))

    if (len(keyArr) == 4):
        print("KEY LENGTH 4")
        for i in keyArr[0]:
            for j in keyArr[1]:
                for k in keyArr[2]:
                    for l in keyArr[3]:
                        if (testString(breakArr([i, j, k, l], encrypt)) and testString(i + j + k + l)):
                            if (checkDict(breakArr([i, j, k, l], encrypt))):
                                #print(breakArr([i, j, k, l], encrypt))
                                solutions.append(breakArr([i, j, k, l], encrypt))

    if (len(keyArr) == 5):
        print("KEY LENGTH 5")
        for i in keyArr[0]:
            for j in keyArr[1]:
                for k in keyArr[2]:
                    for l in keyArr[3]:
                        for m in keyArr[4]:
                            if (testString(breakArr([i, j, k, l, m], encrypt)) and testString(i + j + k + l + m)):
                                if(checkDict(breakArr([i, j, k, l, m], encrypt))):
                                    #print(breakArr([i, j, k, l, m], encrypt))
                                    solutions.append(breakArr([i, j, k, l, m], encrypt))

    return solutions

def solveKey(keyLength):
    result = []

    for i in range(0, keyLength, 1):
        result.append(bruteSingleChar(list(chunks(cipher, keyLength)), i))

    if (goodResult(result)):
        solutions = recursiveSolve(result, cipher)
        print(str(len(solutions)) + "Possible English Legal Solns' = " +  " with key length " + str(keyLength))

        if (len(solutions) > 0):
            return solutions

#-----------------------------------------------------MAIN PROGRAM--------------------------------------------------------

cipher = handleIn()

print("Raw Binary Input")
print(cipher)



threads = []


for n in range(2, len(cipher), 1):
    threads.append(keySolverThread(n, "Thread-"+str(n), n))

    # result = []
    #
    # for i in range(0, n, 1):
    #     result.append(bruteSingleChar(list(chunks(cipher, n)), i))
    #
    # if(goodResult(result)):
    #     solutions = recursiveSolve(result, cipher)
    #     print("Possible English Legal Solns' = ", len(solutions))
    #
    #     if(len(solutions) > 0):
    #         finalKeyAnswers.append(solutions)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(finalKeyAnswers)

wordScore = 0
bestResult = ""
possibleAnswers = []

for soln in finalKeyAnswers:
    for ans in soln:
        if(wordCount(ans) > wordScore):
            possibleAnswers = []
            possibleAnswers.append(ans)
            wordScore = wordCount(ans)

        if(wordCount(ans) == wordScore):
            possibleAnswers.append(ans)

print("Solutions are"),
for i in possibleAnswers:
    print(i, " with a english word count of", wordScore)

