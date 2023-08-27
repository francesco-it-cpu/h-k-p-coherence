import time

from Dataset import Dataset
from HKP import HKP
import logging

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    ds = Dataset("../Datasets/")


    hkp = HKP(0.4,2,3,ds)
    start = time.time()
    minimal_moles,non_moles = hkp.find_minimal_moles()
    end = time.time()
    print(f"Found these minimal moles {minimal_moles.values()} in {end-start} s")





