from Dataset import Dataset
from HKP import HKP
import logging
import time

class Calculator:

    @staticmethod
    def calculator(h:float,k:int,p:int,m=None,top_x=None):

        logging.basicConfig(level=logging.DEBUG, format='%(name)s [%(levelname)s] >> %(message)s')
        logger = logging.getLogger("HKP-Anonymizer")
        logger.debug("Loading Dataset...")
        ds = Dataset("../Datasets/")
        N_Pub_item_before = len(ds.public_items)
        N_transactions = len(ds.transactions)

        hkp = HKP(h, k, p, ds)
        print(type(p))

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
                el = hkp.suppress_MM(minimal_moles, m, top_x, IL, MM)
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

        if m:
            option = f"m-{m}"
        elif top_x:
            option = f"Top_x-{top_x}"
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