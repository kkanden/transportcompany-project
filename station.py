from structures import Vertex
import datetime as dt

class Station(Vertex):
    def __init__(self, key):
        super().__init__(key)
        self.packages_time = []
        self.available_packages = [] # this is sorted by time because packages_time is sorted
        self.distances = {} # already sorted by distance at creation in StationNetwork

    def add_package(self, package):
        self.packages_time.append(package)
        self.packages_time = sorted(self.packages_time, key=lambda pack: pack.time_available) # sort by time

    def update_packages(self, clock):
        for package in self.packages_time:
            if package.time_available <= clock:
                self.available_packages.append(package)
                index = self.packages_time.index(package)
                self.packages_time.pop(index)

    def reset_packages(self):
        if self.available_packages:
            for package in self.available_packages:
                self.packages_time.append(package)
                index = self.available_packages.index(package)
                self.available_packages.pop(index)
            self.packages_time = sorted(self.packages_time, key=lambda pack: pack.time_available)

    def is_empty(self):
        return self.packages_time == [] and self.available_packages == []

    def has_available_packages(self):
        return self.available_packages != []

    def when_next_package(self):
        if not self.packages_time:
            return dt.timedelta.max
        return self.packages_time[0].time_available

    def will_have_available_packages(self, clock):
        for pack in self.packages_time:
            if pack.time_available <= clock:
                return True
        return False

    def distance_to(self, stat_id):
        return self.distances[stat_id]