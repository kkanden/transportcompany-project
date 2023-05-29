class Package:
    def __init__(self, id, start, end, time):
        self.id = id
        self.start_station = start
        self.end_station = end
        self.time_available = time