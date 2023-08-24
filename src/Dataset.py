from pathlib import Path

class Dataset:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

        pub_items = open(self.dataset_path / "pub.dat").read().split()
        self.public_items = set([int(item) for item in pub_items])

        priv_items = open(self.dataset_path / "priv.dat").read().split()
        self.private_items = set([int(item) for item in priv_items])

        self.transactions = self.build_transactions()

        self.size_one_moles = list()
        self.moles = None
        self.minimal_moles = dict()


    def build_transactions(self):
        public_list = open(self.dataset_path / "pub.dat").read().splitlines()
        private_list = open(self.dataset_path / "priv.dat").read().splitlines()
        transactions = [set(
            [int(public_element) for public_element in public_line.split()] +
            [int(private_element) for private_element in private_line.split()])
            for public_line, private_line in zip(public_list, private_list)
        ]
        return transactions

