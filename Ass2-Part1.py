import time

while(True):
    entry = raw_input("Please enter the number of spaces each letter in the alphabet is to move to the right. (1 to 26)")

    try:
        offset = int(entry)

        if(offset >= 1 and offset <= 26):
            break
        else:
            print("That is not within the  1 to 26 range")

    except ValueError:
        print("That is not a number")

    time.sleep(1)


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
        i = i.lower()

        if (i != " "):
                if(ord(i) + offset > 122):
                    output.append(chr((ord(i) + offset) - 26))
                else:
                    output.append(chr(ord(i) + offset))
        else:
            output.append(" ")
else:
    output = []

    for i in word:
        i = i.lower()

        if(i != " "):
            if(ord(i) - offset < 97):
                output.append(chr((ord(i) - offset)+ 26))
            else:
                output.append(chr(ord(i) - offset))
        else:
            output.append(" ")


print(''.join(output))