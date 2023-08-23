import argparse
import numpy as np
import pandas as pd

# Parse the command line arguments
parser = argparse.ArgumentParser(description='Generate two datasets made of random numbers and divide them into public and private according to arguments passed by CLI')
parser.add_argument('-row', type=int, help='Number of rows', required=True)
parser.add_argument('-pu', type=int, help='Number of columns for public dataset', required=True)
parser.add_argument('-pv', type=int, help='Number of columns for private dataset', required=True)
args = parser.parse_args()

# Generate random numbers between 1 and 300 for public and private datasets
public_data = np.random.randint(low=1, high=300, size=(args.row, args.pu))
private_data = np.random.randint(low=1, high=300, size=(args.row, args.pv))

# Create pandas dataframes for public and private datasets
public_df = pd.DataFrame(public_data)
private_df = pd.DataFrame(private_data)

# Print the dataframes
public_df.to_csv(f"Dataset/pub.dat",sep=' ',index=False, header=False)
private_df.to_csv(f"Dataset/priv.dat",sep=' ',index=False, header=False)
print("Datasets wrote to Dataset folder")
