import time, binascii

while(True):
    entry = raw_input("Please enter the key to encrypt / decrypt with using a XOR process")

    try:
        offset = int(entry)

        break

    except ValueError:
        print("That is not a number")

    time.sleep(1)



if offset == "END":
    exit(0)

word = raw_input("Enter in a word to encrypt or decrypt")

if word == "END":
    exit(0)


output = []

for i in offset:
    output.append(str(bin(ord(i))).split("b")[1])


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