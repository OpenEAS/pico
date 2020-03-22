import feedparser
import time
import os
import pty
import serial
import requests

CAP_URI = "https://alerts.weather.gov/cap/or.php?x=0"
DELAY = 1 # Seconds between checks
PHYSICAL_SERIAL = None # Set to a physical serial port path to output there
PHYSICAL_BAUD = 9600   # Baud rate of the physical serial port. If using a virtual port, this can be set to None

print("Starting picoENDEC.")
print("Verifying connectivity to CAP server...", end="", flush=True)

try:
    r = requests.get(CAP_URI)
except requests.exceptions.ConnectionError as e:
    print("ERROR")
    print(e)
else:
    print("SUCCESS")

    print("Verifying CAP format...................", end="", flush=True)
    if r.status_code == 200:
        if r.text.split("<id>")[1].split("</id>")[0] == CAP_URI:
            print("SUCCESS")
        else:
            print("FAIL")
            print("Error detecting CAP data.")
    else:
        print("FAIL")
        print("Invalid HTTP status code. Server reported " + str(r.status_code))


if not PHYSICAL_SERIAL:
    print("Initializing virtual serial port.......", end="", flush=True)

    try:
        master, slave = pty.openpty()
        port_name = os.ttyname(slave)
        ser = serial.Serial(port_name)
    except Exception as e:
        print("FAIL")
        print(e)
    else:
        print("SUCCESS")
else:
    print("Initializing physical serial port.......", end="", flush=True)
    try:
        ser = serial.Serial(PHYSICAL_SERIAL, PHYSICAL_BAUD)
    except Exception as e:
        print("FAIL")
        print(e)
    else:
        print("SUCCESS")

print()
print("Recieved CAP data in " + str(round(r.elapsed.total_seconds(), 2)) + " seconds.")
print("Virtual serial port ready at " + port_name)
print()
print("picoENDEC monitoring.\n")

last_value = ""
while True:
    feed = feedparser.parse("https://alerts.weather.gov/cap/or.php?x=0")

    for entry in feed["items"]:
        title = entry["title"]
        summary = entry["summary"]

        # Time data
        published = entry["published"]
        updated = entry["updated"]
        effective = entry["cap_effective"]
        expires = entry["cap_expires"]

        # CAP Data
        event = entry["cap_event"]
        urgency = entry["cap_urgency"]
        severity = entry["cap_severity"]
        certainty = entry["cap_certainty"]
        area = entry["cap_areadesc"]

        value = entry["value"]

        raw = title + "\n"
        for x in summary.split(" * "):
            raw += x + "\n"
        raw += value

        mini = event + "\n"
        mini += "Effective " + effective + "\n"
        mini += "Urgency: " + urgency + "\n"
        mini += "Severity: " + severity + "\n"
        mini += "Certainty: " + certainty + "\n"
        mini += "Area: " + area


        if value != last_value:
            ser.write("<ENDECSTART>".encode())
            ser.write(raw.encode())
            ser.write("<ENDECEND>".encode())

            print(raw)
            print()

            last_value = value

    time.sleep(DELAY)
