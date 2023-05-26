from station import Station
from graph import Graph
from dijkstra import Dijkstra

class StationNetwork(Graph):
    def __init__(self, stations_file):
        super().__init__()
        self.stations_file = stations_file
        self.stat_list = {}
        self.create_network()

    def add_station(self, key):
        new_station = Station(key)
        self.stat_list[key] = new_station

    def add_edge(self, f, t, weight=1, symmetric=False):
        super().add_edge(f, t, weight, symmetric)
        if f not in self.stat_list:
            self.add_station(f)
        if t not in self.stat_list:
            self.add_station(t)
        self.stat_list[f].add_neighbor(self.stat_list[t], weight)
        if symmetric:
            self.stat_list[t].add_neighbor(self.stat_list[f], weight)

    def get_station(self, id):
        return self.stat_list[id]

    def get_stations(self):
        return self.stat_list.keys()

    def update_packages(self, clock):
        for station in self.stat_list.values():
            station.update_packages(clock)

    def reset_packages(self):
        for station in self.stat_list.values():
            station.reset_packages()

    def is_empty(self):
        for stat_id in self.get_stations():
            station = self.get_station(stat_id)
            if not station.is_empty():
                return False
        return True

    def num_packages_left(self):
        n = 0
        for station in self.stat_list.values():
            n += len(station.packages_time) + len(station.available_packages)
        return n

    def create_network(self):
        with open(self.stations_file, 'r') as f:
            for line in f:
                line = line.strip().split()
                stat1, stat2, dist = line[0], line[1], int(line[2])
                self.add_edge(stat1, stat2, weight=dist, symmetric=True)

        for k in self.vert_list.keys():
            dij = Dijkstra(self)
            dij.dijkstra(k)
            #print(dij.distances)
            distances_sorted = dict(sorted(dij.distances.items(), key=lambda item: item[1]))
            self.stat_list[k].distances = distances_sorted


if __name__ == "__main__":
    stationnet = StationNetwork("station_network.txt")
    print(stationnet.get_station("POL1").distances)
    #dij = Dijkstra(stationnet)
    #dij.dijkstra("POL15")
    #print(dij.distances)
    #print(stationnet.get_station("POL2").get_connections())