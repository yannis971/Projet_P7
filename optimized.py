# -*- coding : utf8 -*-

import time
import pandas as pd


def calculate_and_print_knapsack(W, records):
    """
    Function that resolves the 0-1 knapsack problem and prints the combination of items that matches
    """

    N = len(records)

    knap_sack = [0 for _ in range(W + 1)]
    matrice = [[0 for _ in range(W + 1)] for _ in range(N + 1)]

    for i in range(1, N + 1):
        for j in range(W, 0, -1):
            (name, weight, value, _) = records[i - 1]
            if weight <= j:
                knap_sack[j] = max(knap_sack[j], knap_sack[j - weight] + value)
            matrice[i][j] = knap_sack[j]
        # Quit the loop when max profit is found
        if matrice[i][W] == matrice[i][W - 1] and matrice[i][W] == matrice[i-1][W]:
            N = i
            break

    max_profit = knap_sack[W]
    print("Profit maximal = {:.2f} €".format(max_profit))

    j = min([j for j in range(W + 1) if knap_sack[j] == max_profit])
    print("Investissement = {:.2f} €".format(j / 100))

    print("Listes des actions (name)")
    for i in range(N, 0, -1):
        if max_profit <= 0:
            break
        if max_profit == matrice[i - 1][j]:
            continue
        else:
            (name, price, profit, _) = records[i-1]
            print(name)
            max_profit -= profit
            j -= price


if __name__ == '__main__':
    START_TIME = time.time()
    data_frame = pd.read_csv('data/dataset2_P7.csv')

    # create a list of records from data_frame adding a column ration (profit/price)
    records = [(name, int(price * 100), profit, profit / price)
               for (name, price, profit) in data_frame.to_records(index=False)
               if profit > 0 and price > 0]

    # sort items on ratio (profit/price) decreasing order
    records.sort(key=lambda x: x[3], reverse=True)

    # call the function that resolves the knapsack problem
    calculate_and_print_knapsack(50000, records)

    END_TIME = time.time()
    # print elapsed time
    print("Total elapsed time  : ", (END_TIME - START_TIME), "sec")
    # print process_time() : the sum of the system and user CPU time used by the program
    print("time.process_time() :", time.process_time(), "sec")
    # print perf_counter() : performance counter
    print("time.perf_counter() :", time.perf_counter(), "sec")
