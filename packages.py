from package import Package
import datetime as dt

class Packages:
    def __init__(self, packages_file):
        self.packages_file = packages_file
        self.packages = {}
        self.create_packages()

    def create_packages(self):
        with open(self.packages_file, 'r') as f:
            for line in f:
                line = line.strip().split()
                pack_id, start, end, time_pack = line[0], line[1], line[2], dt.datetime.strptime(line[3], "%H:%M").time()
                if start == end:
                    continue
                time_pack = dt.timedelta(seconds=3600 * time_pack.hour + 60 * time_pack.minute)
                self.add_package(pack_id, start, end, time_pack)

    def add_package(self, pack_id, start, end, time_pack):
        new_package = Package(pack_id, start, end, time_pack)
        self.packages[pack_id] = new_package

    def get_package(self, pack_id):
        return self.packages[pack_id]

    def get_packages(self):
        return self.packages.keys()

    def is_empty(self):
        return bool(self.packages)

