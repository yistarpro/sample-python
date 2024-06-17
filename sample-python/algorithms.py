from openfhe import *
from utils import *


def evalsq(cc, ciphertext, num):
    result = ciphertext.Clone()


    for s in range(num):
        result = cc.EvalMult(result, result)
        cc.ModReduceInPlace(result)


    return result