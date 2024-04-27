from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from distutils.util import strtobool
from datetime import datetime
import time
import math



app = FastAPI()

@app.get("/")
def read_root() -> dict:
    
    load_dotenv(dotenv_path="/updates/.env", override=True)

    # Read virusEvent and convert it to a boolean.
    virus_event = os.getenv('virusEvent', 'False')

    bool = strtobool(virus_event)
    if bool:
        plaintext = "🔴 Virus Detected! 🔴"
    else:
        plaintext = "No viruses found"

    try:
        time, time_unit = calculate_last_modified('/logs/clamav.log')
    except:
        time = 0
        time_unit = "seconds"
    time_combined = f"{time} {time_unit}"

    try:
        event_time, event_time_unit = calculate_last_modified('/updates/.env')
    except:
        event_time = 0
        event_time_unit = "seconds"
    event_time_combined = f"{event_time} {event_time_unit}"

    dict = {
        "virus_event": virus_event,
        "plaintext": plaintext,
        "time": time_combined, 
        "last_event": event_time_combined
    }
    return dict

def calculate_last_modified(location: str) -> tuple:

    # Get how long ago the file was modified.
    time_modified = os.path.getmtime(location)
    seconds_since_modified = int(time.time() - time_modified)

    # Convert the number to minutes, hours or days as required.
    if seconds_since_modified < 60:
        return seconds_since_modified, "seconds"
    minutes_since_modified = int(seconds_since_modified / 60)
    if minutes_since_modified < 60:
        return minutes_since_modified, "minutes"
    hours_since_modified = int(minutes_since_modified / 60)
    if hours_since_modified < 24:
        return hours_since_modified, "hours"
    days_since_modified = int(hours_since_modified / 24)
    return days_since_modified, "days"


# docker compose up -d --force-recreate --build
# docker exec -it clamav_homepage sh
# docker logs clamav_homepage
