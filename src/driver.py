import datetime
import datetime as dt
import random
from stationnetwork import StationNetwork
from package import Package

class Driver:
    """
    Class representing a Driver.
    
    Attributes
    ----------
    id : str
        unique ID of driver
    stationnet : StationNetwork
        instance of StationNetwork the driver lives inside of
    current_station : Station
        instance of Station the driver is currently in; at instantiation station is chosen randomly
    clock : datetime.timedelta
        driver's current time, at instantiation set to 6:00 AM
    work_time_remaining : datetime.timedelta
        at instantiation set to 8 hours
    packages_delivered : int
        number of packages delivered by Driver
    itinerary : list[str]
        list of subsequent actions made by the driver at given time
    
    Methods
    -------
    """
    
    def __init__(self, driver_id: str, stationnet: StationNetwork):
        """
        
        Parameters
        ----------
        driver_id : str
            unique driver ID
        stationnet : StationNetwork
            instance of StationNetwork the driver lives inside of
        """
        
        self.id = driver_id
        self.stationnet = stationnet
        self.current_station = random.choice(list(stationnet.stat_list.values()))
        self.clock = dt.timedelta(hours=6, minutes=0)
        self.work_time_remaining = dt.timedelta(hours=8)
        self.packages_delivered = 0
        self.itinerary = []

    def can_travel_to(self, stat_id: str):
        """Returns True if distance to Station with given ID is shorter than
        remaining worktime, returns False otherwise
        
        Parameters
        ----------
        stat_id : str
            ID of station
        """
        
        distance = self.current_station.distance_to(stat_id)
        return distance <= self.work_time_remaining.seconds // 60  # and \
        # self.clock + dt.timedelta(minutes=distance) <= dt.timedelta(days=1)

    def can_travel_anywhere(self):
        """Invokes can_travel_to method on all Stations in network"""
        
        for stat_id in self.current_station.distances.keys():
            if self.can_travel_to(stat_id):
                return True
        return False

    def pass_time(self, minutes: datetime.timedelta):
        """Subtracts given time from work_time_remaining and adds it to clock

        Parameters
        ----------
        minutes : datetime.timedelta
            time in minutes to pass
        """
        
        time_to_pass = dt.timedelta(minutes=minutes)
        self.clock += time_to_pass
        self.work_time_remaining -= time_to_pass

    def take_package(self, pack: Package):
        """Removes given instance of Package from driver's current station's
        available packages

        Parameters
        ----------
        pack : Package
            instance of Package to be taken
        """
        
        index = -1
        for i, available_pack in enumerate(self.current_station.available_packages):
            if available_pack.id == pack.id:
                index = i
                break
        if index != -1:
            self.current_station.available_packages.pop(index)

    def travel_to(self, stat_id: str):
        """Changes driver's current station to station given and passes an appropriate
        amount of time
        
        Parameters
        ----------
        stat_id : str
            ID of station to travel to
        """
        
        distance = self.current_station.distance_to(stat_id)
        self.current_station = self.stationnet.get_station(stat_id)
        self.pass_time(distance)
        self.current_station.update_packages(self.clock)

    def pickup_and_travel(self):
        """Picks up the first available package from current station and travels to
        package's destination invoking the take_package and travel_to methods
        """
        
        l = self.current_station.available_packages
        # pack = l[0]
        for pack in l:
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
        """Prints driver's current time in HH:MM format"""
        
        return str(self.clock)[:-3]
