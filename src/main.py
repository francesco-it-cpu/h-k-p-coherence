
from Dataset import Dataset
from HKP import HKP

if __name__ == '__main__':
    print("test:")
    ds = Dataset("../Datasets/Paper Example")


    hkp = HKP(0.8,2,2)

    [moles,non_moles] = hkp.get_moles(dataset=ds)
    print(f"Size-{hkp.p} moles")



