import random

# Generate random station IDs
stat_ids = ["POL" + str(k) for k in range(20)]

# Generate the first text file
with open("packages.txt", "w") as f:
    for k in range(50):
        package_id = k
        start = random.choice(stat_ids)
        end = random.choice(stat_ids)
        while start == end:
            end = random.choice(stat_ids)
        hour = 6
        minute = "00"
        f.write(f"{package_id} {start} {end} {hour}:{minute}\n")

    for k in range(50, 120):
        package_id = k
        start = random.choice(stat_ids)
        end = random.choice(stat_ids)
        while start == end:
            end = random.choice(stat_ids)
        hour = random.randint(6, 15)  # Random time between 6:00 and 22:00
        minute = random.randint(0, 59)
        if minute in range(10):
            minute = "0" + str(minute)
        f.write(f"{package_id} {start} {end} {hour}:{minute}\n")



def generate_distances(stations, file_name):
    distances = []
    connections = {}
    visited = set()
    visited.add(stations[0])
    while len(visited) < len(stations):
        station1 = random.choice(list(visited))
        station2 = random.choice(stations)
        if station2 not in visited:
            distance = random.randint(10, 40)
            distances.append((station1, station2, distance))
            connections[station1] = station2
            visited.add(station2)

    for _ in range(len(stations) ** 2 // 15):
        station1 = random.choice(stations)
        station2 = random.choice(stations)
        while station1 == station2:
            station2 = random.choice(stations)
        if (station1, station2) not in connections.items():
            distance = random.randint(10, 40)
            distances.append((station1, station2, distance))

    with open(file_name, "w") as file:
        for distance in distances:
            file.write(f"{distance[0]} {distance[1]} {distance[2]}\n")



generate_distances(stat_ids, "station_network.txt")

