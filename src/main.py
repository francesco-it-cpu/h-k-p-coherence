from Dataset import Dataset
from HKP import HKP
import logging
import time
import argparse

if __name__ == '__main__':

    # Parse the command line arguments
    parser = argparse.ArgumentParser(
        description='Using different options to anonymize the dataset, according to arguments passed by CLI')
    parser.add_argument('-m', type=str, help='Help specify technique for public item removeall ', default='suppress-all')

    args = parser.parse_args()

    logger = logging.getLogger("H-K-P")
    logging.basicConfig(level=logging.DEBUG)
    ds = Dataset("../Datasets/Paper Example")


    hkp = HKP(0.8,2,2,ds)



    start = time.time()
    minimal_moles,non_moles,MM = hkp.find_minimal_moles()
    IL = hkp.IL()
    #vuoi cancellare tutto? fai questo
    #hkp.suppress_MM(minimal_moles)
    #print(f"ds is {ds.transactions}\n")
    if MM !={}:
       print(f"MM is {MM}")

    if IL!={}:
        print(f"IL is {IL}\n")

    print(f"minimal moles are: {minimal_moles}\n")
    #if there are Minimal moles
    if MM!={}:
        while all(len(values) > 0 for values in minimal_moles.values()):
             el=hkp.suppress_MM(minimal_moles,args,IL,MM)
             print(f"Element(s) with max MM/IL: {el}\n")
             minimal_moles, non_moles, MM = hkp.find_minimal_moles()
             IL = hkp.IL()

        print(f"AFTER ELIMINATION\n")
        print(f"public_transactions are: {ds.public_transactions}")
        print(f"public_items are: {ds.public_items}\n")
        #print(f"minimal moles are: {minimal_moles}\n")
    ds.write_anonymized_ds([ds.public_transactions, ds.private_transactions])
    end=time.time()
    print(f"TOTAL TIME: {end-start} s")


