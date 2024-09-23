class Stack:
    def __init__(self):
        self.items = []

    # O(1)
    def is_empty(self):
        return self.items == []

    # O(1)
    def push(self, item):
        self.items.append(item)

    # O(1)
    def pop(self):
        return self.items.pop()

    # O(1)
    def peek(self):
        return self.items[-1]

    # O(1)
    def size(self):
        return len(self.items)

    def __iter__(self):
        while not self.is_empty():
            yield self.pop()


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


class Vertex:
    def __init__(self, key):
        self.id = key
        # klucze - sąsiady (instancje Vertex)
        # wartości - wagi
        self.connected_to = {}
        
    def get_id(self):
        return self.id

    def add_neighbor(self, nbr, weight=1):
        self.connected_to[nbr] = weight

    def get_connections(self):
        return self.connected_to.keys()

    def get_weight(self, nbr):
        return self.connected_to[nbr]

    def __str__(self):
        return f"{self.id} connected to: {[x.id for x in self.connected_to]}."
    

class Graph:
    def __init__(self):
        # klucze - klucze (id) wierzchołków
        # wartości - wierzchołki (instancje Vertex)
        self.vert_list = {}

    def add_vertex(self, key):
        new_vertex = Vertex(key)
        self.vert_list[key] = new_vertex

    def get_vertex(self, key):
        if key in self.vert_list:
            return self.vert_list[key]
        else:
            return None

    def add_edge(self, f, t, weight=1, symmetric=False):
        if f not in self.vert_list:
            self.add_vertex(f)
        if t not in self.vert_list:
            self.add_vertex(t)
        self.vert_list[f].add_neighbor(self.vert_list[t], weight)
        if symmetric:
            self.vert_list[t].add_neighbor(self.vert_list[f], weight)

    def get_vertices(self):
        return self.vert_list.keys()

    def __contains__(self, key): # key in g
        return key in self.vert_list

    def __iter__(self):
        return iter(self.vert_list.values())
    
from queue import Queue    

class BFS:
    def __init__(self, g):
        if not isinstance(g, Graph):
            raise TypeError("The argument g should be a Graph.")
        self.g = g
        self.colors = {}
        self.distances = {}
        self.predecessors = {}

    def clear(self):
        for v_key in self.g.vert_list:
            self.colors[v_key] = "white"
            self.distances[v_key] = 0
            self.predecessors[v_key] = None

    def bfs(self, start_key):
        self.clear()
        vert_queue = Queue()

        vert_queue.put(self.g.vert_list[start_key]) # enqueue
        while not vert_queue.empty():
            current_vert = vert_queue.get()  # deque
            cur_key = current_vert.get_id()

            for nbr in current_vert.get_connections():
                nbr_key = nbr.get_id()
                if self.colors[nbr_key] == 'white':
                    self.colors[nbr_key] = 'gray'
                    self.distances[nbr_key] =\
                        self.distances[cur_key] + 1
                    self.predecessors[nbr_key] = current_vert
                    vert_queue.put(nbr)

            self.colors[cur_key] = 'black'


    def traverse(self, key_x):
        result = Stack()
        x = self.g.vert_list[key_x]
        while self.predecessors[x.get_id()]:
            result.push(x.get_id())
            x = self.predecessors[x.get_id()]

        result.push(x.get_id())
        return list(result)  # brak ścieżki: [key_x]

from math import inf

class Dijkstra(BFS):
    def clear(self):
        super().clear()
        for v_key in self.g.vert_list:
            self.distances[v_key] = inf

    def dijkstra(self, start_key):
        self.clear()
        self.distances[start_key] = 0
        h = MinHeap((v, k) for k, v in self.distances.items())

        while not h.is_empty():
            current_distance, cur_key = h.extract_min()
            # jeśli current_distance == inf, to wierzchołek nie jest osiągalny ze źródła
            if current_distance == inf:
                return

            current_vert = self.g.get_vertex(cur_key)
            self.distances[cur_key] = current_distance
            self.colors[cur_key] = 'black'
            for nbr in current_vert.get_connections():
                nbr_key = nbr.get_id()
                if self.colors[nbr_key] != 'white':
                    continue
                weight = current_vert.get_weight(nbr)
                neighbor_distance = self.distances[nbr_key]
                if current_distance + weight < neighbor_distance:
                    h.decrease_key((neighbor_distance, nbr_key),
                                   (current_distance + weight, nbr_key))
                    self.distances[nbr_key] = current_distance + weight
                    self.predecessors[nbr_key] = current_vert

