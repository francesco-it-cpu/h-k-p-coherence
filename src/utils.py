from Dataset import Dataset
""" def read_datasets(pub_path,priv_path):
    pub = open(pub_path).read()
    priv = open(priv_path).read()
    return [pub,priv] """

if __name__ == '__main__':
    #print(read_datasets('../Datasets/pub.dat', './Datasets/priv.dat'))
    print("test:")
    ds = Dataset("Datasets")
    print(ds.public_item_list)
