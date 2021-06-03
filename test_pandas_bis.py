import sys
import time
import pandas as pd

START_TIME = time.time()
df = pd.read_csv('actions.csv')
df.sort_values(by=['profit', 'price'], ascending=True, inplace=True)
records = df.loc[df['price'] > 0].to_records(index=False)
names = [name for (name, *args) in records]
values = [value for (*args, value) in records]
weights = [weight for (_, weight, _) in records]

N = len(names)      # Nombre d'actions
W = 501             # Investissement maximal + 1

# Initialisation de la matrice de données
matrice = [[0 for _ in range(W)] for _ in range(N)]

# Initialisation de la première ligne de la matrice

for j in range(0, W, 1):
    if j < int(weights[0]):
        matrice[0][j] = 0
    else:
        matrice[0][j] = values[0]

# Boucle d'alimentation de la matrice avec les combinaisons d'actions
for i in range(1, N, 1):
    for j in range(0, W, 1):
        if j < int(weights[i]):
            matrice[i][j] = matrice[i - 1][j]
        else:
            matrice[i][j] = max((values[i] + matrice[i - 1][j - int(weights[i])]), matrice[i - 1][j])

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
    print(names[i], weights[i], values[i])
    max_profit -= values[i]
    N -= 1
    W -= 1
END_TIME = time.time()
print("Total Elapsed time : ", (END_TIME-START_TIME), "sec")

