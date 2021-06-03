import csv
import time

from operator import attrgetter, itemgetter


class ActionException(Exception):
    """
    classe ActionException pour lever une exception lors du
    traitement d'un objet de type Action
    """
    def __init__(self, message):
        self.message = message


class Action:
    """
    classe Action
    """
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


def subset_actions(actions, target_price, subset=[], partial_price=0):
    """
    Fonction genératrice et récursive qui renvoie un objet generator correspondant à la liste
    des N-uplets d'actions dont la somme des prix est égale à un montant cible (target_price)
    """
    if (target_price - 5.0) <= partial_price <= target_price:
        yield subset
    if partial_price > target_price:
        return
    for i, action in enumerate(actions):
        remaining = actions[i + 1:]
        yield from subset_actions(remaining, target_price, subset + [action], partial_price + action.price)


def sum_profit(actions):
    """
    Fonction renvoyant la somme des gains d'une liste d'actions
    """
    return sum([action.profit for action in actions])

def sum_price(actions):
    """
    Fonction renvoyant la somme des gains d'une liste d'actions
    """
    return sum([action.price for action in actions])


if __name__ == "__main__":
    START_TIME = time.time()
    INVEST = 500.0
    with open('actions.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        actions = [Action(**row) for row in reader]
        actions.sort(key=attrgetter('price'), reverse=True)
        list_actions = [{'actions': x, 'sum_profit': sum_profit(x)} for x in
                        subset_actions(actions, INVEST)]
        list_actions.sort(key=itemgetter('sum_profit'), reverse=True)
        """
        for dico in list_actions:
            print("Gain = {:.2f}".format(dico['sum_profit']))
            for action in dico['actions']:
                print(action)
        print("Nombre de combinaisons  trouvées :", len(list_actions))
        """
        dico = list_actions[0]
        print("Le meilleur gain pour {:.2f} € investis est de : {:.2f} €".format(INVEST, dico['sum_profit']))
        print("La somme investie réellement est de : {:.2f} €".format(sum_price(dico['actions'])))
        for action in dico['actions']:
            print(action)
        END_TIME = time.time()
        print("Elapsed time : ", (END_TIME - START_TIME), "sec")
        print("time.perf_counter() :", time.perf_counter())
        print("time.process_time() :", time.process_time())
