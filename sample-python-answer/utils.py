from openfhe import *
import random
import math


#무작위 실수 생성
def randomRealArray(size, bound):
    result =[]
    for i in range(size):
        result.append(random.random()*bound) # 0~1사이의 숫자를 생성한 후, bound를 곱한다.

    return result

#무작위 정수 생성.
def randomIntArray(size, bound):
    result =[]
    for i in range(size):
        result.append(random.randrange(0,bound)) # bound까지의 정수 생성

    return result

#Outputs precision level
def precision(vals, vals2, size):
    maximum = 0
    vals1=vals.GetRealPackedValue()

    for i in range(size):
        tmp = vals1[i]-vals2[i]
        if tmp < 0 : tmp=-tmp
        if tmp > maximum : maximum = tmp

    prec = -math.log2(maximum)
    print("Estimated precision in bits:" + prec + ", max error: "  + maximum)


def PolyEvalprecision(vals, vals1, coeff, size):
    maximum = 0
    truevals=vals.GetRealPackedValue()

    for i in range(size):
        result = 0
        for d, co in enumerate(coeff):
            result += math.pow(vals1[i], d)*co

        tmp = truevals[i]-result
        if tmp < 0 : tmp=-tmp
        if tmp > maximum : maximum = tmp

    prec = -math.log2(maximum)
    print("Estimated precision in bits:" + str(prec) + ", max error: "  + str(maximum))


def InnerProductprecision(vals, vals1, vals2, size):
    maximum = 0
    result = 0
    truevals=vals.GetRealPackedValue()

    for i in range(size):
        result +=vals1[i]*vals2[i]
        
    tmp = truevals[i]-result
    if tmp < 0 : tmp=-tmp
    if tmp > maximum : maximum = tmp

    prec = -math.log2(maximum)
    print("Estimated precision in bits:" + str(prec) + ", max error: "  + str(maximum))



