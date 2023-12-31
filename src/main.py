from Dataset import Dataset
from HKP import HKP
import logging
import time
from argparse import ArgumentParser,RawTextHelpFormatter


if __name__ == '__main__':

    # Parse the command line arguments
    parser = ArgumentParser(
        description='Using different options to anonymize the dataset, according to arguments passed by CLI',
        formatter_class=RawTextHelpFormatter)

    # Add arguments for h, k, and p
    parser.add_argument('--h', type=float, default=0.8, help='Specify the value for h')
    parser.add_argument('--k', type=int, default=2, help='Specify the value for k')
    parser.add_argument('--p', type=int, default=2, help='Specify the value for p')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', type=str,choices=['suppress-all','half','only-max'],
    help="""    suppress-all : suppress all public items in the minimal moles
    half : suppress half of the public items in the minimal moles based on max(MM/IL)
    only-max : suppress only the max(MM/IL) public items in the minimal moles till anonymization is reached""")
    group.add_argument('-top_x', type=int, help='\nSpecify how much top_x values wil be remove')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG,format='%(name)s [%(levelname)s] >> %(message)s')
    logger = logging.getLogger("HKP-Anonymizer")

    logger.debug("Loading Dataset...")
    ds = Dataset("../Datasets")
    N_Pub_item_before = len(ds.public_items)

    hkp = HKP(args.h,args.k,args.p,ds)

    start = time.time()
    minimal_moles,non_moles,MM = hkp.find_minimal_moles()
    IL = hkp.IL()

    logger.info(f"minimal moles are: {minimal_moles}\n")
    
    #if there are Minimal moles
    while len(MM) != 0:
         el=hkp.suppress_MM(minimal_moles,args.m,args.top_x,IL,MM)
         print(f"Suppressing item(s): {el}")
         minimal_moles, non_moles, MM = hkp.find_minimal_moles()
         if len(MM) != 0:
            IL = hkp.IL()
            logger.info(f"minimal moles are: {minimal_moles}\n")

    end = time.time()
    logger.debug(f"TOTAL TIME: {end - start} s")

    #write the anonymization into a file
    Num_pub_transactions=ds.write_anonymized_ds(ds.transactions)

    #Utility Loss
    N_Pub_item_After=len(ds.public_items)
    Utility_loss=100-((N_Pub_item_After/N_Pub_item_before)*100)
    logger.info(f"Public after anonymization: {N_Pub_item_After}")
    logger.info(f"Public before anonymization: {N_Pub_item_before}")

    if args.m:
        option = f"m-{args.m}"
    elif args.top_x:
        option = f"Top_x-{args.top_x}"
    else:
        option = "Option-Unknown"

    # Prepare the object that will be converted to a Dataframe
    """
    data_to_write = [
        {
        'h': args.h,
        'k': args.k,
        'p': args.p,
        'option': option,
        'total_time' : end - start,
        'Utility Loss': Utility_loss,
        'Number of transactions' : Num_pub_transactions,
        }
    ]

    ds.write_performances(data_to_write)
    """

