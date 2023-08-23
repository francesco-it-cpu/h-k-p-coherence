from Dataset import Dataset
from typing import Set

class HKP:

    def __init__(self, h :float, k :int, p :int):
        self.h = h
        self.k = k
        self.p = p

    def calculate_and_check_sup_greater(self, beta, dataset :Dataset):
        beta = set(beta)
        sup = 0
        for row in dataset.transactions:
            if beta.issubset(set(row)):
                sup+=1
        if sup > self.k:
            return True
        return False

    def calculate_breach(beta :set, dataset :Dataset):
        for el in beta:
            for row in dataset.transactions:
                for beta in dataset.public_item_list:
                    if beta.issubset(row): 
                            return                       
    
   
