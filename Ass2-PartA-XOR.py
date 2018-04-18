import time, binascii

#***********************************************************************#
#                                                                       #
#                          PROGRAM HEADER                               #
#***********************************************************************#
#***********************************************************************#
#                                                                       #
# PROGRAMMER'S NAME:    Ethan Childerhose                               #
#                                                                       #
# DATE:                 Wednesday, April 18 2018                        #
#                                                                       #
# PROGRAM NAME:         Assignment 3                                    #
#                                                                       #
# CLASS:                TEJ-3M1                                         #
#                                                                       #
# ASSIGNMENT:           Assignment 2                                    #
#                                                                       #
# TEACHER:              Mr. Henrich                                     #
#                                                                       #
# DUE DATE:             Wednesday, April 18 2018                        #
#                                                                       #
#***********************************************************************#
#                                                                       #
# WHAT THE PROGRAM DOES                                                 #
#                                                                       #
# This program will encode and decode ROT N ecnryptions                 #
#                                                                       #
#***********************************************************************#
#                                                                       #
# PROCEDURES                                                            #
#                                                                       #
# No procedures                                                         #
#***********************************************************************#
#                                                                       #
# ERROR HANDLING                                                        #
#                                                                       #
# Verify input from user to ensure it's numerical or not                #
#                                                                       #
#***********************************************************************#
#                                                                       #
# PROGRAM LIMITATIONS                                                   #
#                                                                       #
# There is no way to change the student's marks after they have been    #
# inputted.                                                             #
#***********************************************************************#
#                                                                       #
# EXTENSIONS AND IMPROVEMENTS                                           #
# While the program follows the output, the program could be improved by#
# allowing the user to change the marks of an already submitted student #
#***********************************************************************#

counter = 0

def xor(char):
    binary = "0"+str(bin(ord(char))).split("b")[1]

    while(True):
        if(len(binary) < 8):
            binary = "0"+binary
        else:
            break

    #print(binary)

    out = []

    global counter

    #print(key)

    for i in range(len(binary)):

        if(int(key[counter]) != int(binary[i])):
            out.append("1")
        else:
            out.append("0")

        if(counter < len(key)-1):
            counter += 1
        else:
            counter = 0


    return "".join(out)

offset = raw_input("Please enter the key to encrypt / decrypt with using a XOR process")


if offset == "END":
    exit(0)

enteredKey = []

for i in offset:
    enteredKey.append("0"+str(bin(ord(i))).split("b")[1])

key = ''.join(enteredKey)

word = raw_input("Enter in a word to encrypt or decrypt")

if word == "END":
    exit(0)


while True:
    quest = raw_input("Enter 'Y' to encrypt or 'N' to decrypt the entered word")

    if("N" in quest or "n" in quest or "y" in quest or "Y" in quest):
        break

    print("not a valid input")
    time.sleep(1)


if("Y" in quest or "y" in quest):
    output = []

    for i in word:
        #print(i)
        output.append(str(hex(int(xor(i), 2))).split("x")[1])
        #output.append(int(xor(i), 2))
        #output.append(xor(i))

    print(output)



else:
    output = []

    for i in word:
        #print(i)
        output.append(str(hex(int(xor(i), 2))).split("x")[1])
        #output.append(int(xor(i), 2))
        #output.append(xor(i))

    print(output)

