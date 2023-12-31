from itertools import product
from Dataset import Dataset
from HKP import HKP
import logging
import time
from argparse import ArgumentParser
from Calculator import Calculator

if __name__ == '__main__':

    h_values1 = [0.3, 0.5]
    k_values1 = [2,4,8]
    p_values1 = [2, 3, 4, 5, 6]
    m_values1 = None
    top_x_values1 = [10, 15, 20, 25]

    # Calculate all possible combinations of h, k e p
    configurations1 = list(product(h_values1, k_values1, p_values1, top_x_values1))

    for config1 in configurations1:
        h, k, p, top_x = config1
        Calculator.calculator(h, k, p, m_values1, top_x)

    h_values = [0.3, 0.5]
    k_values = [2,4,8]
    p_values = [2, 3, 4, 5, 6]
    m_values=['half', 'suppress-all', 'only-max']
    top_x_values=None

    # Calculate all possible combinations of h, k e p
    configurations = list(product(h_values, k_values, p_values, m_values))

    for config in configurations:

        h, k, p, m = config
        Calculator.calculator(h,k,p,m,top_x_values)
