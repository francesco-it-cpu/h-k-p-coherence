# h-k-p-Coherence
Our implementation of h-k-p-Coherence anonymization algorithm described [here](https://www.researchgate.net/publication/221653414_Anonymizing_transaction_databases_for_publication)

# Usage

### Clone the repository 
```
git clone https://github.com/francesco-it-cpu/h-k-p-coherence && cd h-k-p-coherence/src
```
### Example
```
python3 main.py --h 0.4 --k 2 --p 2 -m half
```
There are different methods you can use to suppress minimal moles, either you can use -m and add one of these options
- suppress-all : _suppress all public items that are contained in minimal moles_
- half : _suppress half of the public items based on max(MM/IL) condition_
- only-max : _suppress only the max(MM/IL) public items in the minimal moles till anonymization is reached_

or you can use -top_x [n] (-top_x 10 for example) to suppress the top n public items always based on max(MM/IL)

# Optional
In addition you can generate new pub.csv and priv.csv using 
dataset generator script

```
python3 dataset_generator.py -row 1000 -cols 20 -dens 0.2
```
In this example a 1000 x 4 pub.csv and 1000 x 16 priv.csv would be generated

## Authors
_Flavio Bava_ </br>
_Francesco Ciarlo_ </br>
_Edoardo Oldrini_ </br>

