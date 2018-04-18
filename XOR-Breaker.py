

def handleIn():
    cipherText = raw_input("Enter in the ciphertext in HEX seperate with space: ").split()

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

def bruteForce(index, binaryCipher):
    binaryTest = str(bin(index)).split("b")[1]

    out = []

    while (True):
        if (len(binaryTest) < 8):
            binaryTest = "0" + binaryTest
        else:
            break

    for i in range(8):
        if(int(binaryTest[i]) != int(binaryCipher[i])):
            out.append("1")
        else:
            out.append("0")

    return int(''.join(out), 2)


for i in range(255):
    print(chr(bruteForce(i, "00001101")))
    print(chr(bruteForce(i, )))
