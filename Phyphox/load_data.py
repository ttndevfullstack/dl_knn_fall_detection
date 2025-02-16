import requests as req
import json
import csv
import time
import os

PHYPHOX_DATA_ENDPOINT = "http://192.168.88.183/get"

params = {
    "accX": "",
    "accY": "",
    "accZ": "",
    "acc_time": "",
}

data_collection = []
csv_directory = "Phyphox"
csv_file = os.path.join(csv_directory, "phyphox_data.csv")


def fetch_phyphox_data():
    try:
        response = req.get(PHYPHOX_DATA_ENDPOINT, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if "buffer" in data and data["buffer"]:
            current_data = {}
            for key, value in data["buffer"].items():
                current_data[key] = value["buffer"][0] if value["buffer"] else None

            print(current_data)
            data_collection.append(current_data)

        else:
            print("No buffer data available.")

    except req.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")


def save_to_csv_file():
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    if data_collection:
        headers = data_collection[0].keys()

        with open(csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            if file.tell() == 0:  # Check file is empty
                writer.writeheader()

            # Write the collected data
            for entry in data_collection:
                writer.writerow(entry)

        # Fresh for next request
        data_collection.clear()


def main():
    while True:
        fetch_phyphox_data()
        save_to_csv_file()
        time.sleep(0.1)

if __name__ == "__main__":
    main()
