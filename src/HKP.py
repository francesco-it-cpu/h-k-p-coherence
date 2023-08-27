from Dataset import Dataset
from collections import defaultdict
from itertools import combinations

class HKP:

    def __init__(self, h :float, k :int, p :int,dataset:Dataset):
        self.h = h
        self.k = k
        self.p = p
        self.dataset = dataset



    # ------------ Size-1 moles functions --------------

    def calculate_sup_size1_moles(self,beta):
        """
        Calculates the Support of Beta, only for speed reason
        :param beta: possible mole
        :return: support of Beta
        """
        beta = frozenset([beta])
        sup = 0
        for row in self.dataset.transactions:
            if beta.issubset(row) :
                sup+=1
        return sup

    def build_size_1_dict(self):
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
        for _beta in self.dataset.public_items:
            SupBeta_U_e_dict[_beta] = defaultdict(int)
            sup = self.calculate_sup_size1_moles(_beta)
            if sup != 0:
                SupBeta_dict[_beta] = sup
            else:
                continue

        for row in self.dataset.transactions:
            for beta in self.dataset.public_items:
                if beta in row:
                    for priv_item in self.dataset.private_items:
                        if priv_item in row:
                            SupBeta_U_e_dict[beta][priv_item] += 1

        return SupBeta_dict,SupBeta_U_e_dict

    def get_size1_moles(self):
        """
        Find size-1 moles based on the condition explained in the paper (either Sup(β)<k or Pbreach(β)>h)

        :return: the list of size_1 moles
        """
        size_1_moles = set()
        [SupBeta_dict, SupBeta_U_e_dict] = self.build_size_1_dict()
        for beta in SupBeta_dict:
            sup_Beta = SupBeta_dict[beta]
            priv_item_dict = SupBeta_U_e_dict[beta].values()
            sup_Beta_U_e = max(priv_item_dict, default=0)
            p_breach = sup_Beta_U_e / sup_Beta
            if sup_Beta < self.k or p_breach > self.h:
               size_1_moles.add(beta)
            else:
                continue

        return frozenset(size_1_moles)



    def eliminate_size_1_moles(self, size_1_moles_list):
        """
        Eliminate size-1 moles and also update public items and transactions
        :param size_1_moles_list: got from get_size1_moles
        :return:
        """
        without_size1_moles = []
        item_to_clean_from_transaction = []

        for row in self.dataset.transactions:
            for el in size_1_moles_list:
                if set([el]).issubset(row):
                    item_to_clean_from_transaction.append(el)


            cleaned_row = row.symmetric_difference(set(item_to_clean_from_transaction))
            without_size1_moles.append(cleaned_row)
            item_to_clean_from_transaction.clear()

        cleaned_pub_items = self.dataset.public_items.symmetric_difference(frozenset(size_1_moles_list))
        self.dataset.public_items = cleaned_pub_items
        self.dataset.transactions = without_size1_moles

        return cleaned_pub_items

    # ------------ Size-1 moles functions ending --------------


    # ------------ Size-n moles functions --------------

    def calculate_sup_size_n_moles(self,beta):
        """
        Calculates the Support of Beta, only for speed reason
        :param beta: possible mole
        :return: support of Beta
        """
        sup = 0
        for row in self.dataset.transactions:
            if beta.issubset(row) :
                sup+=1
        return sup

    def build_size_n_dict(self,possible_moles):
        """
        Calculate the Support of Beta Union e (private item) for size N moles

        :return: Two dictionaries :
                 SupBeta_dict : A dictionary,[key: each public_items, value: occurrencies], containing the support of all combos of public items
                 SupBeta_U_e_dict : A dictionary of dictionaries
                 [key: each combo of pub_items : {key : private_item, value: occurrencies of combos of pub_items together with priv_item}
        """
        SupBeta_U_e_dict = {}
        SupBeta_dict = {}

        for _beta in possible_moles:
            SupBeta_U_e_dict[_beta] = defaultdict(int)
            sup = self.calculate_sup_size_n_moles(_beta)
            if sup != 0:
                SupBeta_dict[_beta] = sup
            else:
                continue

        for row in self.dataset.transactions:
            for beta in possible_moles:
                if beta.issubset(row):
                    for priv_item in self.dataset.private_items:
                        if priv_item in row:
                            SupBeta_U_e_dict[beta][priv_item] += 1

        return SupBeta_dict,SupBeta_U_e_dict


    @staticmethod
    def create_combos(p, non_moles):
        """
        Create the set of all possible size-p moles
        :return: A set of possible moles
        """
        possible_moles = set()

        # Generate all combinations of length p
        for combo in combinations(non_moles, p):
            possible_moles.add(frozenset(combo))

        return possible_moles

    def get_moles(self,candidates,mole_list):
        """
        Find size-n moles based on the condition explained in the paper (either Sup(β)<k or Pbreach(β)>h)
        :return: list of moles and non moles
        """
        minimal_moles = set()
        non_moles = set()
        [SupBeta_dict,SupBeta_U_e_dict] = self.build_size_n_dict(candidates)
        for beta in SupBeta_dict:
            sup_Beta = SupBeta_dict[beta]
            priv_item_dict = SupBeta_U_e_dict[beta].values()
            sup_Beta_U_e = max(priv_item_dict,default=0)
            p_breach = sup_Beta_U_e / sup_Beta

            if sup_Beta < self.k or p_breach > self.h:
                flag = False
                for i,subset in mole_list.items():
                    for item in subset:
                        if item.issubset(beta):
                            flag = True
                            break
                if not flag:
                    minimal_moles.add(beta)
            else:
                non_moles.add(beta)

        return minimal_moles,non_moles

    # ------------ Size-n moles functions ending --------------

    def find_minimal_moles(self):

        M = dict()
        F = dict()

        i = 1
        print(f"Searching for size-1 moles...")
        size_1_moles = self.get_size1_moles()
        print(f"Found {len(size_1_moles)} size-1 moles \n {size_1_moles}\n")

        F_i = self.eliminate_size_1_moles(size_1_moles)
        F[i] = F_i

        i = 2

        while i <= self.p:
            if F_i == set([]):
                print(f"No size-{i} moles found\n")
                break
            else:
                C_i = self.create_combos(i,F_i)
                M_i,F_i = self.get_moles(C_i,M)
                M[i] = M_i
                # TODO: Print da aggiustare quando F_i é vuoto
                print(f"Found {len(M[i])} size-{i} moles\n {M_i}\n")
                i+=1

        return M,F

