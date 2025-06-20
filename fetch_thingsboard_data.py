import requests

THINGSBOARD_URL = "http://demo.thingsboard.io/api/plugins/telemetry/DEVICE/device_id/values/timeseries"
HEADERS = {"X-Authorization": "Bearer your_jwt_token"}

def get_sensor_data():
    response = requests.get(THINGSBOARD_URL, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        temperature = data["temperature"][-1]["value"]
        humidity = data["humidity"][-1]["value"]
        gas = data["gas"][-1]["value"]
        return float(temperature), float(humidity), float(gas)
    else:
        print("Failed to fetch data")
        return None

if __name__ == "__main__":
    print(get_sensor_data())
