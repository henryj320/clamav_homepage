"""Return details on when ClamAV was last run."""

from datetime import datetime
from distutils.util import strtobool
import time
import os
from dotenv import load_dotenv
from fastapi import FastAPI



app = FastAPI()

@app.get("/")
def read_root() -> dict:
    """Return the status of ClamAV to the endpoint.

    Returns:
        dict: Dict containing the details of ClamAV.
    """

    load_dotenv(dotenv_path="/updates/.env", override=True)

    # Read virusEvent and convert it to a boolean.
    virus_event = os.getenv('virusEvent', 'False')

    virus = strtobool(virus_event)
    if virus:
        plaintext = "🔴 Virus Detected! 🔴"

        with open('/updates/trigger.txt', 'a', encoding='utf-8') as trigger_file:
            today = datetime.fromtimestamp(time.time()).strftime('%d %B at %H:%M')
            trigger_file.write(today)

    else:
        plaintext = "No viruses found"

    try:
        log_time, log_time_unit = calculate_last_modified('/logs/clamav.log')
    except:
        log_time = 0
        log_time_unit = "seconds"
    log_time_combined = f"{log_time} {log_time_unit}"

    try:
        event_time, event_time_unit = calculate_last_modified('/updates/trigger.txt')
    except:
        event_time = 0
        event_time_unit = "seconds"
    event_time_combined = f"{event_time} {event_time_unit}"

    output = {
        "virus_event": virus_event,
        "plaintext": plaintext,
        "time": log_time_combined, 
        "last_event": event_time_combined
    }
    return output


def calculate_last_modified(location: str) -> tuple:
    """Return when the file was last modified

    Args:
        location (str): Path to the file

    Returns:
        tuple: The time and units since the file was last modified.
    """

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
# pylint --max-line-length=240 ./main.py
