# -*- coding : utf8 -*-
"""
    Program bruteforce.py that resolves the 0-1 knapsack problem using a recursive function
"""

import csv
import time

from operator import attrgetter


class ActionException(Exception):
    """
    classe ActionException pour lever une exception lors du
    traitement d'un objet de type Action
    """

    def __init__(self, message):
        super().__init__()
        self.message = message


# noinspection PyAttributeOutsideInit
class Action:
    """
    classe Action
    """

    def __init__(self, **kwargs):
        for (attr_name, attr_value) in kwargs.items():
            setattr(self, attr_name, attr_value)
        if self.price <= 0 or self.profit <= 0:
            raise ActionException(f"Action {self.name} has price or profit is <= 0")
        self.ratio = self.profit / self.price

    def __str__(self):
        return f"{self._name}, {self._price}, {self._profit}"

    @property
    def name(self):
        """
        Returns name
        @return: self._name
        """
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise ActionException(f"invalid name : {value}")

    @property
    def price(self):
        """
        Returns price
        @return: self._price
        """
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, (float, int)):
            self._price = value
        else:
            try:
                self._price = float(value)
            except ValueError as value_error:
                raise ActionException(f"invalid price : {value} - {value_error}") from value_error

    @property
    def profit(self):
        """
        Returns profit
        @return: self._profit
        """
        return self._profit

    @profit.setter
    def profit(self, value):
        if isinstance(value, (float, int)):
            self._profit = value
        else:
            try:
                self._profit = float(value)
            except ValueError as value_error:
                raise ActionException(f"invalid profit : {value} - {value_error}") from value_error


def subset_actions(list_of_actions,
                   target_price_max,
                   subset,
                   partial_price=0,
                   partial_profit=0):
    """
    Fonction genératrice et récursive qui renvoie un objet generator correspondant à la liste
    des N-uplets d'actions dont la somme des prix est égale à un montant cible (target_price)
    """

    # Base Case
    if target_price_max <= 0.0:
        return

    # Yield the subset (combination of actions) with its partial_price and partial_profit
    # if it matches the condition below
    if 0.0 <= partial_price <= target_price_max:
        yield subset, partial_price, partial_profit

    # Quit generator if list_of_actions is empty or
    # partial_price is greater than target_price_max
    if not list_of_actions or partial_price > target_price_max:
        return

    # Recursion on subset_actions function for each item of list_of_actions
    for i, item in enumerate(list_of_actions):
        yield from subset_actions(list_of_actions[i + 1:],
                                  target_price_max,
                                  subset + [item],
                                  partial_price + item.price,
                                  partial_profit + item.profit)


if __name__ == "__main__":
    START_TIME = time.time()
    INVEST_MAX = 500.0
    with open('data/bruteforce.csv', newline='') as csvfile:
        # read the whole csvfile and store it in a dictionary named reader
        reader = csv.DictReader(csvfile)

        # generate a list of actions from reader
        actions = []
        for row in reader:
            try:
                actions.append(Action(**row))
            except ActionException as action_error:
                print(f"action non prise en compte - {action_error}")

        # sort actions in ratio decreasing order
        actions.sort(key=attrgetter('ratio', 'price'), reverse=False)

        # generate the list of combinations with sum_profit(combination)
        # between 0.0 and INVEST_MAX
        combo_actions = list(subset_actions(actions, INVEST_MAX, []))

        # sort list of combinations in sum_profit decreasing order
        # the first item is the combination of actions with the best profit
        combo_actions.sort(key=lambda x: x[2], reverse=True)

        FILE = 'results/results_bruteforce.txt'

        # write the results into FILE
        with open(FILE, 'w', encoding='utf-8') as file:
            if combo_actions:
                (list_actions, sum_price, sum_profit) = combo_actions[0]
                file.write("Liste des actions\n")
                # Loop to write actions of the list : dico['list_of_actions']
                for action in list_actions:
                    file.write(action.name + "\n")
                file.write(f"Profit maximal = {sum_profit:.2f} €\n")
                file.write(f"Somme investie = {sum_price:.2f} €\n")
                print(f"Nombre de combinaisons trouvées : {len(combo_actions)}\n")
            else:
                file.write(f"Aucune action trouvée pour un gain max = {INVEST_MAX:.2f} €\n")

        END_TIME = time.time()
        # print elapsed time
        print("Total elapsed time  :", (END_TIME - START_TIME), "sec")
        # print process_time() : the sum of the system and user CPU time used by the program
        print("time.process_time() :", time.process_time(), "sec")
        # print perf_counter() : performance counter
        print("time.perf_counter() :", time.perf_counter(), "sec")
        print("You can view all the results in file :", FILE)
