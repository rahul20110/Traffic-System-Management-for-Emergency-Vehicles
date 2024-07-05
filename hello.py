from flask import Flask, request, jsonify
import requests
from time import sleep
def send_signal_to_iot_device(direction):
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

success = send_signal_to_iot_device("north")
if success:
    print("Signal successfully sent to IoT device.")
else:
    print("Failed to send signal to IoT device.")
