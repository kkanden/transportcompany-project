import datetime as dt
import random

class Driver:
    def __init__(self, driver_id, stationnet):
        self.id = driver_id
        self.stationnet = stationnet
        self.current_station = random.choice(list(stationnet.stat_list.values()))
        self.clock = dt.timedelta(hours=6, minutes=0)
        self.work_time_remaining = dt.timedelta(hours=8)
        self.packages_delivered = 0
        self.itinerary = []

    def can_travel_to(self, stat_id):
        distance = self.current_station.distance_to(stat_id)
        return distance <= self.work_time_remaining.seconds // 60  # and \
        # self.clock + dt.timedelta(minutes=distance) <= dt.timedelta(days=1)

    def can_travel_anywhere(self):
        for stat_id in self.current_station.distances.keys():
            if self.can_travel_to(stat_id):
                return True
        return False

    def pass_time(self, minutes):
        time_to_pass = dt.timedelta(minutes=minutes)
        self.clock += time_to_pass
        self.work_time_remaining -= time_to_pass

    def take_package(self, pack):
        index = self.current_station.available_packages.index(pack)
        self.current_station.available_packages.pop(index)

    def travel_to(self, stat_id):
        distance = self.current_station.distance_to(stat_id)
        self.current_station = self.stationnet.get_station(stat_id)
        self.pass_time(distance)
        self.current_station.update_packages(self.clock)

    def pickup_and_travel(self):
        l = self.current_station.available_packages
        for pack in l:
            # if self.can_travel_to(package.end_station):
            self.take_package(pack)
            if not self.itinerary:
                self.clock = pack.time_available
                self.itinerary.append(f"[{self.clock_print()}]: START work at station {self.current_station.get_id()}")
            self.itinerary.append(f"[{self.clock_print()}]: PICK UP package {pack.id} from station {self.current_station.get_id()}")
            self.travel_to(pack.end_station)
            self.itinerary.append(f"[{self.clock_print()}]: DELIVER package {pack.id} to station {self.current_station.get_id()}")
            self.packages_delivered += 1
            break

    def clock_print(self):
        return str(self.clock)[:-3]
