
from Dataset import Dataset
from HKP import HKP
from typing import Set

if __name__ == '__main__':
    print("test:")
    ds = Dataset("../Datasets")
    print("Transactions")
    print(ds.transactions[0])

    hkp = HKP(0,2,0.8)
    print(hkp.calculate_and_check_sup_greater(['126','70'], ds))
