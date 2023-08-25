import time

from Dataset import Dataset
from HKP import HKP
import logging

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    ds = Dataset("../Datasets/Paper Example")


    hkp = HKP(0.8,2,2)

    logging.debug('Searching size 1 moles...')
    size_1_moles = hkp.get_size1_moles(ds)
    cleaned_ds = hkp.eliminate_size_1_moles(ds,size_1_moles)
    logging.info(f"Size-1 moles: {size_1_moles}\n ")
    [moles,non_moles] = hkp.get_moles(ds)



    #logging.info(f"Cleaned dataset: {cleaned_ds}\n ")

    logging.info(f"Size-{hkp.p} moles: {moles}\n")



