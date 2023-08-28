import time

from Dataset import Dataset
from HKP import HKP
import logging

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    ds = Dataset("../Datasets/Paper Example")


    hkp = HKP(0.8,2,3,ds)
    start = time.time()
    minimal_moles,non_moles,MM = hkp.find_minimal_moles()
    prova = hkp.get_IL()
    print(prova)



    print(f"Total time {end-start} s")





