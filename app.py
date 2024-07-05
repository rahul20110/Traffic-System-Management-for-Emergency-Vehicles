from flask import Flask, request, jsonify
import requests
from time import sleep
import threading
from concurrent.futures import ThreadPoolExecutor
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=10)
TARGET_COORDINATES = {'lat': 37.42, 'lon': -122}  # Example: New York City
THRESHOLD_DISTANCE = 10  # kilometers
# Coordinates for each trigger area by approach
# Format: [(lat1, lon1), (lat2, lon2), (lat3, lon3), (lat4, lon4)]
east_bool=False
north_bool=False
south_bool=False
west_bool=False

# East
trigger1_east = [(28.52958376005019, 77.27277711190712), (28.529683345891634, 77.27272869059334),
                 (28.52981580458348, 77.27299720878796), (28.529740390166193, 77.27307864463387)]
trigger2_east = [(28.529390389212807, 77.27237103315278), (28.52947450556951, 77.272322611839),
                 (28.529583760047494, 77.2725328043602), (28.52951027917212, 77.27260763729969)]

# North
trigger1_north = [(28.530292294572074, 77.27051387445871), (28.530379504667803, 77.27069034436298),
                  (28.52998221364731, 77.27071681484861), (28.53005973396402, 77.2708999023743)]
trigger2_north = [(28.52963337151645, 77.27098151970503), (28.529931825410845, 77.27095946096699),
                  (28.52957523104906, 77.27102784305491), (28.529732210237427, 77.27112931324986)]

# South
trigger1_south = [(28.527618840260793, 77.27223100732071), (28.52771441472937, 77.27241231076579),
                  (28.528006167834242, 77.27224054960729), (28.527898856441283, 77.27199435861345)]
trigger2_south = [(28.527969279555226, 77.27194473872323), (28.528064853706052, 77.27217947897317),
                  (28.528373373180443, 77.27198481632688), (28.528249294804752, 77.2717481676196)]

# West
trigger1_west = [(28.528566634260983, 77.26998486126871), (28.528389549013735, 77.27009101541766),
                 (28.528567814828303, 77.27044575839646), (28.528743719210713, 77.27035438520495)]
trigger2_west = [(28.528370659901533, 77.2696381806238), (28.52822781089302, 77.26974433477275),
                 (28.528386007304167, 77.27009504658133), (28.52854538404542, 77.2699969547728)]

# Junction trigger
junction_trigger = [(28.528798799047177, 77.2713286796511), (28.528952061643892, 77.27168301946566),
                    (28.529279340401214, 77.27148313546772), (28.52913406068803, 77.27113242990768)]

trigger_1_bool=False
trigger_2_bool=False
junction_trigger_bool_entry=False
junction_trigger_bool_exit=False
vehicle_point = None
def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def point_in_polygon(point, polygon):
    """ Check if a point (x, y) is inside a polygon defined by a list of (x, y) tuples. """
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside
from threading import Timer

from threading import Timer

def wait_for_trigger2(direction):
    global vehicle_point, trigger_2_bool, east_bool, north_bool, south_bool, west_bool
    # print("Waiting for vehicle to enter trigger2...")
    var=False
    def check_trigger():
        global vehicle_point
        global var
        global trigger_2_bool
        global east_bool
        global north_bool
        global south_bool
        global west_bool

        print("Checking if vehicle has entered trigger2...")
        # print("Current Location ", vehicle_point[0], vehicle_point[1])
        if direction=="east" and point_in_polygon(vehicle_point, trigger2_east):
            print("Vehicle has entered trigger2, sending signal to IoT device...")
            print("Emergency Vehicle is Approaching from East")
            trigger_2_bool = True
            var=True
            success = send_signal_to_iot_device(direction)
            east_bool=True
            if success:
                print("Signal successfully sent to IoT device.")
            else:
                print("Failed to send signal to IoT device.")

            return
        elif direction=="north" and point_in_polygon(vehicle_point, trigger2_north):
            print("Vehicle has entered trigger2, sending signal to IoT device...")
            print("Emergency Vehicle is Approaching from North")
            trigger_2_bool = True
            var=True
            success = send_signal_to_iot_device(direction)
            north_bool=True
            if success:
                print("Signal successfully sent to IoT device.")
            else:
                print("Failed to send signal to IoT device.")
            return
        elif direction=="south" and point_in_polygon(vehicle_point, trigger2_south):
            print("Vehicle has entered trigger2, sending signal to IoT device...")
            print("Emergency Vehicle is Approaching from South")
            trigger_2_bool = True
            var=True
            south_bool=True
            success = send_signal_to_iot_device(direction)
            if success:
                print("Signal successfully sent to IoT device.")
            else:
                print("Failed to send signal to IoT device.")

            return
        elif direction=="west" and point_in_polygon(vehicle_point, trigger2_west):
            print("Vehicle has entered trigger2, sending signal to IoT device...")
            print("Emergency Vehicle is Approaching from West")
            trigger_2_bool = True
            var=True
            west_bool=True
            success = send_signal_to_iot_device(direction)
            if success:
                print("Signal successfully sent to IoT device.")
            else:
                print("Failed to send signal to IoT device.")
            return
            
        else:
            timer = Timer(1, check_trigger)
            timer.start()
    if(var):
        return
    check_trigger()


    
