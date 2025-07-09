import datetime
import json

with open("marc_trains.json", mode="r", encoding="utf-8") as read_file:
    trains = json.load(read_file)

origin = input("Enter the origin station: ")
destination = input("Enter the destination station: ")

arrival_time = input("Enter an arrival time (24 hr format): ")

arrival_time = datetime.datetime.strptime(arrival_time, "%H:%M").time()

origin_tracker = 0

for train in trains:
    for stop in train["stops"]:
        print(stop)
        if origin_tracker == 2:
            origin_tracker = 0
            break

        if stop["station"] == origin:
            origin_tracker = 1
            continue

        while origin_tracker==1 and stop["station"] == destination:
            stop["arrival_time"] = datetime.datetime.strptime(stop["arrival_time"], "%H:%M").time()
            if stop["arrival_time"] < (arrival_time):
                print(train["train_id"])
                origin_tracker = 2
                continue
        


        