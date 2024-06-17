from openfhe import *
from utils import *
from algorithms import *




def InnerProductTest():
        
    # Step 1: Parameter Set

    multDepth = 5; # 곱셈 한번짜리 연산이므로 1이면 충분하다.
    batchSize = 1 << 16;
    scaleModSize = 40;


    parameters = CCParamsCKKSRNS()
    parameters.SetMultiplicativeDepth(multDepth)
    parameters.SetScalingModSize(scaleModSize)
    parameters.SetRingDim(batchSize << 1)
    parameters.SetBatchSize(batchSize)
    
    cc = GenCryptoContext(parameters)

    # Enable the features that you wish to use
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)
    #/ cc.Enable(ADVANCEDSHE)
       

    # Step 2: Key Generation
    keys = cc.KeyGen()
    cc.EvalMultKeyGen(keys.secretKey)

    AddRotKeyForSum(keys.secretKey, cc, batchSize) #batchSize개의 입력에 대한 innerproduct를 실험할 예정.

    # Step 3: Encoding and encryption of inputs
    print("!!!!!!!!!!!!!!! InnerProduct Test !!!!!!!!!!!!!!!")

    # Inputs
    x1 = randomRealArray(batchSize, 1)
    x2 = randomRealArray(batchSize, 1)

    ptxt1 = cc.MakeCKKSPackedPlaintext(x1)
    ptxt2 = cc.MakeCKKSPackedPlaintext(x2)

    #입력값을 확인해보자
    ptxt1.SetLength(16); #전체를 출력하는 것보다 일부만 체크하기
    print("\n Input x1: "+str(ptxt1))
    ptxt1 = cc.MakeCKKSPackedPlaintext(x1) #setlength로 잘랐었기 때문에, 다시한번 plaintext 생성

    # Encrypt the encoded vectors
    ciphertext1 = cc.Encrypt(keys.publicKey, ptxt1)
    ciphertext2 = cc.Encrypt(keys.publicKey, ptxt2)


    c2=EvalInnerProduct(cc, ciphertext1, ciphertext2, batchSize)
    result = cc.Decrypt(c2, keys.secretKey)

    #정확도 체크
    InnerProductprecision(result, x1, x2, batchSize)

    #실제 Decryption 결과 내부는 어떻게 생겼을까?
    result.SetLength(8)
    print("Decrypted" +str(result))



    #입력값의 범위(bound), 시험 횟수(iteration), 차수(degree)등의 요소를 더 넣어보자
def PolyEvalTest(scaleModSize, iteration, degree, bound):

    multDepth = 10 # 8차 polynomial은 몇의 depth를 먹을까? 
    batchSize = 1 << 16

    parameters = CCParamsCKKSRNS()
    parameters.SetMultiplicativeDepth(multDepth)
    parameters.SetScalingModSize(scaleModSize)
    parameters.SetRingDim(batchSize << 1)
    parameters.SetBatchSize(batchSize)
        
    cc = GenCryptoContext(parameters)

    # Enable the features that you wish to use
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)
    #/ cc.Enable(ADVANCEDSHE)


    # Key Generation
    keys = cc.KeyGen()
    cc.EvalMultKeyGen(keys.secretKey)

    # Encoding and encryption of inputs
    print("!!!!!!!!!!!!!!! Polynomial Eval Test !!!!!!!!!!!!!!!")
    print("Degree: " + str(degree))

    # Inputs
    x1 = randomRealArray(batchSize, bound)
    ptxt1 = cc.MakeCKKSPackedPlaintext(x1)

    #x1의 일부 값 확인
    print("\n Input x1: ")
    for i in range(8):
        print(x1[i])

    # Encrypt the encoded vectors
    ptxt1 = cc.MakeCKKSPackedPlaintext(x1)
    c1 = cc.Encrypt(keys.publicKey, ptxt1)

    #coeff 생성
    coeff = randomIntArray(degree+1, bound); #상수항 때문에 degree +1
    #coeff = {0,0,1}; #x^2
    #coeff = {1,2,1}; 
    #coeff = {0,1}; #x
    print("Coeff: ",coeff)

    for j in range(iteration):
            
        c2 = EvalPolynomial(cc, c1, coeff)
        result = cc.Decrypt(c2, keys.secretKey)
        PolyEvalprecision(result, x1, coeff, batchSize)

        result.SetLength(8)
        print("Result: " + str(result))
        print("Level: " + str(result.GetLevel())) #곱셈 횟수 소모(level)확인            
      
 