@app.route('/location', methods=['POST'])
def handle_location():
    global vehicle_point, trigger_1_bool, trigger_2_bool, junction_trigger_bool_entry, junction_trigger_bool_exit
    try:
        data = request.get_json(force=True)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        vehicle_point = (latitude, longitude)  # Update vehicle point
        
        # print(f"Received location: {latitude}, {longitude}")
        
        if not trigger_1_bool:
            if point_in_polygon(vehicle_point, trigger1_east):
                print("Vehicle has entered trigger1, waiting for entry into trigger2")
                trigger_1_bool = True
                threading.Thread(target=wait_for_trigger2, args=("east",)).start()
                return jsonify({"message": "Vehicle has entered trigger1. Waiting for entry into trigger2."}), 200
            elif point_in_polygon(vehicle_point, trigger1_north):
                print("Vehicle has entered trigger1, waiting for entry into trigger2")
                trigger_1_bool = True
                threading.Thread(target=wait_for_trigger2, args=("north",)).start()
                return jsonify({"message": "Vehicle has entered trigger1. Waiting for entry into trigger2."}), 200
            elif point_in_polygon(vehicle_point, trigger1_south):
                print("Vehicle has entered trigger1, waiting for entry into trigger2")
                trigger_1_bool = True
                threading.Thread(target=wait_for_trigger2, args=("south",)).start()
                return jsonify({"message": "Vehicle has entered trigger1. Waiting for entry into trigger2."}), 200
            elif point_in_polygon(vehicle_point, trigger1_west):
                print("Vehicle has entered trigger1, waiting for entry into trigger2")
                trigger_1_bool = True
                threading.Thread(target=wait_for_trigger2, args=("west",)).start()
                return jsonify({"message": "Vehicle has entered trigger1. Waiting for entry into trigger2."}), 200

        if trigger_2_bool:
            print("Device is close enough. Sending signal to IoT device...")
            trigger_2_bool = False
            # sleep(2)  # Simulate a delay
            return jsonify({"message": "Device is close enough. Signal sent to IoT device."}), 200
        elif junction_trigger_bool_entry == False:
            if point_in_polygon(vehicle_point, junction_trigger):
                print("Vehicle has entered junction trigger")
                junction_trigger_bool_entry = True
                
                return jsonify({"message": "Vehicle has entered junction trigger."}), 200
        elif junction_trigger_bool_exit == False and junction_trigger_bool_entry == True:
            if point_in_polygon(vehicle_point, junction_trigger) == False:
                print("Emergency Vehicle has passed junction. Restoring normal traffic flow...")
                reset_signal()
                junction_trigger_bool_exit = True
                junction_trigger_bool_entry = False
                trigger_1_bool=False
                trigger_2_bool=False
                junction_trigger_bool_entry=False
                junction_trigger_bool_exit=False
                
                return jsonify({"message": "Vehicle has exited junction trigger."}), 200

        return jsonify({"message": "Device is not close enough."}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Server encountered an unexpected error."}), 500

def reset_signal():
    global east_bool, north_bool, south_bool, west_bool
    IOT_DEVICE_ENDPOINT = None
    if east_bool:
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v2=0"
        east_bool=False
    elif north_bool:
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v1=0"
        north_bool=False
    elif south_bool:
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v3=0"
        south_bool=False
    elif west_bool:
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v4=1"
        west_bool=False
    try:
        response = requests.get(IOT_DEVICE_ENDPOINT)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False


def send_signal_to_iot_device(direction):
    IOT_DEVICE_ENDPOINT = None
    if direction == "east":
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v2=1"
    elif direction == "north":
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v1=1"
    elif direction == "south":
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v3=1"
    elif direction == "west":
        IOT_DEVICE_ENDPOINT = "https://blr1.blynk.cloud/external/api/update?token=GMoA29hBPVQMupQsFdfINWVeIt-SZZ40&v4=1"

    try:
        response = requests.get(IOT_DEVICE_ENDPOINT)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False


if __name__ == '__main__':
    app.run(debug=True, host="10.190.0.6", port=50000)
