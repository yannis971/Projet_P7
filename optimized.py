# -*- coding : utf8 -*-

import time
import pandas as pd


def calculate_and_print_knapsack(W, prices, profits, N, names):
    """
    Function tha resolve the 0-1 knapsack problem and prints the combination of items that matches
    """
    global START_TIME
    INTER_TIME = time.time()
    print("Partial Elapsed time 01 - avant init matrice: ", (INTER_TIME - START_TIME), "sec")

    matrice = [[0 for _ in range(W + 1)] for _ in range(N + 1)]

    INTER_TIME = time.time()
    print("Partial Elapsed time 02 - après init matrice: ", (INTER_TIME - START_TIME), "sec")

    for i in range(N + 1):
        for j in range(W + 1):
            if i == 0 or j == 0:
                matrice[i][j] = 0
            elif prices[i - 1] <= j:
                matrice[i][j] = max(profits[i - 1] + matrice[i - 1][j - prices[i - 1]], matrice[i - 1][j])
            else:
                matrice[i][j] = matrice[i - 1][j]

    INTER_TIME = time.time()
    print("Partial Elapsed time 03 - après alimentation matrice: ", (INTER_TIME - START_TIME), "sec")

    max_profit = matrice[N][W]
    print("Profit maximal = {:.2f} €".format(max_profit))

    j = min([j for j in range(W + 1) if matrice[N][j] == max_profit])
    print("Investissement = {:.2f} €".format(j / 100))

    for i in range(N, 0, -1):
        if max_profit <= 0:
            break
        if max_profit == matrice[i - 1][j]:
            continue
        else:
            print("{},{:.2f},{:.2f}".format(names[i - 1], prices[i - 1] / 100, profits[i - 1]))
            max_profit -= profits[i - 1]
            j -= prices[i - 1]


if __name__ == '__main__':
    START_TIME = time.time()
    df = pd.read_csv('data/dataset2_P7.csv')
    records = [(name, int(price * 100), profit, profit / price)
               for (name, price, profit) in df.to_records(index=False)
               if profit > 0 and price > 0]
    records.sort(key=lambda x: x[3], reverse=True)
    profits = [profit for (name, price, profit, _) in records]
    prices = [price for (name, price, profit, _) in records]
    names = [name for (name, price, profit, _) in records]
    W = 50000
    N = len(profits)
    calculate_and_print_knapsack(W, prices, profits, N, names)
    END_TIME = time.time()
    print("Total Elapsed time : ", (END_TIME - START_TIME), "sec")
    print("time.perf_counter() :", time.perf_counter())
    print("time.process_time() :", time.process_time())
