class MinHeap:
    # O(n log(n)), można lepiej: O(n)
    def __init__(self, values=()):
        self.heap = []
        self.keys = dict()  # pod którym indeksem jest klucz: self.heap[i] == k jest tożsame z self.keys[k] == i

        for x in values:
            self.insert_key(x)

    # O(1)
    def is_empty(self):
        return self.size() == 0

    # O(log(n))
    def insert_key(self, key):
        i = len(self.heap)
        self.heap.append(key)
        self.keys[key] = i
        self.heapify_up(i)

    # O(1)
    def peek(self):
        if self.is_empty():
            raise IndexError('Empty heap')
        return self.heap[0]

    # O(log(n))
    def extract_min(self):
        if self.is_empty():
            raise IndexError('Empty heap')
        ret = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        del self.keys[ret]
        if not self.is_empty():
            self.keys[self.heap[0]] = 0
        self.heapify_down(0)
        return ret

    def heapify_up(self, i):
        lst = self.heap
        while i > 0:  # i - indeks, na ktorym poprawiamy własność
            parent = MinHeap.parent(i)
            if lst[parent] <= lst[i]:  # klucz w rodzicu nie większy, niż klucz w i: OK, jest kopiec
                break
            lst[i], lst[parent] = lst[parent], lst[i]
            self.keys[lst[i]] = i
            self.keys[lst[parent]] = parent
            i = parent

    def heapify_down(self, i):
        while True:  # i - indeks, na ktorym poprawiamy własność
            left, right = MinHeap.left_child(i), MinHeap.right_child(i)
            smallest = i
            lst = self.heap
            if left < len(lst) and lst[left] < lst[smallest]:
                smallest = left
            if right < len(lst) and lst[right] < lst[smallest]:
                smallest = right
            if smallest == i:  # klucz nie mniejszy, niż klucze w lewym i prawym dziecku (jeśli istnieją): OK
                break
            lst[i], lst[smallest] = lst[smallest], lst[i]
            self.keys[lst[i]] = i
            self.keys[lst[smallest]] = smallest
            self.heapify_down(smallest)

    # O(log(n)), klucze musza byc unikalne i hashowalne!
    def decrease_key(self, key, new_val):
        self.decrease_key_at_index(self.keys[key], new_val)

    # O(log(n))
    def decrease_key_at_index(self, i, new_val):
        if new_val > self.heap[i]:
            raise ValueError('Key value larger than before')
        del self.keys[self.heap[i]]
        self.heap[i] = new_val
        self.keys[new_val] = i
        self.heapify_up(i)

    def size(self):
        return len(self.heap)

    def __iter__(self):
        while not self.is_empty():
            yield self.extract_min()

    @staticmethod
    def parent(i):  # metoda statyczna - bez self. Użycie: MinHeap.parent(i) - jak każda zwykła funkcja
        return (i - 1) // 2

    @staticmethod
    def left_child(i):
        return 2 * i + 1

    @staticmethod
    def right_child(i):
        return 2 * i + 2


def test():
    heap = MinHeap()
    heap.insert_key(20)
    heap.insert_key(30)
    heap.insert_key(40)
    heap.insert_key(10)
    print(heap.heap)
    print(heap.keys)
    heap.decrease_key(30, 0)
    print(heap.heap)
    print(heap.keys)
    print(heap.extract_min())
    print(heap.extract_min())
    heap.insert_key(35)
    print(heap.heap)
    print(heap.keys)
    heap.decrease_key(35, 20)
    print(heap.heap)
    print(heap.keys)


if __name__ == "__main__":
    test()
