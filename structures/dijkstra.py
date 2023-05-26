import sys
sys.path.append("C:/Users/Gracz/OneDrive/Desktop/PYTHON/PROJECT/structures/min_heap.py")
from min_heap import MinHeap
from graph import Graph
from bfs import BFS
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


if __name__ == "__main__":
    g = Graph()

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 5)
    g.add_edge(0, 3)
    g.add_edge(3, 4, weight=1000)
    g.add_edge(2, 5)
    g.add_edge(4, 5)
    g.add_edge(0, 5, 2.99)  # g.add_edge(0, 5, 2.99)
    
    dij = Dijkstra(g)
    dij.dijkstra(0)
    print(dij.traverse(4))
    print(dij.distances[4])
