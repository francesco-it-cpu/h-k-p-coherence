from Dataset import Dataset
from HKP import HKP
import logging
import time

class Calculator:

    @staticmethod
    def calculator(h:float,k:int,p:int,m=None,top_x=None):

        ds = Dataset("../Datasets/")
        N_Pub_item_before = len(ds.public_items)

        hkp = HKP(h, k, p, ds)
        print(type(p))

        start = time.time()
        minimal_moles, non_moles, MM = hkp.find_minimal_moles()
        IL = hkp.IL()

        # if there are Minimal moles
        while len(MM) != 0:
            el = hkp.suppress_MM(minimal_moles, m, top_x, IL, MM)
            minimal_moles, non_moles, MM = hkp.find_minimal_moles()
            if len(MM) != 0:
                IL = hkp.IL()


        end = time.time()

        # write the anonymization into a file
        Num_pub_transactions = ds.write_anonymized_ds(ds.transactions)

        # Utility Loss
        N_Pub_item_After = len(ds.public_items)
        Utility_loss = 100 - ((N_Pub_item_After / N_Pub_item_before) * 100)

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
                    'Number of transactions': Num_pub_transactions,
                }
            ]

            ds.write_performances(data_to_write)