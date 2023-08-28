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

        self.il = SupBeta_dict
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

        for row in self.dataset.public_transactions:
            for el in size_1_moles_list:
                if set([el]).issubset(row):
                    item_to_clean_from_transaction.append(el)


            cleaned_row = row.symmetric_difference(set(item_to_clean_from_transaction))
            without_size1_moles.append(cleaned_row)
            item_to_clean_from_transaction.clear()

        cleaned_pub_items = self.dataset.public_items.symmetric_difference(frozenset(size_1_moles_list))
        self.dataset.public_items = cleaned_pub_items
        self.dataset.public_transactions = without_size1_moles
        self.dataset.transactions = [pub_trans.union(priv_trans) for pub_trans,priv_trans in zip(without_size1_moles,self.dataset.private_transactions) if pub_trans!=frozenset()]

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
        for row in self.dataset.public_transactions:
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
        MM = defaultdict(int)


        i = 1
        print(f"Searching for size-1 moles...")
        size_1_moles = self.get_size1_moles()
        print(f"Found {len(size_1_moles)} size-1 moles \n {size_1_moles}\n")

        F_i = self.eliminate_size_1_moles(size_1_moles)
        F[i] = F_i

        i = 2

        while i <= self.p:
            if F_i == set():
                print(f"No size-{i} moles found\n")
                break
            else:
                C_i = self.create_combos(i,F_i)
                M_i,F_i = self.get_moles(C_i,M)
                M[i] = M_i


                # --------  Update the elements_in_moles dictionary for size-1 moles

                for mole in M_i:
                    for element in mole:
                        MM[element] = MM.get(element, 0) + 1

                # ------------------------------------------------------------------
                if M_i == set():
                    print(f"No size-{i} moles found\n")
                    break

                print(f"Found {len(M[i])} size-{i} moles\n {M_i}\n")
                i+=1

        return M,F,MM

    """
    def calculate_MM(self, minimal_moles):

        MM = {}

        for item in minimal_moles.values():
            for minimal in item:
                for el in minimal:
                    MM.setdefault(el, 0)

        for p, item in minimal_moles.items():
            for minimal in item:
                for el in minimal:
                    MM[el] += 1
        return MM

    """
    def suppress_MM(self,minimal_moles:dict):

        without_MM = []
        item_to_clean_from_transaction = []

        for row in self.dataset.public_transactions:
            for p,moles in minimal_moles.items():
                for mole in moles:
                    for el in mole:
                        if set([el]).issubset(row):
                            item_to_clean_from_transaction.append(el)


            cleaned_row = row.symmetric_difference(set(item_to_clean_from_transaction))
            without_MM.append(cleaned_row)
            item_to_clean_from_transaction.clear()

        self.dataset.transactions = [pub_trans.union(priv_trans) for pub_trans,priv_trans in zip(without_MM,self.dataset.private_transactions)]


    def IL(self):
        dict_IL=defaultdict(int)
        for item in self.dataset.public_transactions:
            for el in item:
                dict_IL[el]=self.calculate_sup_size1_moles(el)

        return dict_IL


    def morte(self,IL,MM,minimal_moles):

        division=defaultdict(int)
        single_mole=set()
        for p,item in minimal_moles.items():
            for minimal in item:
                for el in minimal:
                    single_mole.add(el)

        for _item in single_mole:
            division[_item]= MM[_item]/IL[_item]

        # Get half of the elements or just one element if there's only one
        sorted_division = sorted(division.items(), key=lambda x: x[1], reverse=True)
        num_elements = len(sorted_division)

        if num_elements == 1:
            selected_elements = [sorted_division[0][0]]  # Only one element
        else:
            selected_elements = [key for key, _ in sorted_division[:num_elements // 2]]

        cleaned_pub_items = self.eliminate_size_1_moles(selected_elements)

        """
         # Get the top 10 elements or all elements if there are fewer than 10
        sorted_division = sorted(division.items(), key=lambda x: x[1], reverse=True)
        top_10_elements = [key for key, _ in sorted_division[:10]]
        cleaned_pub_items = self.eliminate_size_1_moles(top_10_elements)
        """

        """
        # Get only the Max element
        max_value=max(division.values())
        keys_with_max_value = [key for key, value in division.items() if value == max_value]
        cleaned_pub_items=self.eliminate_size_1_moles(keys_with_max_value)
        """

        return selected_elements, cleaned_pub_items