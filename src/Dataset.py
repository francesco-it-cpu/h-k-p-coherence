from pathlib import Path
import os
import csv

class Dataset:
    def __init__(self, dataset_path):
        self.dataset_path = Path(dataset_path)

        pub_items = open(self.dataset_path / "pub.csv").read().split()
        self.public_items = frozenset(int(item) for item in pub_items)

        priv_items = open(self.dataset_path / "priv.csv").read().split()
        self.private_items = frozenset(int(item) for item in priv_items)

        self.transactions,self.public_transactions,self.private_transactions = self.build_transactions()

        self.size_one_moles = list()
        self.minimal_moles = dict()


    def build_transactions(self):
        """
        Build transactions by reading each line of pub.csv and priv.csv
        :return: A set of transactions,
        pub_transactions: transactions only with public items
        priv_transactions : transactions only with private items
        """
        public_list = open(self.dataset_path / "pub.csv").read().splitlines()
        private_list = open(self.dataset_path / "priv.csv").read().splitlines()

        pub_transactions = [frozenset([int(public_element) for public_element in public_line.split()]) for public_line in public_list]
        priv_transactions = [frozenset([int(private_element) for private_element in private_line.split()]) for private_line in
                           private_list]

        transactions = [pub_tr.union(priv_tr) for pub_tr,priv_tr in zip(pub_transactions, priv_transactions)]

        return transactions,pub_transactions,priv_transactions

    @staticmethod
    def write_anonymized_ds(transactions):
        cwd = os.getcwd()
        parent_dir = os.path.relpath(os.path.join(cwd, '../Datasets'))
        folder = os.path.join(parent_dir, 'Anonymized')

        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(f'{folder}/anon_pub.csv', 'w') as anon_pub, open(f'{folder}/anon_priv.csv','w') as anon_priv:
            pub_writer = csv.writer(anon_pub, delimiter=' ')
            priv_writer = csv.writer(anon_priv, delimiter=' ')
            for pub_sets,priv_sets in zip(transactions[0],transactions[1]):
                pub_writer.writerow(pub_sets)
                priv_writer.writerow(priv_sets)

        print(f"Wrote anonymized datasets to {folder}")

        file_path = f'{folder}/anon_pub.csv'

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                num_lines = sum(1 for line in file)
        else:
            num_lines = 0

        return num_lines
