# -*- coding : utf8 -*-
"""
    Program bruteforce.py that resolves the 0-1 knapsack problem using a recursive function
"""

import csv
import time

from operator import attrgetter, itemgetter


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


def subset_actions(list_of_actions, target_price_min, target_price_max, subset, partial_price=0):
    """
    Fonction genératrice et récursive qui renvoie un objet generator correspondant à la liste
    des N-uplets d'actions dont la somme des prix est égale à un montant cible (target_price)
    """

    # Base Case
    if target_price_max <= 0.0:
        return

    # Yield the subset (combination of actions) if it matches the condition below
    if target_price_min <= partial_price <= target_price_max:
        yield subset

    # Quit generator if list_of_actions is empty or
    # partial_price is greater than target_price_max
    if not list_of_actions or partial_price > target_price_max:
        return

    # Recursion on subset_actions function for each item of list_of_actions
    for i, item in enumerate(list_of_actions):
        remaining = list_of_actions[i + 1:]
        yield from subset_actions(remaining, target_price_min, target_price_max,
                                  subset + [item], partial_price + item.price)


def sum_profit(list_of_actions):
    """
    Fonction renvoyant la somme des gains d'une liste d'actions
    :type list_of_actions: list
    """
    return sum([item.profit for item in list_of_actions])


def sum_price(list_of_actions):
    """
    Fonction renvoyant la somme des gains d'une liste d'actions
    :type list_of_actions: list
    """
    return sum([item.price for item in list_of_actions])


if __name__ == "__main__":
    START_TIME = time.time()
    INVEST = 500.0

    with open('data/bruteforce.csv', newline='') as csvfile:

        # read csvfile and store it in a dict named reader
        reader = csv.DictReader(csvfile)

        # generate a list of actions from reader
        actions = []
        for row in reader:
            try:
                actions.append(Action(**row))
            except ActionException as action_error:
                print(f"action non prise en compte - {action_error}")

        # sort actions in price decreasing order
        actions.sort(key=attrgetter('price'), reverse=True)

        # generate the list of combinations with sum_profit(combination)
        # between INVEST_MIN = max(min(actions.price), 0.0)
        #     and INVEST_MAX
        INVEST_MIN = max(actions[-1].price, 0.0)
        combo_actions = [{'list_of_actions': x, 'sum_profit': sum_profit(x)} for x in
                         subset_actions(actions, INVEST_MIN, INVEST, [])]

        # sort list of combinations in sum_profit decreasing order
        # the first item is the combination of actions with the best profit
        combo_actions.sort(key=itemgetter('sum_profit'), reverse=True)

        FILE = 'results/results_bruteforce.txt'

        # write the results into FILE
        with open(FILE, 'w', encoding='utf-8') as file:
            if combo_actions:
                dico = combo_actions[0]
                file.write("Profit maximal = {:.2f} €\n".format(dico['sum_profit']))
                file.write("Somme investie = {:.2f} €\n".format(sum_price(dico['list_of_actions'])))
                file.write(f"Nombre de combinaisons trouvées : {len(combo_actions)}\n")
                file.write("Liste des actions\n")

                # Loop to write actions of the list : dico['list_of_actions']
                for action in dico['list_of_actions']:
                    file.write(action.__str__() + "\n")

            else:
                file.write("Aucune action trouvée pour un gain max = {:.2f} €\n".format(INVEST))

        END_TIME = time.time()
        # print elapsed time
        print("Total elapsed time  :", (END_TIME - START_TIME), "sec")
        # print process_time() : the sum of the system and user CPU time used by the program
        print("time.process_time() :", time.process_time(), "sec")
        # print perf_counter() : performance counter
        print("time.perf_counter() :", time.perf_counter(), "sec")
        print("You can view all the results in file :", FILE)
