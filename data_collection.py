import requests
import json

def get_sensor_data():
    try:
        response = requests.get("https://thingspeak.mathworks.com/channels/2911126/private_show")  
        data = response.json()
        temperature = data["temperature"]
        humidity = data["humidity"]
        gas = data["gas"]
        return temperature, humidity, gas
    except Exception as e:
        print(f"Error fetching sensor data: {e}")
        return 0, 0, 0  
