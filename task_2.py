import timeit
from functools import lru_cache
from random import seed
import matplotlib.pyplot as plt
from splay_tree import SplayTree



@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    cached = tree.find(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val


def measure_time(func, *args):
    stmt = lambda: func(*args)
    return timeit.timeit(stmt, number=1)


if __name__ == "__main__":
    seed(50)
    ns = list(range(0, 1000, 50))
    lru_times = []
    splay_times = []

    for n in ns:
        fibonacci_lru.cache_clear()

        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=3) / 3
        lru_times.append(lru_time)

        tree = SplayTree()
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=3) / 3
        splay_times.append(splay_time)

    plt.plot(ns, lru_times, marker="o", label="LRU Cache")
    plt.plot(ns, splay_times, marker="x", label="Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("\nn        LRU Cache Time (s)   Splay Tree Time (s)")
    print("-------------------------------------------------")
    for n, lru, splay in zip(ns, lru_times, splay_times):
        print(f"{n:<10}{lru:.8f}          {splay:.8f}")
