from package import Package
import datetime as dt

class Packages:
    """ 
    Class representing all packages present in station network.
    
    Attributes
    ----------
    packages_file : str
        path to file with packages information each line being in
        following format: unique ID, ID of source station, ID of destination,
        time (HH:MM) of availability at source station
    packages : dict
        dictionary with keys being package IDs and values being instances
        of Package class
        
    Methods 
    -------
    """
    def __init__(self, packages_file):
        """
        Parameters
        ----------
        packages_file : str
            path to file with packages information each line being in
            following format: unique ID, ID of source station, ID of destination,
            time (HH:MM) of availability at source station 
        """
        self.packages_file = packages_file
        self.packages = {}
        self.create_packages()

    def create_packages(self):
        """creates instances of Package from packages_file and 
        puts them inpackages attribute using add_package method"""
        
        with open(self.packages_file, 'r') as f:
            for line in f:
                line = line.strip().split()
                pack_id, start, end, time_pack = line[0], line[1], line[2], dt.datetime.strptime(line[3], "%H:%M").time()
                if start == end:
                    continue
                time_pack = dt.timedelta(seconds=3600 * time_pack.hour + 60 * time_pack.minute)
                self.add_package(pack_id, start, end, time_pack)

    def add_package(self, id, start, end, time_pack):
        """Creates single instance of Package with given variables and puts it in
        packages attribute
        
        Parameters
        ----------
        id : str
            a unique package ID
        start_station : str
            ID of source station
        end_station : str
            ID of destination
        time : str
            time given in HH:MM format representing the time the package
            will be available at source station
        """
        
        new_package = Package(id, start, end, time_pack)
        self.packages[id] = new_package

    def get_package(self, pack_id):
        """Returns instance of Package with given ID

        Parameters
        ----------
        pack_id : str
            unique ID of package
        """
        return self.packages[pack_id]

    def get_packages(self):
        """Returns all instances of Package from packages attribute"""
        return self.packages.keys()

