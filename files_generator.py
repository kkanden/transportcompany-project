import random

# Generate random station IDs


# Generate the first text file
def generate_files(n_stations, n_packages, file_name_stat, file_name_pack):
    stat_ids = ["POL" + str(k) for k in range(n_stations)]
    with open(file_name_pack, "w") as f:
        for k in range(n_packages // 5):
            package_id = k
            start = random.choice(stat_ids)
            end = random.choice(stat_ids)
            while start == end:
                end = random.choice(stat_ids)
            hour = 6
            minute = "00"
            f.write(f"{package_id} {start} {end} {hour}:{minute}\n")

        for k in range(n_packages // 5, n_packages):
            package_id = k
            start = random.choice(stat_ids)
            end = random.choice(stat_ids)
            while start == end:
                end = random.choice(stat_ids)
            hour = random.randint(6, 19)  # Random time between 6:00 and 22:00
            minute = random.randint(0, 59)
            if minute in range(10):
                minute = "0" + str(minute)
            f.write(f"{package_id} {start} {end} {hour}:{minute}\n")


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

    with open(file_name_stat, "w") as file:
        for distance in distances:
            file.write(f"{distance[0]} {distance[1]} {distance[2]}\n")



generate_files(20, 50, "station_network.txt", "packages.txt")

