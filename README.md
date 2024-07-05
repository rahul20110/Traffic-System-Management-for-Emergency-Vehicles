# ResQSignal

## Overview
ResQSignal is a cutting-edge project developed in April 2024, designed to streamline traffic flow for emergency vehicles through real-time traffic light control. By leveraging Python Flask, Google Cloud Platform (GCP), SIM modules, and Arduino boards, this system ensures emergency vehicles can navigate through intersections more efficiently by dynamically changing traffic lights to green.

## Key Features
- **Real-Time Traffic Light Control:** Utilizes real-time location data from a mobile app to control traffic lights, ensuring emergency vehicles have immediate passage.
- **Python Flask API:** A robust API built with Flask facilitates seamless communication between the mobile app and the server.
- **Google Cloud Platform Hosting:** The system is hosted on GCP, offering reliable and scalable server communication.
- **Hardware Integration:** SIM modules and Arduino boards are integrated to physically control the traffic lights based on the server commands.

## Technologies Used
- Python Flask
- Google Cloud Platform (GCP)
- SIM Modules
- Arduino Boards

## How It Works
1. **Location Tracking:** Emergency vehicles transmit their real-time location using a mobile app.
2. **Server Processing:** The Flask API, hosted on GCP, receives this data and calculates the vehicle's proximity to intersections.
3. **Traffic Light Manipulation:** Commands are sent to the traffic lights via SIM modules and Arduino boards, turning them green as emergency vehicles approach.

## Demonstration
For a detailed demonstration of ResQSignal in action, watch our video on YouTube:
[![ResQSignal Demonstration](https://www.youtube.com/watch?v=VQpYAUBQMxY)](https://www.youtube.com/watch?v=VQpYAUBQMxY)
