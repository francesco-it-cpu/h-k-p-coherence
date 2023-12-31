from Dataset import Dataset
from collections import defaultdict
from itertools import combinations
import logging

class HKP:

    def __init__(self, h :float, k :int, p :int,dataset:Dataset):
        self.h = h
        self.k = k
        self.p = p
        self.dataset = dataset

        #logger = logging.getLogger("HKP-Anonymizer")
        #self.logger = logger


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
        item_to_clean_from_transaction = []
        idx_to_remove = set()
        for idx,row in enumerate(self.dataset.transactions):
            for el in size_1_moles_list:
                if set([el]).issubset(row):
                    item_to_clean_from_transaction.append(el)
            cleaned_row = row.symmetric_difference(set(item_to_clean_from_transaction))
            # If the len of sets is different, it means that pub_items were in cleaned_row and
            #  were excluded by the 'difference' operation
            if len(cleaned_row) == len(cleaned_row.difference(self.dataset.public_items)):
                self.dataset.transactions[idx] = frozenset()
            else:
                self.dataset.transactions[idx] = cleaned_row
            item_to_clean_from_transaction.clear()
        symmetric_diff = self.dataset.public_items.symmetric_difference(frozenset(size_1_moles_list))
        cleaned_pub_items = symmetric_diff if symmetric_diff != frozenset() else set()
        self.dataset.public_items = cleaned_pub_items
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
        :return: list of minimal moles and non moles
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
        """
        Calculate all the minimal_moles after called the 'eliminate_size1_moles' function
        :return:
        MM: a dictionary:
            key: i-th public item inside the list of the minimal moles
            value: the number of minimal moles containing the i-th public item
        F: first of all contains the size_1 moles, after cicles will contain all the size-i non moles
        M: all the minimal moles
        """

        M = dict()
        F = dict()
        MM = defaultdict(int)


        i = 1

        #self.logger.info("Finding size one moles...\n")
        size_1_moles = self.get_size1_moles()
        #self.logger.info(f"Found {len(size_1_moles)} -->> {size_1_moles}\n")

        #self.logger.info("Suppressing size-1 moles...\n")
        F_i = self.eliminate_size_1_moles(size_1_moles)
        #self.logger.info(f"Size-1 moles suppression completed\n")

        F[i] = F_i

        i = 2

        while i <= self.p:
            if F_i == set():
                #self.logger.info(f"No size-{i} moles found")
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
                    #self.logger.info(f"No size-{i} moles found\n")
                    break

                #self.logger.info(f"Found {len(M[i])} size-{i} moles\n")
                i+=1

        return M,F,MM

    def suppress_MM(self,minimal_moles:dict, m=None,top_x=None,IL=None,MM=None ):
        """

        :param minimal_moles: all the minimal moles
        :param m: args passed through the command line
        :param top_x: args passed through the command line
        :param IL: A dictionary containing:
                        key: i-th public item
                        value: Sup of the i-th public item
        :param MM: a dictionary:
            key: i-th public item inside the list of the minimal moles
            value: the number of minimal moles containing the i-th public item
        :return: depends on the match:
            top_x_elements: return each time the top x elements of the dictionary (from the max to the 'x', selected via cmd line by the user)
            selected_elements: return each time the half size of the 'sorted_division' array
            keys_with_max_value: return each time the max value of the 'sorted_division' array
        """

        if m is None and top_x is not None:
            division = self.prepare_data(minimal_moles, MM, IL)
            # Verify if top_x choosen is greater than len of division
            if top_x > len(division):
                top_x = len(division)  # set top_x to the len of division
            # Get the top 10 elements or all elements if there are fewer than 10
            sorted_division = sorted(division.items(), key=lambda x: x[1], reverse=True)
            top_x_elements = [key for key, _ in sorted_division[:top_x]]

            self.eliminate_size_1_moles(top_x_elements)
            #self.logger.info(f"Suppressing Item(s) with max MM/IL: {top_x_elements}\n")

            return top_x_elements

        else:
            match m:
                case 'suppress-all':
                    single_mole = set()
                    for p, item in minimal_moles.items():
                        for minimal in item:
                            for el in minimal:
                                single_mole.add(el)

                    self.eliminate_size_1_moles(single_mole)

                case 'half':

                    division=self.prepare_data(minimal_moles,MM,IL)
                    # Get half of the elements or just one element if there's only one
                    sorted_division = sorted(division.items(), key=lambda x: x[1], reverse=True)
                    num_elements = len(sorted_division)

                    if num_elements == 1:
                        selected_elements = [sorted_division[0][0]]  # Only one element
                    else:
                        selected_elements = [key for key, _ in sorted_division[:num_elements // 2]]

                    #self.logger.info(f"Suppressing Item(s) with max MM/IL: {selected_elements}\n")
                    self.eliminate_size_1_moles(selected_elements)

                    return selected_elements

                case 'only-max':

                    division = self.prepare_data(minimal_moles, MM, IL)
                    # Get only the Max element
                    max_value=max(division.values())
                    keys_with_max_value = [key for key, value in division.items() if value == max_value]

                    self.eliminate_size_1_moles(keys_with_max_value)
                    #self.logger.info(f"Suppressing Item(s) with max MM/IL: {keys_with_max_value}\n")

                    return keys_with_max_value

                case _:
                    print(f"Invalid option selected! {m}")
                    exit()


    def IL(self):
        """
        A function to calculate the IL for each remaining public item in the dataset
        :return: a dictionary containing:
                key: i-th public item
                value: IL associated to the i-th public item
        """
        dict_IL=defaultdict(int)
        for item in self.dataset.public_items:
            il = self.calculate_sup_size1_moles(item)
            if il != 0:
                dict_IL[item]= il
            else:
                continue

        return dict_IL

    def prepare_data(self,minimal_moles,MM,IL):
        """
        For each public item in the minimal moles, calculate MM/IL
        :param minimal_moles:
              :param IL: A dictionary containing:
                        key: i-th public item
                        value: Sup of the i-th public item
        :param MM: a dictionary:
            key: i-th public item inside the list of the minimal moles
            value: the number of minimal moles containing the i-th public item
        :return: a dictionary:
                key: the i-th public item in the minimal moles array
                value: the division associated to him
        """
        division = defaultdict(int)
        single_mole = set()
        for p, item in minimal_moles.items():
            for minimal in item:
                for el in minimal:
                    single_mole.add(el)

        for _item in single_mole:
            division[_item] = MM[_item] / IL[_item]

        return division

