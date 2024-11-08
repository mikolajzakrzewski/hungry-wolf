import math


def euclidean_distance(p, q):
    return math.sqrt(sum((p_n - q_n) ** 2 for p_n, q_n in zip(p, q)))

def euclidean_distance_squared(p, q):
    return sum((p_n - q_n) ** 2 for p_n, q_n in zip(p, q))
