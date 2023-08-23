from pathlib import Path

class Dataset:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)
        self.public_item_list = open(self.dataset_path / "pub.dat").read().splitlines()
        self.private_item_list = open(self.dataset_path / "priv.dat").read().splitlines()

        self.transactions = self.build_transactions()

        self.size_one_moles = list()
        self.moles = None
        self.minimal_moles = dict()

    def build_transactions(self):
        transactions = []
        for row in range(len(self.private_item_list)):
            transaction = self.public_item_list[row] + " " + self.private_item_list[row]
            transactions.append(transaction)
        return transactions

