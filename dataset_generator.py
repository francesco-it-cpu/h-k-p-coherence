import argparse
import numpy as np
import pandas as pd

# Parse the command line arguments
parser = argparse.ArgumentParser(description='Generate two datasets made of random numbers and divide them into public and private according to arguments passed by CLI')
parser.add_argument('-row', type=int, help='Number of rows', required=True)
parser.add_argument('-cols', type=int, help='Number of columns for private dataset', required=True)
parser.add_argument('-dens', type=float, help='Density:how many cols pub and priv will have', required=True)


args = parser.parse_args()

pub_cols = int(args.dens*args.cols)
priv_cols = int(args.cols - pub_cols)

print(f"Using density of {int(args.dens*100)}%")
print(f"Generating pub.dat with {args.row} rows and {pub_cols} columns")
# Generate random numbers between 1 and 300 for public and private datasets
public_data = np.random.randint(low=1, high=799, size=(args.row, pub_cols))
print(f"Generating priv.dat with {args.row} rows and {priv_cols} columns")
private_data = np.random.randint(low=800, high=1000, size=(args.row, priv_cols))

# Create pandas dataframes for public and private datasets
public_df = pd.DataFrame(public_data)
private_df = pd.DataFrame(private_data)

# Print the dataframes
public_df.to_csv(f"./Datasets/pub.csv",sep=' ',index=False, header=False)
private_df.to_csv(f"./Datasets/priv.csv",sep=' ',index=False, header=False)
print("\nWrote everything to Datasets folder")
