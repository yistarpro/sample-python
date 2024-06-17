from openfhe import *
from utils import *
from algorithms import *




def sqTest():

    mult_depth = 5
    scale_mod_size = 50
    batch_size = 1 << 14

    parameters = CCParamsCKKSRNS()
    parameters.SetMultiplicativeDepth(mult_depth)
    parameters.SetScalingModSize(scale_mod_size)
    parameters.SetBatchSize(batch_size)

    cc = GenCryptoContext(parameters)
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)

    print("The CKKS scheme is using ring dimension: " + str(cc.GetRingDimension()))

    keys = cc.KeyGen()
    cc.EvalMultKeyGen(keys.secretKey)

    x1 = [0.25, 0.5, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0]

    ptx1 = cc.MakeCKKSPackedPlaintext(x1)

    print("Input x1: " + str(ptx1))

    # Encrypt the encoded vectors
    c1 = cc.Encrypt(keys.publicKey, ptx1)

    # Step 4: Evaluation
    c2 = evalsq(cc, c1, 3)

    # Step 5: Decryption and output
    print("Results of homomorphic computations:")
    result = cc.Decrypt(c2, keys.secretKey)
    result.SetLength(batch_size)
    print("8 sq of x1 = " + str(result))


   