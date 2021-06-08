# -*- coding : utf8 -*-
"""
    Program optimized.py that resolves the 0-1 knapsack problem using the dynamic programming method
"""

import argparse
import sys
import time
import pandas as pd


def parse_arguments():
    """
    Function that parses arguments for the program
    @return: None
    """
    message = """indiquer chemin vers le fichier csv à traiter  : exemple 'data/dataset1_P7.csv'"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help=message)
    return parser.parse_args()


def help_message():
    """
    Function that prints help message on how to use the program
    @return: None
    """
    print("\nProgramme optimized.py Projet P7 du parcours DA Python")
    print("\nAuteur : Yannis Saliniere")
    print("\nLicense : GNU GPL V3")
    print("\nusage: optimized.py [-h] [-f FILE]\n")
    print("  -h, --help \t\t show this help message and exit")
    print("  -f FILE, --file FILE")
    print("\t\t\t chemin vers le fichier_csv csv à traiter ")


def calculate_and_print_knapsack(max_weight: int, items: [], results_file) -> None:
    """
    Function that resolves the 0-1 knapsack problem and prints the combination of items that gives
    the best profit for weight of selected items less or equal to max_weight
    @param max_weight: int
    @param items: list
    @param results_file: str
    """

    number_of_items = len(items)  # number of items
    min_weight = items[-1][1]  # minimum weight is the last item's price
    knapsacks = [0] * (max_weight + 1)
    matrices = [[0] * (max_weight + 1) for _ in range(number_of_items + 1)]

    for i in range(1, number_of_items + 1):
        (_, price, profit, _) = items[i - 1]
        for j in range(max_weight, 0, -1):
            if price <= j:
                knapsacks[j] = max(knapsacks[j], knapsacks[j - price] + profit)
            matrices[i][j] = knapsacks[j]
        # Quit the loop when max profit is found
        # i.e. when the line from where the last knapsacks index between
        # (max_weight - min_weight) and max_weight do not vary anymore
        if matrices[i][(max_weight - min_weight):] == matrices[i - 1][(max_weight - min_weight):]:
            number_of_items = i
            break

    max_profit = knapsacks[max_weight]
    j = min([j for j in range(max_weight + 1) if knapsacks[j] == max_profit])

    with open(results_file, 'w', encoding='utf-8') as file:
        file.write(f'Profit maximal = {max_profit:.2f} €\n')
        file.write(f'Investissement = {(j / 100):.2f} €\n')
        file.write('Liste des actions\n')
        for i in range(number_of_items, 0, -1):
            if max_profit <= 0:
                break
            if max_profit == matrices[i - 1][j]:
                continue
            (name, price, profit, _) = items[i - 1]
            file.write(f'{name}\n')
            max_profit -= profit
            j -= price


if __name__ == '__main__':
    args = parse_arguments()
    if not args.file:
        help_message()
        sys.exit(0)
    START_TIME = time.time()
    data_frame = pd.read_csv(args.file)

    # create a list of items from data_frame adding a column ration (profit/price)
    records = [(name, int(price * 100), profit, profit / price)
               for (name, price, profit) in data_frame.to_records(index=False)
               if profit > 0 and price > 0]

    # sort items on ratio (profit/price) decreasing order
    records.sort(key=lambda x: x[3], reverse=True)

    # path to file results
    RESULTS_FILE = args.file.replace("data/", "results/results_").replace("csv", "txt")

    # call the function that resolves the 0-1 knapsack problem
    calculate_and_print_knapsack(50000, records, RESULTS_FILE)

    END_TIME = time.time()
    # print elapsed time
    print(f'Total elapsed time  : {END_TIME - START_TIME} sec')
    # print process_time() : the sum of the system and user CPU time used by the program
    print(f'time.process_time() : {time.process_time()} sec')
    # print perf_counter() : performance counter
    print(f'time.perf_counter() : {time.perf_counter()} sec')
    print(f'You can view the results in file {RESULTS_FILE}')
