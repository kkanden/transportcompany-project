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
    time : str
        time given in HH:MM format representing the time the package
        will be available at source station
        
    Methods
    --------
    """
    def __init__(self, id, start, end, time):
        """ 
        
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
        self.id = id
        self.start_station = start
        self.end_station = end
        self.time_available = time