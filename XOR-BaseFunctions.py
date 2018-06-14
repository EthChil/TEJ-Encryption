

def getSolutions(arr, key, depth, encrypted):

    if(depth < len(arr)):
        for i in arr[depth]:
            tmp = getSolutions(arr, key.append(i), depth+1)


    else:
        if (testString(breakArr(key, encrypted)) and testString(''.join(key))):
            if (checkDict(breakArr(key, encrypted))):
                finalSolutions.append(breakArr(key, encrypted))





if (len(keyArr) == 5):
    print("KEY LENGTH 5 STARTED")
    for i in keyArr[0]:
        for j in keyArr[1]:
            for k in keyArr[2]:
                for l in keyArr[3]:
                    for m in keyArr[4]:
                        if (testString(breakArr([i, j, k, l, m], encrypt)) and testString(i + j + k + l + m)):
                            if(checkDict(breakArr([i, j, k, l, m], encrypt))):
                                # print(breakArr([i, j, k, l, m], encrypt))
                                solutions.append(breakArr([i, j, k, l, m], encrypt))