class MinHeap:
    def __init__(self):
        self.heap = []

    # O(1)
    def is_empty(self):
        return self.size() == 0

    # O(log(n))
    def insert_key(self, key):
        i = len(self.heap)
        self.heap.append(key)
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
        self.heapify_down(0)
        return ret

    def heapify_up(self, i):
        while i > 0:  # i - indeks, na ktorym poprawiamy własność
            parent = MinHeap.parent(i)
            if self.heap[parent] <= self.heap[i]:  # klucz w rodzicu nie większy, niż klucz w i: OK, jest kopiec
                break
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent

    def heapify_down(self, i):
        lst = self.heap
        while True:  # i - indeks, na ktorym poprawiamy własność
            left, right = MinHeap.left_child(i), MinHeap.right_child(i)
            smallest = i
            if left < len(lst) and lst[left] < lst[smallest]:
                smallest = left
            if right < len(lst) and lst[right] < lst[smallest]:
                smallest = right
            if smallest == i:  # klucz nie mniejszy, niż klucze w lewym i prawym dziecku (jeśli istnieją): OK
                break
            lst[i], lst[smallest] = lst[smallest], lst[i]
            i = smallest

    def size(self):
        return len(self.heap)

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
    print(heap.extract_min())
    print(heap.extract_min())
    heap.insert_key(35)
    print(heap.heap)
    print(heap.extract_min())
    print(heap.extract_min())


if __name__ == "__main__":
    test()

