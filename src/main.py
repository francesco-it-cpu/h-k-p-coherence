from Dataset import Dataset
from HKP import HKP
import logging
import time
from argparse import ArgumentParser

if __name__ == '__main__':

    # Parse the command line arguments
    parser = ArgumentParser(
        description='Using different options to anonymize the dataset, according to arguments passed by CLI')
    group = parser.add_mutually_exclusive_group(required=True)

    # Opzione per specificare la tecnica per la rimozione degli elementi pubblici
    group.add_argument('-m', type=str, help='Specify technique for public item removal')

    # Opzione per specificare il valore top_x
    group.add_argument('-top_x', type=int, help='Specify the top_x value')

    args = parser.parse_args()

    logger = logging.getLogger("H-K-P")
    logging.basicConfig(level=logging.DEBUG)
    ds = Dataset("../Datasets/Paper Example")

    hkp = HKP(0.8,2,2,ds)


    start = time.time()
    minimal_moles,non_moles,MM = hkp.find_minimal_moles()
    IL = hkp.IL()
    """
    if MM !={}:
       print(f"MM is {MM}")

    if IL!={}:
        print(f"IL is {IL}\n")
    """

    print(f"minimal moles are: {minimal_moles}\n")
    #if there are Minimal moles
    if MM!={}:
        while all(len(values) > 0 for values in minimal_moles.values()):
             el=hkp.suppress_MM(minimal_moles,args.m,args.top_x,IL,MM)
             print(f"Suppressing Item(s) with max MM/IL: {el}\n")
             minimal_moles, non_moles, MM = hkp.find_minimal_moles()
             IL = hkp.IL()

        print(f"minimal moles are: {minimal_moles}\n")
    ds.write_anonymized_ds([ds.public_transactions, ds.private_transactions])
    end=time.time()
    print(f"TOTAL TIME: {end-start} s")


