from openfhe import *
from utils import *
from algorithms import *
from testcode import *



if __name__ == "__main__":
	InnerProductTest()
	PolyEvalTest(50, 1, 8, 5.0) #Scaling Factor, iteration, degree, bound
