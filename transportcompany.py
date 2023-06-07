from packages import Packages
from stationnetwork import StationNetwork
from driver import Driver
import datetime as dt

class TransportCompany:
    """
    Class representing the whole transport company. This is where all supplementary
    classes are used
    
    Attribues
    ---------
    stationnet : StationNetwork
        represents the network of stations managed by the company
    packages : Packages
        represents the packages managed by the company
        
    Methods
    -------
    """
    
    def __init__(self, packages_file, stations_file):
        """
        Parameters
        ----------
        packages_file : str
            path to file with packages information each line being in
            following format: unique ID, ID of source station, ID of destination,
            time (HH:MM) of availability at source station
        stations_file : str
            path to file with information about the network of stations each line being
            in the following format: Station1 ID, Station2 ID, distance
        """
        
        self.stationnet = StationNetwork(stations_file)
        self.packages = Packages(packages_file)
        self.distribute_packages()
 
    def distribute_packages(self):
        """Parses through all instances of Package in packages attribute and assigns them
        to their appropriate source station"""
        
        for pack_id in self.packages.get_packages():
            pack = self.packages.get_package(pack_id)
            start_station = self.stationnet.get_station(pack.start_station)
            start_station.add_package(pack)

    def create_itineraries(self, wtf=False):
        """Returns a dictionary containing itineraries for all drivers
        
        The basic structure of this simulation is as follows:
        
        1. While there are undelivered packages in the network instantiate a Driver
        2. If Driver's worktime remaining is greater than zero, their current time is less than 24:00 and they can travel anywhere, keep working
            
            a. If there are available packages at current station, take the first one  available and deliver it
            b. Else:
            
                1. Calculate wait time: how long until next available package at current station and travel time: shortest time to another station that will have an available package upon arrival
                2. If wait time is less than or equal to travel time, wait for the next package and then pick it up and deliver. Go back to a.
                3. If travel time is less than wait time, travel to another station, wait there for a package if needed, pick it up and deliver. Go back to a.
            
            c. Go back to 2
            
        3. Go back to 1.
        
        Once the Driver finishes work (conditions in 2. are not met), their itinerary is added to a dictionary containing all
        itineraries.
        
        This implemntation has its flaws. For one, it is possible for a loop iteration to create an "empty" Driver itinerary (a Driver that does not deliver a single package).
        Within this code paradigm, it is not exactly possible to fully prevent this from happening. To cope with this, if a Driver does not deliver a single package,
        their itinerary is ignored and removed. 
        
        Parameters
        __________  
        wtf : bool
            optional argument set by default to False determining whether to write
            the drivers' itineraries to a text file
               
        """
        
        itineraries = {}
        k = 1
        while not self.stationnet.is_empty():
            driver = Driver(k, self.stationnet) # create driver and itinerary list for them
            while driver.work_time_remaining > dt.timedelta() and driver.clock <= dt.timedelta(days=1) and\
                    driver.can_travel_anywhere(): # driver works for max 8h or until 24:00
                self.stationnet.update_packages(driver.clock)

                if driver.current_station.has_available_packages(): # if possible, pick up package from here and travel
                    # print("*driver picks up from current station*")
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
                                #stat = None

                    if wait_time > dt.timedelta(days=1) and travel_time > dt.timedelta(days=1):
                        break
                    
                    if wait_time <= travel_time:
                        # if driver.work_time_remaining - wait_time <= dt.timedelta() or wait_time > dt.timedelta(hours=8) or\
                        #     driver.clock + wait_time >= dt.timedelta(days=1):
                        #     break
                        # print('*driver waits*')
                        if driver.itinerary: # if it's not driver's first action
                            driver.itinerary.append(f"[{driver.clock_print()}]: WAIT at station {driver.current_station.id} for {wait_time.seconds // 60} minutes")
                            driver.pass_time(wait_time.seconds // 60)
                            driver.current_station.update_packages(driver.clock)
                        else:
                            driver.clock += wait_time
                            driver.current_station.update_packages(driver.clock)
                        driver.pickup_and_travel()

                    else:
                        if not driver.itinerary:
                            driver.itinerary.append(f"[{driver.clock_print()}]: START work at station {driver.current_station.get_id()}")
                        # print("*driver travels elsewhere*")
                        driver.itinerary.append(f"[{driver.clock_print()}]: TRAVEL to station {stat.id} from {driver.current_station.get_id()}")
                        driver.travel_to(stat.id)
                        driver.itinerary.append(f"[{driver.clock_print()}]: ARRIVE at station {driver.current_station.get_id()}")
                        if not driver.current_station.has_available_packages():
                            wait_time = driver.current_station.when_next_package() - driver.clock
                            if driver.clock + wait_time >= dt.timedelta(hours=23, minutes=59):
                                break
                            driver.itinerary.append(f"[{driver.clock_print()}]: WAIT at station {driver.current_station.id} for {wait_time.seconds // 60} minutes")
                            driver.pass_time(wait_time.seconds // 60)
                            driver.current_station.update_packages(driver.clock)
                        driver.pickup_and_travel()


            driver.itinerary.append(f"[{driver.clock_print()}]: FINISH work at station {driver.current_station.id}")
            total_worktime = dt.timedelta(hours=8) - driver.work_time_remaining
            driver.itinerary.append(f"Total work time: {total_worktime.seconds // 3600} hours and {total_worktime.seconds % 3600 // 60} minutes")
            driver.itinerary.append(f"Number of packages delivered: {driver.packages_delivered}")
            itineraries[k] = driver.itinerary
            if driver.packages_delivered == 0:
                del itineraries[k]
                #k -= 1
            self.stationnet.reset_packages()
            # print(self.stationnet.num_packages_left())
            # print("----------------")
            k += 1
            
        if wtf:
            with open("driver itineraries", "w") as f:
                for dri in itineraries:
                    f.write(f"Driver {dri}\n")
                    for step in itineraries[dri]:
                        f.write(f"{step}\n")
                    f.write("----------\n")
                f.write(f"Number of drivers: {len(itineraries)}")
                    

        return itineraries


if __name__ == "__main__":
    transpol = TransportCompany("packages.txt", "station_network.txt")
    #print(transpol.stationnet.get_station("POL0").distances)
    #print(transpol.stationnet.get_station("POL15").packages_time)
    #print(transpol.stationnet.is_empty())
    #print(transpol.packages.get_package("100").end_station)
    #print(transpol.stationnet.get_station("POL0").available_packages)
    its = transpol.create_itineraries(wtf=True)
    for dri in its:
        print(f"Driver {dri}") 
        for steps in its[dri]:
            print(steps)
        print("-----------")
    print(f"Number of drivers: {len(its)}")