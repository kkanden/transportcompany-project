from structures import Vertex
import datetime as dt

class Station(Vertex):
    """
    Class representing a station. It inherits all properties from Vertex class.
    
    Attributes
    ----------
    stat_id : str
        unique ID of station
    packages_time : list
        list of instances of Package that will be available on station,
        sorted non-decreasingly by time of availability
    available_packages : list
        list of instances of Package that are currently available on station,
        sorted non-decreasingly by time of availability by nature of how it is created
    distances : dict
        dictionary of all instances of Station in network and their distance from
        this Station
    
    Methods
    --------
    add_package(package : Package):
        adds instance of Package to packages_time attribute
    update_packages(clock: datetime.timedelta):
        parses through packages_time and adds instance of Package to available_packages
        dictionary if clock is greater than or equal to time of availability of Package,
        then removes that Package from packages_time
    reset_packages():
        puts all packages from available_packages back to packages_time and then sorts
        non-decreasingly by time of availability
    is_empty():
        checks whether Station has any packages in packages_time or available_packages
    has_available_packages():
        checks whether Station has any packages in available_packages
    will_have_packages(clock : datetime.timedelta):
        checks whether Station will have any packages in available_packages at 
        given time
    when_next_package():
        returns time in datetime.delta of next available package
    distance_to(stat_id : str):
        returns distance to other Station of given ID
    """
    
    def __init__(self, stat_id):
        """
        Parameters
        ----------
        stat_id : str
            unique ID of station
        """
        
        super().__init__(stat_id)
        self.packages_time = []
        self.available_packages = [] # this is sorted by time because packages_time is sorted
        self.distances = {} # already sorted by distance at creation in StationNetwork

    def add_package(self, package):
        """Adds instance of Package to packages_time attribute and instantly sorts
        non-decreasingly by time

        Parameters
        ----------
        package : Package
            instance of Package to be added
        """
        
        self.packages_time.append(package)
        self.packages_time = sorted(self.packages_time, key=lambda pack: pack.time_available) # sort by time

    def update_packages(self, clock):
        """Parses through packages_time and adds instance of Package to available_packages
        dictionary if clock is greater than or equal to time of availability of Package,
        then removes that Package from packages_time
        
        Parameters
        ----------
        clock : datetime.timedelta
            time to update packages by
        """
        
        for package in self.packages_time:
            if package.time_available <= clock:
                self.available_packages.append(package)
                index = self.packages_time.index(package)
                self.packages_time.pop(index)

    def reset_packages(self):
        """Puts all packages from available_packages back to packages_time and then sorts
        non-decreasingly by time of availability
        """
        
        if self.available_packages:
            for package in self.available_packages:
                self.packages_time.append(package)
                index = self.available_packages.index(package)
                self.available_packages.pop(index)
            self.packages_time = sorted(self.packages_time, key=lambda pack: pack.time_available)

    def is_empty(self):
        """Checks whether Station has any packages in packages_time or available_packages,
        returns bool
        """
        
        return self.packages_time == [] and self.available_packages == []

    def has_available_packages(self):
        """Checks whether Station has any packages in available_packages, returns bool
        """
        
        return self.available_packages != []

    def will_have_available_packages(self, clock):
        """Checks whether Station will have any packages in available_packages at 
        given time
        
        Parameters
        ----------
        clock : datetime.delta
            time to check packages availability by
        """
        
        for pack in self.packages_time:
            if pack.time_available <= clock:
                return True
        return False

    def when_next_package(self):
        """Returns time in datetime.delta of next available package
        """
        
        if not self.packages_time:
            return dt.timedelta.max
        return self.packages_time[0].time_available

    def distance_to(self, stat_id):
        """Returns distance to other Station of given ID
        
        Parameters
        ----------
        stat_id : str
            ID of Station
        """
        
        return self.distances[stat_id]