import csv
import time

from operator import attrgetter, itemgetter


class ActionException(Exception):
    """
    classe JoueurExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Joueur
    """
    def __init__(self, message):
        self.message = message


class Action:

    def __init__(self, **kwargs):
        for (attr_name, attr_value) in kwargs.items():
            setattr(self, attr_name, attr_value)

    def __str__(self):
        return f"'name': {self._name}, 'price': {self._price}, 'profit': {self._profit}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value
        else:
            raise ActionException(f"invalid name : {value}")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._price = value
        else:
            try:
                self._price = float(value)
            except ValueError:
                raise ActionException(f"invalid price : {value}")

    @property
    def profit(self):
        return self._profit

    @profit.setter
    def profit(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._profit = value
        else:
            try:
                self._profit = float(value)
            except ValueError:
                raise ActionException(f"invalid profit : {value}")


def subset_actions(actions, target, partial=[], partial_price=0):
    if partial_price == target:
        yield partial
    if partial_price >= target:
        return
    for i, action in enumerate(actions):
        remaining = actions[i + 1:]
        yield from subset_actions(remaining, target, partial + [action], partial_price + action.price)


def sum_profit(actions):
    return sum([action.profit for action in actions])


if __name__ == "__main__":
    TIME_DEBUT = time.gmtime()
    INVEST = 500.0
    with open('actions.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        actions = [Action(**row) for row in reader]
        actions.sort(key=attrgetter('price'), reverse=True)
        list_actions = [{'actions': x, 'sum_profit': sum_profit(x)} for x in
                        subset_actions(actions, INVEST)]
        list_actions.sort(key=itemgetter('sum_profit'), reverse=True)
        dico = list_actions[0]
        print("best profit for {:.2f} € invested = {:.2f} €".format(INVEST, dico['sum_profit']))
        for action in dico['actions']:
            print(action)
        #for dico in list_actions:
        #    print("sum_profit = {:.2f}".format(dico['sum_profit']))
        #    for action in dico['actions']:
        #        print(action)
        print("Number of combinations :", len(list_actions))
        TIME_FIN = time.gmtime()
        print("Debut :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_DEBUT))
        print("Fin :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_FIN))
        print("time.perf_counter() :", time.perf_counter())
        print("time.process_time() :", time.process_time())
