class Package:
    def __init__(self, id, start, end, time):
        self.id = id
        self.start_station = start
        self.end_station = end
        self.time_available = time

    def __str__(self):
        return f"package ID: {self.id}"

    def __eq__(self, other):
        if isinstance(other, Package):
            return (
                self.id == other.id
                and self.start_station == other.start_station
                and self.end_station == other.end_station
                and self.time_available == other.time_available
            )
        return False