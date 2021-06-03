
import time
from subprocess import call

class ActionException(Exception):
    """
    classe JoueurExeption pour lever ou intercepter une exception lors du
    traitement d'un objet de type Joueur
    """
    def __init__(self, message):
        self.message = message


class Action:

    __attr_names = ['name', 'price', 'profit']

    def __init__(self, *args):
        for i, value in enumerate(args):
            setattr(self, self.__attr_names[i], value)

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
            self._price = int(value * 100)
        else:
            try:
                self._price = int(float(value)*100)
            except ValueError:
                raise ActionException(f"invalid price : {value}")

    @property
    def profit(self):
        return self._profit

    @profit.setter
    def profit(self, value):
        if isinstance(value, int) or isinstance(value, float):
            self._profit = int(value * 100)
        else:
            try:
                self._profit = int(float(value)*100)
            except ValueError:
                raise ActionException(f"invalid profit : {value}")


if __name__ == "__main__":
    TIME_DEBUT = time.gmtime()
    # tri du fichier sur valeur (sort on profit)
    call('sed 1d actions.csv | sort -t "," -k3 -n > actions_sorted.csv', shell=True)
    csv_gen = (row[:-1] for row in open("actions_sorted.csv",  newline=''))
    names = []
    values = []
    weights = []
    for i, item in enumerate(csv_gen):
        print(item)
        a = Action(*item.split(sep=","))
        names.append(a.name)
        weights.append(a.price)
        values.append(a.profit)
    N = len(values)
    print("values :", values)
    print("N :", N)
    W = 50001
    print("weights", weights)
    print("W :", W)
    m = [[0 for _ in range(W)] for _ in range(N)]
    for j in range(0, W, 1):
        if j < weights[0]:
            m[0][j] = 0
        else:
            m[0][j] = values[0]
    for i in range(1, N, 1):
        for j in range(0, W, 1):
            if j < weights[i]:
                m[i][j] = m[i-1][j]
            else:
                m[i][j] = max((values[i] + m[i-1][j-weights[i]]), m[i-1][j])
    for i in range(N):
        print("i :", i, "values[i] :", values[i], "max(m[i]) :", max(m[i]))
    TIME_FIN = time.gmtime()
    print("Debut :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_DEBUT))
    print("Fin :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_FIN))
    print("time.perf_counter() :", time.perf_counter())
    print("time.process_time() :", time.process_time())
