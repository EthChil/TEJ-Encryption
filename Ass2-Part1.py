import time

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



while(True):
    entry = raw_input("Please enter the number of spaces each letter in the alphabet is to move to the right. (1 to 26)")

    try:
        offset = int(entry)

        if((offset >= 1 and offset <= 26)):
            break
        else:
            print("That is not within the  1 to 26 range")

    except ValueError:
        print("That is not a number")

    time.sleep(1)


word = raw_input("Enter in a word to encrypt or decrypt")

if word == "END":
    exit(0)

if word == "\"END\"":
    word = "END"

while True:
    quest = raw_input("Enter 'Y' to encrypt or 'N' to decrypt the entered word")

    if("N" in quest or "n" in quest or "y" in quest or "Y" in quest):
        break

    print("not a valid input")
    time.sleep(1)

if("Y" in quest or "y" in quest):
    output = []

    for i in word:
        LOWER = False

        if(i.islower()):
            LOWER = True


        i = i.lower()

        if (i != " "):
                if(not LOWER):
                    if (ord(i) + offset > 122):
                        output.append(chr((ord(i) + offset) - 26).upper())
                    else:
                        output.append(chr(ord(i) + offset).upper())
                else:
                    if(ord(i) + offset > 122):
                        output.append(chr((ord(i) + offset) - 26))
                    else:
                        output.append(chr(ord(i) + offset))
        else:
            output.append(" ")
else:
    output = []

    for i in word:
        LOWER = False

        if(i.islower()):
            LOWER = True

        i = i.lower()

        if(i != " "):
            if (not LOWER):
                if (ord(i) + offset > 122):
                    output.append(chr((ord(i) - offset) - 26).upper())
                else:
                    output.append(chr(ord(i) - offset).upper())
            else:
                if (ord(i) + offset > 122):
                    output.append(chr((ord(i) - offset) - 26))
                else:
                    output.append(chr(ord(i) - offset))
        else:
            output.append(" ")


print(''.join(output))