
import time


if __name__ == "__main__":
    TIME_DEBUT = time.gmtime()
    values = [1, 4, 5, 7]
    weights = [1, 3, 4, 5]
    N = len(values)
    print("N :", N)
    W = 8
    print("W :", W)
    m = [[0 for _ in range(W)] for _ in range(N)]
    for j in range(0, W, 1):
        if j < values[0]:
            m[0][j] = 0
        else:
            m[0][j] = values[0]
    for i in range(1, N, 1):
        for j in range(0, W, 1):
            if j < weights[i]:
                m[i][j] = m[i-1][j]
            else:
                a = values[i] + m[i-1][j-weights[i]]
                b = m[i-1][j]
                m[i][j] = max(a, b)
                print("i =", i, "j =", j)
                print("a =", a, "b =", b)
                print("m[i][j] =", m[i][j])

    for i in range(N):
        print("i =", i, "values[i] =", values[i], "max(m[i]) =", max(m[i]), "m[i] =", m[i])
    TIME_FIN = time.gmtime()
    print("Debut :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_DEBUT))
    print("Fin :", time.strftime("%a, %d %b %Y %H:%M:%S +0000", TIME_FIN))
    print("time.perf_counter() :", time.perf_counter())
    print("time.process_time() :", time.process_time())
