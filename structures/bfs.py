from queue import Queue
from stack import Stack
from graph import Graph


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


def bfs_test():
    g = Graph()
    for i in range(6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 5)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 0)
    g.add_edge(5, 4)
    g.add_edge(5, 2)

    bfs = BFS(g)

    bfs.bfs(0)
    for v_key in g.vert_list:
        print(f"Path from 0 to {v_key}: {bfs.traverse(v_key)}.")
    print(bfs.distances[2])

if __name__ == "__main__":
    bfs_test()

