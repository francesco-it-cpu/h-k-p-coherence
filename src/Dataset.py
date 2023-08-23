from pathlib import Path

class Dataset:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)
        self.public_items = set(open(self.dataset_path / "pub.dat").read().split())
        self.private_items = set(open(self.dataset_path / "priv.dat").read().split())

        self.transactions = self.build_transactions()

        self.size_one_moles = list()
        self.moles = None
        self.minimal_moles = dict()


    def build_transactions(self):
        public_list = open(self.dataset_path / "pub.dat").read().splitlines()
        private_list = open(self.dataset_path / "priv.dat").read().splitlines()
        transactions = [(public_line.split() + private_line.split()) for public_line, private_line in
                            zip(public_list, private_list)]
        return transactions

