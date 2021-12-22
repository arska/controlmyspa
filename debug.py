"""
Dump the details for a spa for debugging

use e.g. with "python debug.py user@example.com myverysecretpassword"
"""
import argparse
import logging

from controlmyspa import ControlMySpa
import pprint

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
info = API._info

# remove potentially sensitive information
del info["owner"]
del info["p2pAPSSID"]
del info["serialNumber"]
del info["_id"]
del info["_links"]

# print remaining data
pprint.pprint(API._info)
