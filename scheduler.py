import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler

url = "https://ogcapi.hft-stuttgart.de/sta/udigit4icity/v1.1/Observations"

def fetch():
    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        # Save data to a file
        with open("data.json", "w") as f:
            json.dump(data, f)

        print("Data fetched successfully and saved.")
    except Exception as e:
        print(f"Error fetching data: {e}")

def start_scheduler():
    # Initialize and start the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch, "interval", minutes=10)
    scheduler.start()

    # Initial fetch
    fetch()
