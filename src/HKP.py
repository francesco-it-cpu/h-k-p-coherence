from Dataset import Dataset
from collections import defaultdict
from itertools import combinations

class HKP:

    def __init__(self, h :float, k :int, p :int):
        self.h = h
        self.k = k
        self.p = p

    def calculate_sup(self, beta, dataset :Dataset):
        """
        Calculates the Support of Beta
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

    def calculate_p_breach_size1moles(self, dataset):
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
        for beta in dataset.public_items:
            SupBeta_U_e_dict[beta] = defaultdict(int)
            SupBeta_dict[beta] = self.calculate_sup([beta],dataset)

        for row in dataset.transactions:
            for beta in dataset.public_items:
                if beta in row:
                    for priv_item in dataset.private_items:
                        if priv_item in row:
                            SupBeta_U_e_dict[beta][priv_item] += 1

        return SupBeta_dict,SupBeta_U_e_dict


    def calculate_p_breach_sizeNmoles(self, dataset):
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
            SupBeta_dict[_beta] = self.calculate_sup(_beta,dataset)

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
            for r in range(1, len(public_items) + 1):
                for combo in combinations(public_items, p):
                    possible_moles.append(combo)
            p += 1

        return set(possible_moles)

    def get_moles(self,dataset):
        """
        Find moles based on the condition explained in the paper (either Sup(β)<k or Pbreach(β)>h)
        :param dataset: dataset
        :return: list of moles and non moles
        """
        moles = []
        non_moles = []
        [SupBeta_dict,SupBeta_U_e_dict] = self.calculate_p_breach_sizeNmoles(dataset)
        for pairs in zip(SupBeta_dict,SupBeta_U_e_dict.values()):
            beta = pairs[0]
            sup_Beta = SupBeta_dict[beta]
            sup_Beta_U_e = max(pairs[1].values())
            p_breach = sup_Beta_U_e / sup_Beta
            if sup_Beta < self.k or p_breach > self.h:
                moles.append(beta)
            else:
                non_moles.append(beta)

        return moles,non_moles