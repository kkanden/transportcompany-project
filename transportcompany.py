from packages import Packages
from stationnetwork import StationNetwork
from driver import Driver
import datetime as dt

class TransportCompany:
    def __init__(self, packages_file, stations_file):
        self.stationnet = StationNetwork(stations_file)
        self.stationnet.create_network()
        self.packages = Packages(packages_file)
        self.distribute_packages()
        # self.stationnet.update_packages(dt.timedelta(hours=6))

    def distribute_packages(self):
        for pack_id in self.packages.get_packages():
            pack = self.packages.get_package(pack_id)
            start_station = self.stationnet.get_station(pack.start_station)
            start_station.add_package(pack)

    def simulation(self):
        itineraries = {}
        k = 0
        while not self.stationnet.is_empty():
            k += 1
            driver = Driver(k, self.stationnet) #create driver and itinerary list for them
            while driver.work_time_remaining > dt.timedelta() and driver.clock <= dt.timedelta(days=1) and\
                    driver.can_travel_anywhere(): #driver works for max 8h or until 24:00
                self.stationnet.update_packages(driver.clock)

                if driver.current_station.has_available_packages(): #if possible, pick up package from here and travel
                    print("*driver picks up from current station*")
                    driver.pickup_and_travel()

                else: # check if better to wait here or travel to the closest station with available package (waiting preferred)
                    wait_time = driver.current_station.when_next_package() - driver.clock
                    travel_time = dt.timedelta.max
                    stat = None
                    for stat_id, distance in driver.current_station.distances.items(): # distances are sorted nondecreasing
                        stat = self.stationnet.get_station(stat_id)
                        if not stat.is_empty():
                            if stat.will_have_available_packages(driver.clock + dt.timedelta(minutes=distance)):
                                travel_time = dt.timedelta(minutes=distance)
                                break # break because this will be minimal time
                            else:
                                travel_time = min(stat.when_next_package() - driver.clock, travel_time)

                    if wait_time <= travel_time:
                        print('*driver waits*')
                        if driver.itinerary: # if it's not driver's first action
                            driver.itinerary.append(f"[{driver.clock_print()}]: Wait at station {driver.current_station.id} for {wait_time.seconds // 60} minutes")
                        driver.pass_time(wait_time.seconds // 60)
                        driver.current_station.update_packages(driver.clock)
                        driver.pickup_and_travel()

                    else:
                        if not driver.itinerary:
                            driver.itinerary.append(f"[{driver.clock_print()}]: START work")
                        #if driver.can_travel_to(stat.id):
                        print("*driver travels elsewhere*")
                        driver.itinerary.append(f"[{driver.clock_print()}]: Travel to station {stat.id}")
                        driver.travel_to(stat.id)
                        driver.itinerary.append(f"[{driver.clock_print()}]: Arrive at station {driver.current_station.get_id()}")
                        driver.pickup_and_travel()

                #print(driver.itinerary)

            driver.itinerary.append(f"[{driver.clock_print()}]: FINISH work at station {driver.current_station.id}")
            total_worktime = dt.timedelta(hours=8) - driver.work_time_remaining
            driver.itinerary.append(f"Total work time: {total_worktime.seconds // 3600} hours and {total_worktime.seconds % 3600 // 60} minutes")
            driver.itinerary.append(f"Number of packages delivered: {driver.packages_delivered}")
            itineraries[k] = driver.itinerary
            if driver.packages_delivered == 0:
                del itineraries[k]
            self.stationnet.reset_packages()
            print(self.stationnet.num_packages_left())
            print("----------------")

        return itineraries


if __name__ == "__main__":
    transpol = TransportCompany("packages.txt", "station_network.txt")
    #print(transpol.stationnet.get_station("POL0").distances)
    #print(transpol.stationnet.get_station("POL15").packages_time)
    #print(transpol.stationnet.is_empty())
    #print(transpol.packages.get_package("100").end_station)
    #print(transpol.stationnet.get_station("POL0").available_packages)
    its = transpol.simulation()
    for dri in its:
        print(f"Driver {dri}") 
        for steps in its[dri]:
            print(steps)
        print("-----------")
    print(f"Number of drivers: {len(its)}")