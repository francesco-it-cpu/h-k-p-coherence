from pathlib import Path

class Dataset:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

        pub_items = open(self.dataset_path / "pub.dat").read().split()
        self.public_items = frozenset(int(item) for item in pub_items)

        priv_items = open(self.dataset_path / "priv.dat").read().split()
        self.private_items = frozenset(int(item) for item in priv_items)

        self.transactions = self.build_transactions()

        self.size_one_moles = list()
        self.minimal_moles = dict()


    def build_transactions(self):
        """
        Build transactions by reading each line of pub.dat and priv.dat
        :return: A set of transactions
        """
        public_list = open(self.dataset_path / "pub.dat").read().splitlines()
        private_list = open(self.dataset_path / "priv.dat").read().splitlines()
        transactions = [frozenset(
            [int(public_element) for public_element in public_line.split()] +
            [int(private_element) for private_element in private_line.split()])
            for public_line, private_line in zip(public_list, private_list)
        ]
        return transactions

