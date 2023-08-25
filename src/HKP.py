from Dataset import Dataset
from collections import defaultdict
from itertools import combinations

class HKP:

    def __init__(self, h :float, k :int, p :int):
        self.h = h
        self.k = k
        self.p = p



    # ------------ Size-1 moles functions --------------
    def calculate_sup_size1_moles(self, beta, dataset :Dataset):
        """
        Calculates the Support of Beta, only for speed reason
        :param beta: possible mole
        :param dataset: dataset
        :return: support of Beta
        """
        sup = 0
        beta = set([beta])
        for row in dataset.transactions:
            if beta.issubset(set(row)) :
                sup+=1
        return sup

    def get_size1_candidates(self, dataset):
        """
        Calculate the Support of Beta Union e (private item)
        :param dataset: dataset
        :return: Two dictionaries :
                 SupBeta_dict : A dictionary,[key: each public_items, value: occurrencies], containing the support of all public items
                 SupBeta_U_e_dict : A dictionary of dictionaries
                 [key: each pub_item : {key : private_item, value: occurrencies of pub_item together with priv_item}
        """
        SupBeta_U_e_dict = {}
        SupBeta_dict = {}
        for _beta in dataset.public_items:
            SupBeta_U_e_dict[_beta] = defaultdict(int)
            sup = self.calculate_sup_size1_moles(_beta,dataset)
            if sup != 0:
                SupBeta_dict[_beta] = self.calculate_sup_size1_moles(_beta,dataset)
            else:
                continue

        for row in dataset.transactions:
            for beta in dataset.public_items:
                if beta in row:
                    for priv_item in dataset.private_items:
                        if priv_item in row:
                            SupBeta_U_e_dict[beta][priv_item] += 1

        return SupBeta_dict,SupBeta_U_e_dict

    def get_size1_moles(self,dataset):
        """
        Find size-1 moles based on the condition explained in the paper (either Sup(β)<k or Pbreach(β)>h)
        :param dataset:
        :return:
        """
        size_1_moles = []
        [SupBeta_dict, SupBeta_U_e_dict] = self.get_size1_candidates(dataset)
        for pairs in zip(SupBeta_dict, SupBeta_U_e_dict.values()):
            beta = pairs[0]
            sup_Beta = SupBeta_dict[beta]
            sup_Beta_U_e = max(pairs[1].values(), default=0)
            p_breach = sup_Beta_U_e / sup_Beta
            if sup_Beta < self.k or p_breach > self.h:
               size_1_moles.append(beta)
            else:
                continue

        return size_1_moles


    def eliminate_size_1_moles(self,dataset,size_1_moles_list):
        """
        Eliminate size-1 moles and also update public items and transactions
        :param dataset: dataset
        :param size_1_moles_list: got from get_size1_moles
        :return:
        """
        without_size1_moles = []
        item_to_clean_from_transaction = []

        for row in dataset.transactions:
            for el in size_1_moles_list:
                if set([el]).issubset(row):
                    item_to_clean_from_transaction.append(el)


            cleaned_row = row.symmetric_difference(set(item_to_clean_from_transaction))
            without_size1_moles.append(cleaned_row)
            item_to_clean_from_transaction.clear()

        dataset.public_items = dataset.public_items.symmetric_difference(set(size_1_moles_list))
        dataset.transactions = without_size1_moles

        return without_size1_moles

    # ------------ Size-1 moles functions ending --------------


    # ------------ Size-n moles functions --------------
    def calculate_sup_size_n_moles(self, beta, dataset :Dataset):
        """
        Calculates the Support of Beta, only for speed reason
        :param beta: possible mole
        :param dataset: dataset
        :return: support of Beta
        """
        sup = 0
        beta = set(beta)
        for row in dataset.transactions:
            if beta.issubset(set(row)) :
                sup+=1
        return sup

    def get_size_n_candidates(self, dataset):
        """
        Calculate the Support of Beta Union e (private item) for size N moles
        :param dataset: dataset
        :return: Two dictionaries :
                 SupBeta_dict : A dictionary,[key: each public_items, value: occurrencies], containing the support of all combos of public items
                 SupBeta_U_e_dict : A dictionary of dictionaries
                 [key: each combo of pub_items : {key : private_item, value: occurrencies of combos of pub_items together with priv_item}
        """
        SupBeta_U_e_dict = {}
        SupBeta_dict = {}
        possible_moles = self.create_combos(dataset.public_items)
        for _beta in possible_moles:
            SupBeta_U_e_dict[_beta] = defaultdict(int)
            sup = self.calculate_sup_size_n_moles(_beta,dataset)
            if sup != 0:
                SupBeta_dict[_beta] = sup
            else:
                continue

        for row in dataset.transactions:
            for beta in possible_moles:
                if set(beta).issubset(row):
                    for priv_item in dataset.private_items:
                        if priv_item in row:
                            SupBeta_U_e_dict[beta][priv_item] += 1

        return SupBeta_dict,SupBeta_U_e_dict



    def create_combos(self,public_items):
        """
        Create the set of all possible size-p moles
        :param public_items: list of public items
        :return: A set of possible moles
        """
        possible_moles = []
        p = 2
        while p <= self.p:
            # Generate all combinations of different lengths
            for combo in combinations(public_items, p):
                possible_moles.append(combo)
            p += 1

        return set(possible_moles)

    def get_moles(self,dataset):
        """
        Find size-n moles based on the condition explained in the paper (either Sup(β)<k or Pbreach(β)>h)
        :param dataset: dataset
        :return: list of moles and non moles
        """
        moles = []
        non_moles = []
        [SupBeta_dict,SupBeta_U_e_dict] = self.get_size_n_candidates(dataset)
        for pairs in zip(SupBeta_dict,SupBeta_U_e_dict.values()):
            beta = pairs[0]
            sup_Beta = SupBeta_dict[beta]
            sup_Beta_U_e = max(pairs[1].values(),default=0)
            p_breach = sup_Beta_U_e / sup_Beta
            if sup_Beta < self.k or p_breach > self.h:
                moles.append(beta)
            else:
                non_moles.append(beta)

        return moles,non_moles

    # ------------ Size-n moles functions ending --------------