import itertools

lookupList = [46, 44, 33, 63, 34, 32,
              65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
              97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110 ,111, 112, 113, 114, 115, 116, 117 ,118, 119, 120, 121, 122]

diagraphs = ["cj", "fq", "gx", "hx", "jf", "jq", "jx", "jz", "qb", "qc", "qj", "qk", "qx", "qz", "sx", "vf", "vj", "vq", "vx", "wx", "xj", "zx"]

vowels = ["a", "e", "i", "o", "u", "y",
          "A", "E", "I", "O", "U", "Y"]

commonLetters = ["E","T","A","O","I","N",
                 "e","t","a","o","i","n"]

def handleIn():
    #cipherText = raw_input("Enter in the ciphertext in HEX seperate with space: ").split()

    cipherText = "05 00 01 09 1c 4d 2c 4d 0b 12 00 00 4d 0c 05 0c 0b".split()
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
    if (checkDiagraph(wordStr) and checkVowel(wordStr)):
        return True
    return False


def recursiveSolve(keyArr, encrypt):
    print("KEY LENGTH 2")
    if(len(keyArr) == 2):
        for i in keyArr[0]:
            for k in keyArr[1]:
                if(testString(breakArr([i, k], encrypt)) and testString(i+k)):
                    print(breakArr([i, k], encrypt))

    print("KEY LENGTH 3")
    if (len(keyArr) == 3):
        for i in keyArr[0]:
            for j in keyArr[1]:
                for k in keyArr[2]:
                    if (testString(breakArr([i, j, k], encrypt)) and testString(i+j+k)):
                        print(breakArr([i, j, k], encrypt))

    print("KEY LENGTH 4")
    if (len(keyArr) == 4):
        for i in keyArr[0]:
            for j in keyArr[1]:
                for k in keyArr[2]:
                    for l in keyArr[3]:
                        if (testString(breakArr([i, j, k, l], encrypt)) and testString(i + j + k + l)):
                            print(breakArr([i, j, k, l], encrypt))

    print("KEY LENGTH 5")
    if (len(keyArr) == 5):
        for i in keyArr[0]:
            for j in keyArr[1]:
                for k in keyArr[2]:
                    for l in keyArr[3]:
                        for m in keyArr[4]:
                    if (testString(breakArr([i, j, k], encrypt)) and testString(i + j + k)):
                        print(breakArr([i, j, k], encrypt))


cipher = handleIn()

print(cipher)

# print(bruteSingleChar(cipher))

finalKeyAnswers = []

for n in range(2, len(cipher), 1):
    result = []

    for i in range(0, n, 1):
        result.append(bruteSingleChar(list(chunks(cipher, n)), i))

    if(goodResult(result)):
        print(result)
        recursiveSolve(result, cipher)
        finalKeyAnswers.append(result)

#print(finalKeyAnswers)
print("meme")




#
# for i in lookupList:
#     print(chr(i)),
#
# for j in cipher:
#     print("STARTING TO DO " + j)
#     for i in lookupList:
#         decoded = bruteForce(i, j)
#
#         if(decoded in lookupList):
#             print(chr(decoded)),
#         else:
#             print("*"),
#
