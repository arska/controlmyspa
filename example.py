"""
Example usage of controlmyspa module

use e.g. with "python example.py user@example.com myverysecretpassword"
"""
import argparse
import logging

from controlmyspa import ControlMySpa

PARSER = argparse.ArgumentParser(description="Get metrics from Balboa Controlmyspa")
PARSER.add_argument(
    "-v", "--verbose", help="enable debug logging", action="store_true", default=False,
)
PARSER.add_argument("email", help="email to log in to controlmyspa.com")
PARSER.add_argument("password", help="password to log in to controlmyspa.com")
ARGS = PARSER.parse_args()

LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

if ARGS.verbose:
    logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=LOGFORMAT)
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(
        logging.WARNING
    )

logging.debug("starting with arguments: %s", ARGS)

API = ControlMySpa(ARGS.email, ARGS.password)
print("current temp", API.current_temp)
print("desired temp", API.desired_temp)

# API.desired_temp = 36 if API.desired_temp == 37 else 37

print("temp range", API.temp_range)
print("panel lock", API.panel_lock)

print("lights", API.lights)

# toggle lights
# API.lights = [not x for x in API.lights]

print("jets", API.jets)

# toggle jets
# API.set_jet(0, not API.get_jet(0))
# API.set_jet(1, not API.get_jet(1))
# API.set_jet(2, not API.get_jet(2))

print("blowers", API.blowers)
