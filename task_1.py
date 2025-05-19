import random
import time
from lru import FenwickTree, LRUCache


class NonCachedArray:
    def __init__(self, array):
        """
    Initialize a NonCachedArray with a given array.
    Args:
    array (list): The list of integers to be managed by the NonCachedArray.
    """
        self.array = array

    def range_sum(self, L, R):
        return sum(self.array[L : R + 1])

    def update(self, index, value):
        self.array[index] = value


class CachedArray:
    def __init__(self, array, cache_capacity=1000):
        """
        Initialize a CachedArray with a given array and cache capacity.
        Args:
        array (list): The list of integers to be managed by the CachedArray.
        cache_capacity (int, optional): The maximum number of cached range sums. Defaults to 1000.
        """
        self.array = array
        self.n = len(array)
        self.fenw = FenwickTree(self.n)
        self.fenw.build(array)
        self.cache = LRUCache(cache_capacity)

    def range_sum_with_cache(self, L, R):
        key = (L, R)
        cached_res = self.cache.get(key)
        if cached_res is not None:
            return cached_res
        res = self.fenw.range_sum(L + 1, R + 1)
        self.cache.put(key, res)
        return res

    def update_with_cache(self, index, value):
        old_val = self.array[index]
        delta = value - old_val
        self.array[index] = value
        self.fenw.update(index + 1, delta)
        self.cache.invalidate_overlapping(index)


N = 100_000
Q = 50_000
random.seed(50)

array = [random.randint(1, 100) for _ in range(N)]

queries = []
for _ in range(Q):
    if random.random() < 0.7:
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(("Range", L, R))
    else:
        idx = random.randint(0, N - 1)
        val = random.randint(1, 100)
        queries.append(("Update", idx, val))


non_cached_arr = NonCachedArray(array.copy())

start = time.time()
for q in queries:
    if q[0] == "Range":
        _, L, R = q
        _ = non_cached_arr.range_sum(L, R)
    else:
        _, idx, val = q
        non_cached_arr.update(idx, val)
time_no_cache = time.time() - start


cached_arr = CachedArray(array.copy())

start = time.time()
for q in queries:
    if q[0] == "Range":
        _, L, R = q
        _ = cached_arr.range_sum_with_cache(L, R)
    else:
        _, idx, val = q
        cached_arr.update_with_cache(idx, val)
time_cache = time.time() - start


print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {time_cache:.2f} секунд")
