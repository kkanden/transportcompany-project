import random


# Generate random station IDs


# Generate the first text file
def generate_files(n_stations: int, n_packages: int, file_name_station: str, file_name_package: str):
    """Generates two text files: one containing information of n_packages packages (unique ID, source station
    destination, time of availability at source station (HH:MM)), the other containing information of a station network
    with n_station Stations (Station1 ID, Station2 ID, distance)

    Parameters
    ----------
    n_stations : int
        number of stations in the network to be generated
    n_packages : int
        number of packages to be generated
    file_name_station : str
        path to file to generate station network information to
    file_name_package : str
        path to file to generate packages information to 
    """

    assert n_stations > 1
    assert n_packages > 0
    stat_ids = ["POL" + str(k) for k in range(n_stations)]

    # Generate packages with time available between 6:00 and 14:59
    with open(file_name_package, "w") as f:
        for k in range(n_packages // 3):
            package_id = k
            start = random.choice(stat_ids)
            end = random.choice(stat_ids)
            while start == end:
                end = random.choice(stat_ids)
            hour = 6
            minute = "00"
            f.write(f"{package_id} {start} {end} {hour}:{minute}\n")

        for k in range(n_packages // 4, n_packages):
            package_id = k
            start = random.choice(stat_ids)
            end = random.choice(stat_ids)
            while start == end:
                end = random.choice(stat_ids)
            hour = random.randint(6, 14)  # Random time between 6:00 and 22:00
            minute = random.randint(0, 59)
            if minute in range(10):
                minute = "0" + str(minute)
            f.write(f"{package_id} {start} {end} {hour}:{minute}\n")

    # Generate Station Network ensuring that you can travel to every station from a given station
    distances = []
    connections = {}
    visited = set()
    visited.add(stat_ids[0])
    while len(visited) < len(stat_ids):
        station1 = random.choice(list(visited))
        station2 = random.choice(stat_ids)
        if station2 not in visited:
            distance = random.randint(10, 40)
            distances.append((station1, station2, distance))
            connections[station1] = station2
            visited.add(station2)

    for _ in range(len(stat_ids) ** 2 // 15):
        station1 = random.choice(stat_ids)
        station2 = random.choice(stat_ids)
        while station1 == station2:
            station2 = random.choice(stat_ids)
        if (station1, station2) not in connections.items():
            distance = random.randint(10, 40)
            distances.append((station1, station2, distance))

    with open(file_name_station, "w") as f:
        for distance in distances:
            f.write(f"{distance[0]} {distance[1]} {distance[2]}\n")


if __name__ == "__main__":
    generate_files(50, 2000, "station_network.txt", "packages.txt")
