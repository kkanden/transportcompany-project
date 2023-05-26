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
