from collections import OrderedDict


class FenwickTree:
    def __init__(self, n):
        """
        Initialize a Fenwick Tree with a given size.
        Args:
        n (int): The size of the tree. The tree will have n + 1 elements
        initialized to zero to accommodate 1-based indexing.
        """
        self.n = n
        self.tree = [0] * (n + 1)

    def build(self, array):
        for i, val in enumerate(array, 1):
            self.update(i, val)

    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def range_sum(self, l, r):
        return self.query(r) - self.query(l - 1)


class LRUCache:
    def __init__(self, capacity):
        """
        Initialize an LRUCache with a specified capacity.
        Args:
        capacity (int): The maximum number of items that can be stored in the cache.
        Once the capacity is reached, the least recently used items will be removed to make space for new ones.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate_overlapping(self, index):
        keys_to_remove = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            del self.cache[key]
