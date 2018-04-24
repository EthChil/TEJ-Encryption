

def handleIn():
    #cipherText = raw_input("Enter in the ciphertext in HEX seperate with space: ").split()

    cipherText = "0a 07 1a 0f 00 1f 0c 0d 10 01 0e".split()

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


cipher = handleIn()

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



lookupList = [32,
              65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
              97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110 ,111, 112, 113, 114, 115, 116, 117 ,118, 119, 120, 121, 122]


for i in lookupList:
    print(chr(i)),

for j in cipher:
    print("STARTING TO DO " + j)
    for i in lookupList:
        decoded = bruteForce(i, j)

        if(decoded == 32 or (decoded >= 65 and decoded <= 90) or (decoded >= 97 and decoded <= 122)):

            print(chr(decoded)),
        else:
            print("*"),

