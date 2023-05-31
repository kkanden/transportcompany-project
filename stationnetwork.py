from station import Station
from structures import Graph
from structures import Dijkstra

class StationNetwork(Graph):
    """Class representing the whole network of Stations. It inherits all properties
    from Graph class. Its basic building blocks are instances of Station, which in turn
    inherit from Vertex. Thus graph algorithms such as Dijkstra also work with this
    class
    
    Attributes
    ----------
    stations_file : str
        path to file with information about the network of stations each line being
        in the following format: Station1 ID, Station2 ID, distance
    stat_list : dict
        equivalent of vert_list in Graph for instances of Station
        
    Methods
    -------
    """
    
    def __init__(self, stations_file):
        """
        Parameters
        ----------
        stations_file : str
            path to file with information about the network of stations each line being
            in the following format: Station1 ID, Station2 ID, distance
        """
        
        super().__init__()
        self.stations_file = stations_file
        self.stat_list = {}
        self.create_network()

    def add_station(self, stat_id):
        """Creates instance of Station with given ID and adds it stat_list
        
        Parameters
        ----------
        stat_id : str
            unique station ID
        """
        new_station = Station(stat_id)
        self.stat_list[stat_id] = new_station

    def add_edge(self, f, t, weight=1, symmetric=False):
        """Overrides Graph's add_edge method such that it also creates connections
        between instances of Station

        Parameters
        ----------
        f : str
            ID of first station
        t : str
            ID of other station
        weight : int
            in case of Stations - represents distance in minutes
        symmetric : bool
            makes the connection directional or non-directional
        """
        
        super().add_edge(f, t, weight, symmetric)
        if f not in self.stat_list:
            self.add_station(f)
        if t not in self.stat_list:
            self.add_station(t)
        self.stat_list[f].add_neighbor(self.stat_list[t], weight)
        if symmetric:
            self.stat_list[t].add_neighbor(self.stat_list[f], weight)

    def get_station(self, stat_id):
        """Station equivalent of get_vertex
        
        Parameters
        ----------
        stat_id : str
            ID of station
        """
        return self.stat_list[stat_id]

    def get_stations(self):
        """Station equivalent of get_vertices"""
        return self.stat_list.keys()

    def update_packages(self, clock):
        """Invokes update_packages method on all Stations in stat_list"""
        for station in self.stat_list.values():
            station.update_packages(clock)

    def reset_packages(self):
        """Invokes reset_packages method on all Stations in stat_list"""
        for station in self.stat_list.values():
            station.reset_packages()

    def is_empty(self):
        """Invokes is_empty method on all Stations in stat_list, if all are empty
        returns True, returns False otherwise"""
        for stat_id in self.get_stations():
            station = self.get_station(stat_id)
            if not station.is_empty():
                return False
        return True

    def num_packages_left(self):
        """Returns the number of packages left in network"""
        n = 0
        for station in self.stat_list.values():
            n += len(station.packages_time) + len(station.available_packages)
        return n

    def create_network(self):
        """Creates the network using stations_file given at initialization"""
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