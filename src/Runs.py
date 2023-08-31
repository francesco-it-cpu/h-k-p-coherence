from itertools import product
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
    group.add_argument('-m', type=str, help='Specify technique for public item removal')
    group.add_argument('-top_x', type=int, help='Specify how much top_x values wil be remove')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format='%(name)s [%(levelname)s] >> %(message)s')
    logger = logging.getLogger("HKP-Anonymizer")

    h_values = [0.8, 0.4]
    k_values = [2, 3, 4, 5, 6]
    p_values = [2, 3, 4, 5, 6]

    # Calculate all possible combinations of h, k e p
    configurations = list(product(h_values, k_values, p_values))

    for config in configurations:

        logger.debug("Loading Dataset...")
        ds = Dataset("../Datasets/")
        N_Pub_item_before = len(ds.public_items)
        N_transactions = len(ds.transactions)

        h, k, p = config
        print(type(p),type(h),type(k))
        hkp=HKP(h, k, p, ds)

        start = time.time()
        minimal_moles, non_moles, MM = hkp.find_minimal_moles()
        IL = hkp.IL()
        """
        if MM !={}:
           print(f"MM is {MM}")
    
        if IL!={}:
            print(f"IL is {IL}\n")
        """
        logger.info(f"minimal moles are: {minimal_moles}\n")
        # if there are Minimal moles
        if MM != {}:
            while len(MM) != 0:
                el = hkp.suppress_MM(minimal_moles, args.m, args.top_x, IL, MM)
                minimal_moles, non_moles, MM = hkp.find_minimal_moles()
                if len(MM) != 0:
                    IL = hkp.IL()

            logger.info(f"minimal moles are: {minimal_moles}\n")

        end = time.time()
        logger.debug(f"TOTAL TIME: {end - start} s")

        # write the anonymization into a file
        Num_pub_transactions = ds.write_anonymized_ds([ds.public_transactions, ds.private_transactions])

        # Utility Loss
        N_Pub_item_After = len(ds.public_items)
        Utility_loss = 100 - ((N_Pub_item_After / N_Pub_item_before) * 100)
        logger.info(f"After: {N_Pub_item_After}")
        logger.info(f"Before: {N_Pub_item_before}")

        if args.m:
            option = f"m-{args.m}"
        elif args.top_x:
            option = f"Top_x-{args.top_x}"
        else:
            option = "Option-Unknown"

        # Prepare the object that will be converted to a Dataframe
        data_to_write = [
            {
                'h': h,
                'k': k,
                'p': p,
                'option': option,
                'total_time': end - start,
                'Utility Loss': Utility_loss,
                'pub_trans after anonymization': Num_pub_transactions,
                'rows': N_transactions
            }
        ]

        ds.write_performances(data_to_write)
