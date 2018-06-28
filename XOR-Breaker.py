#Written by Ethan Childerhose on 6/12/2018
#
#XOR-Breaker
#
#Given an encrypted HEX string it will decrypt it given that the answer is an english sentence
# with minimal slang. The program will retain most punctuation and all capitalization.
#
#TODO: allow infinite length key
#
#
import threading
import enchant

dictionary = enchant.Dict("en_US")

#ascii
lookupList = [46, 44, 33, 63, 34, 32,
              65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
              97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110 ,111, 112, 113, 114, 115, 116, 117 ,118, 119, 120, 121, 122]

diagraphs = ["bq", "bz", "cf", "cj" "cv", "cx", "fq", "fv", "fx", "fz", "gq", "gv", "gx", "hx", "hz", "jb", "jd", "jf", "jg", "jh", "jl", "jm", "jp", "jq", "js", "jt", "jv", "jw", "jx", "jy", "jz", "kq", "kx", "kz", "mx", "mz", "pq", "pv", "px", "qb", "qc", "qd", "qf", "qg", "qh", "qj", "qk", "ql", "qm", "qn", "qp", "qq", "qv", "qw", "qx", "qy", "qz", "sx", "tq", "vb", "vf", "vh", "vj", "vk", "vm", "vp", "vq", "vw", "vx", "wq", "wv", "wx", "xd", "xj", "xk", "xr", "xz", "yq", "yy", "zf", "zr", "zx"]

#Vowel List
vowels = ["a", "e", "i", "o", "u", "y",
          "A", "E", "I", "O", "U", "Y"]


finalKeyAnswers = []


class keySolverThread (threading.Thread):
   def __init__(self, threadID, name, keyLength):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.keyLength = keyLength
   def run(self):
       solution = recursiveSolve(self.keyLength)

       if(solution != None):
           finalKeyAnswers.append(solution)

#Takes raw hex input from the user then convert to binary and return
def handleIn():
    cipherText = chunks(raw_input("Enter in the ciphertext in HEX: ").strip(" "), 2)

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

#convert ascii characters to binary
def asciiToBin(ascii):
    binary = bin(ord(ascii)).split("b")[1]

    while (True):
        if (len(binary) < 8):
            binary = "0" + binary
        else:
            break

    return binary

#XOR a character and a 8bit binary number
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

#convert a number to any base recursively
def convertToBase(number, base):
    if(number / base < 1):
        return str(number % base)
    else:
        return str(number % base) + "," + str(convertToBase(int(number / base), base))

#Check if diagraph exists in the given string
def checkDiagraph(input):
    for i in diagraphs:
        if(i in input):
            return False
    return True

#Check if a vowel exists in the given string
def checkVowel(input):
    for i in vowels:
        if(i in input):
            return True
    return False


#Codes is taken in as an array of binary
def bruteSingleChar(codes, depth):
    possible = []

    for a in lookupList:
        found = True

        for b in codes:
            if(len(b) <= depth):
                break

            b = b[depth]

            if(xorChar(chr(a), b) not in lookupList):
                found = False
                break

        if(found):
            possible.append(chr(a))

    return possible

#xor two strings return the output
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


def getKey(decrypt, encrypt):
    decrypted = []

    for pointer in range(len(encrypt)):
        decrypted.append(chr(xorChar(decrypt[pointer], encrypt[pointer])))

    return ''.join(decrypted)

#Break an array l into smaller arrays of length n
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

#Check if an array is a good result after being computed
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

    return wordCount

#Calculates the amount of different permutations in a given dataset
def calcIterations(keyArray):
    permutations = 1

    for i in keyArray:
        permutations *= len(i)

    return permutations

#Main recursive solver
def recursiveSolve(keyLength):
    finalSolutions = []
    result = []

    def getSolutions(keyArray, key, depth, encrypted):
        if (depth < len(keyArray)):
            for i in keyArray[depth]:
                if(key == None):
                    getSolutions(keyArray, [i], depth + 1, encrypted)
                else:
                    key.append(i)
                    getSolutions(keyArray, key, depth + 1, encrypted)
                    key.remove(i)
        else:
            if (testString(breakArr(key, encrypted)) and testString(''.join(key))):
                if (checkDict(breakArr(key, encrypted))):
                    finalSolutions.append(breakArr(key, encrypted))

    for i in range(0, keyLength, 1):
        result.append(bruteSingleChar(list(chunks(cipher, keyLength)), i))

    if (goodResult(result)):
        print("st " + str(calcIterations(result)) + " en")

        getSolutions(result, [], 0, cipher)
        print(str(len(finalSolutions)) + " Possible English Legal Solution(s) with key length " + str(keyLength))

        if (len(finalSolutions) > 0):
            return finalSolutions

#Finds a substring that repeats within the string
def repeats(string):
    for x in range(1, len(string)):
        substring = string[:x]

        if substring * (len(string)//len(substring))+(substring[:len(string)%len(substring)]) == string:
            return substring

    return string


#-----------------------------------------------------MAIN PROGRAM--------------------------------------------------------

cipher = handleIn()

#print raw binary
print("Raw Binary Input")
print(cipher)

#Array of threads
threads = []

#Create threads, one thread will find the legal solns of a given key length
maxKeySize = int(len(cipher)/3)
if(maxKeySize < 5):
    maxKeySize = 5

#Create and name threads
for n in range(2, maxKeySize, 1):
    threads.append(keySolverThread(n, "Thread-"+str(n), n))

#start all the threads
for num in range(len(threads)):
    print("Starting Thread #" + str(num))
    threads[num].start()

#wait for all the threads to finish
for num in range(len(threads)):
    print("Waiting on Thread #" + str(num))
    threads[num].join()

#print all possible answers
print("")
print("All Possible Solutions: "),
print(finalKeyAnswers)

#new line
print("")

#narrow down to the most likely answers
wordScore = 0
bestResult = ""
possibleAnswers = []

#Select best solution(s)
for soln in finalKeyAnswers:
    for ans in soln:
        if(wordCount(ans) > wordScore):
            possibleAnswers = []
            possibleAnswers.append(ans)
            wordScore = wordCount(ans)

        elif(wordCount(ans) == wordScore):
            possibleAnswers.append(ans)

#Print the final Solution(s)
print("Solutions are:")
for i in possibleAnswers:
    print(str(i) + " with an english word count of " + str(wordScore) + ", encrypted with the key: " + str(repeats(getKey(i ,cipher))))



