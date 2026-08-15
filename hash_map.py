"""Small hash map implementation using open addressing and linear probing."""

_TOMBSTONE = object()


class HashMap:
    def __init__(self, initial_capacity=8):
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be positive")
        self._capacity = max(8, initial_capacity)
        self._slots = [None] * self._capacity
        self._size = 0
        self._used = 0

    def __len__(self):
        return self._size

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __setitem__(self, key, value):
        if (self._used + 1) / self._capacity > 0.65:
            self._resize(self._capacity * 2)

        idx = self._find_slot_for_insert(key)
        old = self._slots[idx]
        if old is None or old is _TOMBSTONE:
            self._size += 1
            if old is None:
                self._used += 1
        self._slots[idx] = (key, value)

    def __getitem__(self, key):
        idx = self._find_slot(key)
        if idx is None:
            raise KeyError(key)
        return self._slots[idx][1]

    def __delitem__(self, key):
        idx = self._find_slot(key)
        if idx is None:
            raise KeyError(key)
        self._slots[idx] = _TOMBSTONE
        self._size -= 1

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        for slot in self._slots:
            if slot is not None and slot is not _TOMBSTONE:
                yield slot

    def keys(self):
        for key, _ in self.items():
            yield key

    def values(self):
        for _, value in self.items():
            yield value

    def _find_slot(self, key):
        start = hash(key) % self._capacity
        idx = start
        while True:
            slot = self._slots[idx]
            if slot is None or slot is _TOMBSTONE:
                return None
            if slot[0] == key:
                return idx
            idx = (idx + 1) % self._capacity
            if idx == start:
                return None

    def _find_slot_for_insert(self, key):
        start = hash(key) % self._capacity
        idx = start
        first_tombstone = None
        while True:
            slot = self._slots[idx]
            if slot is None:
                return first_tombstone if first_tombstone is not None else idx
            if slot is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = idx
            elif slot[0] == key:
                return idx
            idx = (idx + 1) % self._capacity
            if idx == start:
                if first_tombstone is not None:
                    return first_tombstone
                raise RuntimeError("hash map is full")

    def _resize(self, new_capacity):
        old_items = list(self.items())
        self._capacity = new_capacity
        self._slots = [None] * self._capacity
        self._size = 0
        self._used = 0
        for key, value in old_items:
            self[key] = value


if __name__ == "__main__":
    table = HashMap()
    table["name"] = "Ada"
    table["language"] = "Python"
    table["year"] = 2026

    assert len(table) == 3
    assert table["name"] == "Ada"
    assert table.get("missing", "fallback") == "fallback"

    table["name"] = "Grace"
    assert table["name"] == "Grace"
    assert len(table) == 3

    del table["year"]
    assert "year" not in table
    assert sorted(table.keys()) == ["language", "name"]

    for i in range(30):
        table[f"k{i}"] = i
    assert table["k12"] == 12
    assert len(table) == 32

    print("basic hash map checks passed")
