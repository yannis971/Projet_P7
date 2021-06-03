# -*- coding : utf8 -*-

import sys
import time
import pandas as pd

START_TIME = time.time()
df = pd.read_csv('data/dataset1_P7.csv')
df.sort_values(by=['profit', 'price'], ascending=True, inplace=True)
records = [(name, price, profit) for (name, price, profit) in df.loc[df['price'] > 0].to_records(index=False)]

N = len(records)    # Nombre d'actions
W = 501             # Investissement maximal + 1

# Initialisation de la matrice de données
matrice = [[0 for _ in range(W)] for _ in range(N)]

# Initialisation de la première ligne de la matrice
(_, weight, value) = records[0]
for j in range(0, W, 1):
    if j < int(weight):
        matrice[0][j] = 0
    else:
        matrice[0][j] = value

# Boucle d'alimentation de la matrice avec les combinaisons d'actions
for i in range(1, N, 1):
    (_, weight, value) = records[i]
    for j in range(0, W, 1):
        if j < int(weight):
            matrice[i][j] = matrice[i - 1][j]
        else:
            matrice[i][j] = max((value + matrice[i - 1][j - int(weight)]), matrice[i - 1][j])

# Détermination du profit maximal et de l'investissement correspondant
max_profit = max(matrice[-1])
investment = min([j for j in range(W) if matrice[-1][j] == max_profit])
print("Le profit maximum est obtenu pour un investissement de {:.2f} €. Ce profit atteint la valeur de {:.2f} €.".format(investment, max_profit))

INTER_TIME = time.time()
print("Partial Elapsed time : ", (INTER_TIME-START_TIME), "sec")

# Affichage de la combinaison d'actions
print("La combinaison d'actions est la suivante :")
while max_profit > 0:
    try:
        (i, j) = min([(i, j) for j in range(W) for i in range(N) if abs(matrice[i][j] - max_profit) < 0.001])
    except ValueError:
        print("ValueError")
        print("max_profit :", max_profit)
        sys.exit(1)
    (name, weight, value) = records[i]
    print(name, weight, value, j)
    max_profit -= value
    N -= 1
    W -= 1
END_TIME = time.time()
print("Elapsed time : ", (END_TIME-START_TIME), "sec")
