class Package:
    """
    Class representing a single package. 
    
    Attributes
    ----------
    id : str
        a unique package ID
    start_station : str
        ID of source station
    end_station : str
        ID of destination
    time_available : str
        time given in HH:MM format representing the time the package
        will be available at source station
        
    Methods
    --------
    """
    
    def __init__(self, package_id: str, start_station: str, end_station: str, time_available: str):
        """ 
        
        Parameters
        ----------
        package_id : str
            a unique package ID
        start_station : str
            ID of source station
        end_station : str
            ID of destination
        time : str
            time given in HH:MM format representing the time the package
            will be available at source station
        """
        
        self.id = package_id
        self.start_station = start_station
        self.end_station = end_station
        self.time_available = time_available