from flask import Flask, render_template, request
import datetime
import json

app = Flask(__name__)

# Load data once when the app starts
with open("marc_trains.json", encoding="utf-8") as f:
    trains = json.load(f)

# Extract all unique station names for dropdowns
station_names = ["Perryville", 
                 "Aberdeen", 
                 "Edgewood", 
                 "Martin Airport", 
                 "Penn Station",
                 "West Baltimore", 
                 "Halethorpe",
                 "BWI Rail Station", 
                 "Odenton",
                 "Bowie State",
                 "Seabrook",
                 "New Carrollton",
                 "Union Station Washington"]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        origin = request.form["origin"]
        destination = request.form["destination"]
        arrival_time_input = request.form["arrival_time"]
        arrival_time = datetime.datetime.strptime(arrival_time_input, "%H:%M").time()

        for train in trains:
            departure_time = None
            origin_tracker = 0
            for stop in train["stops"]:
                if origin_tracker == 2:
                    break

                if origin_tracker == 0 and stop["station"] == origin:
                    if isinstance(stop["arrival_time"], str):
                        departure_time = datetime.datetime.strptime(stop["arrival_time"], "%H:%M").time()
                    origin_tracker = 1
                    continue

                if origin_tracker == 1 and stop["station"] == destination:
                    if isinstance(stop["arrival_time"], str):
                        stop["arrival_time"] = datetime.datetime.strptime(stop["arrival_time"], "%H:%M").time()

                    if stop["arrival_time"] <= arrival_time:
                        results.append({
                            "train_id": train["train_id"],
                            "arrival_time": stop["arrival_time"].strftime("%H:%M"),
                            "arrival_station": stop["station"],
                            "departure_time": departure_time.strftime("%H:%M"),
                            "departure_station": origin
                        })
                    origin_tracker = 2

    return render_template("index.html", stations=station_names, results=results)

if __name__ == "__main__":
    app.run(debug=True)
