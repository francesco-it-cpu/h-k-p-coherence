class Dataset:
    def __init__(self,dataset_path):
        self.public_item_list = list(open(dataset_path/"pub.dat").read())
        self.private_item_list = list(open(dataset_path/"priv.dat").read())
        
        self.dataset_path = dataset_path

        self.transactions = self.Build_transactions()

        self.size_one_moles = list()
        self.moles = None  # list of minimal moles found in the dataset
        self.MinimalMoles = dict()
    
    def Build_transactions(self):
        for row in range(0,len(self.private_item_list)):
            print(self.private_item_list[row])
            self.transactions[row] = self.private_item_list[row].append(self.public_item_list[row])

        
