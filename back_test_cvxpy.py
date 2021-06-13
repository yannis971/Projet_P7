# -*- coding : utf8 -*-
"""
Résolution du problème avec numpy et cvxpy
"""

import sys
import time
import argparse
import cvxpy

import numpy as np
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
    print("\nProgramme back_test_numpy.py Projet P7 du parcours DA Python")
    print("\nAuteur : Yannis Saliniere")
    print("\nLicense : GNU GPL V3")
    print("\nusage: optimized.py [-h] [-f FILE]\n")
    print("  -h, --help \t\t show this help message and exit")
    print("  -f FILE, --file FILE")
    print("\t\t\t chemin vers le fichier_csv csv à traiter ")


if __name__ == '__main__':
    args = parse_arguments()
    if not args.file:
        help_message()
        sys.exit(0)
    START_TIME = time.time()

    # generate a pandas.DataFrame from file passed in args
    data_frame = pd.read_csv(args.file)

    # create a list of items from data_frame adding a column ration (profit/price)
    records = [(name, int(price * 100), profit, profit / price)
               for (name, price, profit) in data_frame.to_records(index=False)
               if profit > 0 and price > 0]

    # sort items on ratio (profit/price) then price decreasing order
    records.sort(key=lambda x: (x[3], x[1]), reverse=True)

    # Poids limite
    POIDS_LIMITE = 50000

    # Les poids et Valeurs
    poids = np.array([price for (_, price, profit, _) in records])
    valeurs = np.array([profit for (_, price, profit, _) in records])
    names = np.array([name for (name, price, profit, _) in records])
    N = len(names)

    # Variables de décision
    decision = cvxpy.Variable(len(poids), boolean=True)

    # Contrainte de poids total
    contrainte_poids = poids @ decision <= POIDS_LIMITE

    # Fonction objectif
    # fonction_objectif = valeurs * decision
    fonction_objectif = valeurs @ decision

    # On résout le problème avec CVXPY en précisant sa nature (Maximisation ou Minimisation)

    # Puis en passant toutes les contraintes en argument dans une liste
    probleme_sacados = cvxpy.Problem(cvxpy.Maximize(fonction_objectif), [contrainte_poids])

    # On précise le solver à utilisé pour résoudre le problème
    # GLPK_MI est un solver dédié au problème de programmation linéaire en nombres entiers
    probleme_sacados.solve(solver=cvxpy.GLPK_MI, verbose=True)

    # path to file results
    RESULTS_FILE = args.file.replace("data/", "results/cvxpy_results_").replace("csv", "txt")

    with open(RESULTS_FILE, 'w', encoding='utf-8') as file:
        SUM_PROFIT = 0.0
        SUM_PRICE = 0.0
        file.write("Liste des actions\n")
        for i in range(N-1, -1, -1):
            if decision.value[i] > 0:
                file.write(names[i] + "\n")
                SUM_PRICE += poids[i] / 100
                SUM_PROFIT += valeurs[i]
        file.write(f"Profit maximal = {SUM_PROFIT:.2f} €\n")
        file.write(f"Somme investie = {SUM_PRICE:.2f} €\n")

    END_TIME = time.time()
    # print elapsed time
    print(f'Total elapsed time  : {END_TIME - START_TIME} sec')
    # print process_time() : the sum of the system and user CPU time used by the program
    print(f'time.process_time() : {time.process_time()} sec')
    # print perf_counter() : performance counter
    print(f'time.perf_counter() : {time.perf_counter()} sec')
    print(f'You can view the results in file {RESULTS_FILE}')
