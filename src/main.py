import time

from Dataset import Dataset
from HKP import HKP
import logging

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    ds = Dataset("../Datasets/Paper Example")


    hkp = HKP(0.8,2,2,ds)
    start = time.time()
    minimal_moles,non_moles,MM = hkp.find_minimal_moles()
    IL = hkp.IL()
    print(f"IL is {IL}\nMM is {MM}")
    end=time.time()
    print(f"Total time {end-start} s")





