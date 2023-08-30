from Dataset import Dataset
from HKP import HKP
import logging
import time
from argparse import ArgumentParser
import csv
import os

if __name__ == '__main__':

    # Parse the command line arguments
    parser = ArgumentParser(
        description='Using different options to anonymize the dataset, according to arguments passed by CLI')

    # Add arguments for h, k, and p
    parser.add_argument('--h', type=float, default=0.8, help='Specify the value for h')
    parser.add_argument('--k', type=int, default=2, help='Specify the value for k')
    parser.add_argument('--p', type=int, default=2, help='Specify the value for p')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', type=str, help='Specify technique for public item removal')
    group.add_argument('-top_x', type=int, help='Specify how much top_x values wil be remove')

    args = parser.parse_args()

    logger = logging.getLogger("H-K-P")
    logging.basicConfig(level=logging.DEBUG)
    ds = Dataset("../Datasets/")
    N_Pub_item_before=len(ds.public_items)

    hkp = HKP(args.h,args.k,args.p,ds)

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
    #write the anonymization into a file
    Num_pub_transactions=ds.write_anonymized_ds([ds.public_transactions, ds.private_transactions])
    end=time.time()
    print(f"TOTAL TIME: {end-start} s")

    #Utility Loss
    N_Pub_item_After=len(ds.public_items)
    Utility_loss=100-((N_Pub_item_After/N_Pub_item_before)*100)
    print(f"After: {N_Pub_item_After}")
    print(f"Before: {N_Pub_item_before}")

    cwd = os.getcwd()
    parent_dir = os.path.relpath(os.path.join(cwd, '../Datasets'))
    folder = os.path.join(parent_dir, 'Performance')

    #The performances will be written into a csv file
    if not os.path.exists(folder):
        os.makedirs(folder)

    if args.m:
        option = f"m-{args.m}"
    elif args.top_x:
        option = f"Top_x-{args.top_x}"
    else:
        option = "Option-Unknown"

    data_to_write = [
        [f"h: {args.h}"],
        [f"k: {args.k}"],
        [f"p: {args.p}"],
        [f"Option: {option}"],
        [f"TotalTime: {end - start} s"],
        [f"Utility Loss: {Utility_loss}"],
        [f"Number of public transactions after anonymization: {Num_pub_transactions}"]
    ]

    with open(f'{folder}/{args.h}_{args.k}_{args.p}_{option}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_to_write)


