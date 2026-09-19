"""
Python module to get metrics from and control Balboa ControlMySpa whirlpools
"""

import http
import logging
import time

import requests

_LOGGER = logging.getLogger(__name__)


class SpaOfflineError(Exception):
    """Raised when the spa API response does not contain 'currentState',
    which typically indicates the spa gateway is offline."""


class ControlMySpa:
    """
    Class representing Balboa ControlMySpa whirlpools
    """

    _email = None
    _password = None

    def __init__(self, email, password, spa_offset=0):
        """
        Initialize connection to Balboa ControlMySpa cloud API
        :param email: email address used to log in
        :param password: password used to log in
        :param spa_offset: which spa to use if the user has access to multiple.
            Starts and defaults to zero.
        """
        self._email = email
        self._password = password
        self._spa_offset = spa_offset
        self._spa_id = None
        self._list = None

        """
        2023-12-13: iot.controlmyspa.com has a new TLS certificate, probably since
        June 2023. This certificate is signed by digicert, but there is an intermediate
        certificate missing in the python certifi trust store and the server does not
        provide it (anymore?). Instead of disabling the TLS certificate validation, we
        download the intermediate certificate from digicert over a successfully
        verified TLS connection and add it to the local trust store. Sorry for the hack."""
        """
        try:
            self._get_idm()
        except requests.exceptions.SSLError:
            print("TLS certificate missing, downloading to " + certifi.where())
            customca = requests.get(
                "https://cacerts.digicert.com/RapidSSLTLSRSACAG1.crt.pem", timeout=10
            ).content
            cafile = certifi.where()
            with open(cafile, "ab") as outfile:
                outfile.write(b"\n")
                outfile.write(customca)
                outfile.close()
        """
        # log in and fetch pool info
        self._do_login()
        self.refresh()

    def _do_login(self):
        """
        Log in and get API access tokens
        """
        response = requests.post(
            "https://iot.controlmyspa.com/auth/login",
            json={
                "email": self._email,
                "password": self._password,
            },
            timeout=10,
        )
        if response.status_code != requests.codes.ok:
            _LOGGER.warning("error from controlmyspa API: %s", response.text)
            response.raise_for_status()
        self._iam = response.json()
        self._token = self._iam["data"]["accessToken"]
        return self._iam

    def _send(self, method, path, **kwargs):
        """
        Make one authenticated request, without inspecting the result
        """
        return requests.request(
            method,
            "https://iot.controlmyspa.com" + path,
            headers={"Authorization": "Bearer " + self._token},
            timeout=10,
            **kwargs,
        )

    def _request(self, method, path, **kwargs):
        """
        Make an authenticated request, logging in again if the token expired.

        A client that outlives its access token gets a 401 that is not a
        failure to report: it means log in and make the call again. A second
        401 in a row is a real one and raises, so credentials that are simply
        wrong do not turn into a login loop.
        """
        response = self._send(method, path, **kwargs)
        if response.status_code == http.HTTPStatus.UNAUTHORIZED:
            _LOGGER.info("access token rejected, logging in again")
            self._do_login()
            response = self._send(method, path, **kwargs)
        if response.status_code != requests.codes.ok:
            _LOGGER.warning("error from controlmyspa API: %s", response.text)
            response.raise_for_status()
        return response.json()

    def _get_json(self, path):
        """
        GET an authenticated API path and return the decoded body
        """
        return self._request("GET", path)

    def _post_json(self, path, payload):
        """
        POST a command to an authenticated API path and return the decoded body
        """
        return self._request("POST", path, json=payload)

    def _get_spa_id(self):
        """
        Look up the id of the selected spa. It does not change, so only once.
        """
        if self._spa_id is None:
            self._list = self._get_json("/spas/owned")
            self._spa_id = self._list["data"]["spas"][self._spa_offset]["_id"]
        return self._spa_id

    @staticmethod
    def _current_state(dashboard):
        """
        Map the dashboard onto the legacy currentState names, or None when the
        dashboard carries no reading
        """
        if not dashboard.get("hasCurrentState") or dashboard.get("currentTemp") in (
            None,
            "",
        ):
            return None
        return {
            "currentTemp": dashboard["currentTemp"],
            "desiredTemp": dashboard["desiredTemp"],
            "celsius": dashboard["isCelsius"],
            "tempRange": dashboard["tempRange"],
            "heaterMode": dashboard["heaterMode"],
            "panelLock": dashboard["isPanelLocked"],
            "online": dashboard["isOnline"],
            "components": dashboard.get("components") or [],
        }

    def refresh(self, retries=3, retry_delay=5):
        """
        Re-read the spa state over the existing session.

        A caller that keeps the client alive calls this instead of building a
        new one: the token and the spa id are already known, so it costs one
        request instead of three.

        Retries a few times if currentState is missing (gateway may be temporarily offline).

        Since 2026-08 the API no longer serves GET /spas. The spa is looked up
        via /spas/owned and read via /spas/{id}/dashboard, whose fields are
        mapped back onto the legacy currentState so callers see no change.
        """
        spa_id = self._get_spa_id()
        for attempt in range(retries):
            dashboard = self._get_json(f"/spas/{spa_id}/dashboard")["data"]
            self._info = {
                "_id": spa_id,
                "serialNumber": dashboard.get("serialNumber"),
                "currentState": self._current_state(dashboard),
                "dashboard": dashboard,
            }
            if self._info["currentState"]:
                return self._info
            if attempt < retries - 1:
                _LOGGER.warning(
                    "Spa data missing 'currentState', retrying in %ds (%d/%d)",
                    retry_delay,
                    attempt + 1,
                    retries,
                )
                time.sleep(retry_delay)
        raise SpaOfflineError(
            f"Spa data does not contain 'currentState' after {retries} attempts"
            " — the spa gateway may be offline"
        )

    @property
    def info(self):
        """
        The spa state as the API returned it, as of the last refresh().

        The shape is Balboa's, not this library's, and can change without
        notice; the typed properties below are the stable way to read a
        value. This is here for logging and debugging.
        """
        return self._info

    @property
    def current_temp(self):
        """
        Get current pool temperature, in celsius or farenheit according to spa settings
        """
        # update fresh info
        # self.refresh()
        if self._info["currentState"]["celsius"]:
            return round(
                (float(self._info["currentState"]["currentTemp"]) - 32) * 5 / 9, 1
            )
        return float(self._info["currentState"]["currentTemp"])

    @property
    def desired_temp(self):
        """
        Get desired pool temperature, in celsius or farenheit according to spa settings
        """
        # update fresh info
        # self.refresh()
        if self._info["currentState"]["celsius"]:
            return round(
                (float(self._info["currentState"]["desiredTemp"]) - 32) * 5 / 9, 1
            )
        return float(self._info["currentState"]["desiredTemp"])

    @desired_temp.setter
    def desired_temp(self, temperature):
        """
        Set the desired temperature of the whirlpool
        :param temperature: temperature, in celsius if the whirlpool is set to celsius
        or in fahrenheit if the whirlpool is set to fahrenheit
        """
        # TODO: check high/low ranges and adjust range accordingly
        if self._info["currentState"]["celsius"]:
            # convert to fahrenheit since the API always expects fahrenheit
            temperature = round(temperature / 5 * 9 + 32, 1)
        self._post_json(
            "/spa-commands/temperature/value",
            {"value": temperature, "spaId": self._info["_id"], "via": "MOBILE"},
        )
        # update the local info
        self.refresh()

    @property
    def temp_range(self):
        """
        Get temp range HIGH (True) or LOW (False)
        """
        # update fresh info
        # self.refresh()
        return self._info["currentState"]["tempRange"] == "HIGH"

    @temp_range.setter
    def temp_range(self, temp_range=True):
        """
        Set temp range HIGH or LOW
        :param temp_range: True for HIGH, False for LOW
        """
        self._post_json(
            "/spa-commands/temperature/range",
            {
                "range": ("HIGH" if temp_range else "LOW"),
                "spaId": self._info["_id"],
                "via": "MOBILE",
            },
        )
        # update the local info
        self.refresh()

    @property
    def heater_mode(self):
        """
        Get heater mode of spa READY (True) or REST (False)
        """
        # update fresh info
        # self.refresh()
        return self._info["currentState"]["heaterMode"] == "READY"

    @heater_mode.setter
    def heater_mode(self, heater_mode=True):
        """
        Set heater mode READY or REST
        :param heater_mode: True for READY, False for REST
        """
        self._post_json(
            "/spa-commands/temperature/heater-mode",
            {
                "mode": ("READY" if heater_mode else "REST"),
                "spaId": self._info["_id"],
                "via": "MOBILE",
            },
        )
        # update the local info
        self.refresh()

    @property
    def panel_lock(self):
        """
        Get panel lock status, Locked = True, unlocked = False
        """
        # update fresh info
        # self.refresh()
        return self._info["currentState"]["panelLock"]

    @panel_lock.setter
    def panel_lock(self, lock=True):
        """
        Set panel lock
        :param lock: True for locked, False for unlocked
        """
        self._post_json(
            "/spa-commands/panel/state",
            {
                "state": ("LOCK_PANEL" if lock else "UNLOCK_PANEL"),
                "spaId": self._info["_id"],
                "via": "MOBILE",
            },
        )
        # update the local info
        self.refresh()

    def get_jet(self, jet_number=0):
        """
        get jet state HIGH = True, OFF = False
        :param jet_number: My pool has jets 0, 1 and 2
        """
        # update fresh info
        # self.refresh()
        return next(
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "PUMP" and x["port"] == str(jet_number)
        )

    def set_jet(self, jet_number=0, state=False):
        """
        Enable/disable jet
        :param jet_number: My pool has jets 0, 1 and 2
        :param state: False to furn off, True to turn on
        """
        self._post_json(
            "/spa-command/component-state",
            {
                "state": ("HIGH" if state else "OFF"),
                "deviceNumber": jet_number,
                "componentType": "jet",
                "spaId": self._info["_id"],
                "via": "MOBILE",
            },
        )
        # update the local info
        self.refresh()

    @property
    def jets(self):
        """
        get an array of jets True/False (ON/OFF) status
        """
        return [
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "PUMP"
        ]

    @jets.setter
    def jets(self, array):
        """
        set jets ON/OFF based on array of True/False
        :param array: array of True/False
        """
        for i, state in enumerate(array):
            self.set_jet(i, state)

    @property
    def circulation_pumps(self):
        """
        get an array of circulation pumps True/False (ON/OFF) status
        (just information, cannot be set)
        """
        return [
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "CIRCULATION_PUMP"
        ]

    @property
    def ozone_generators(self):
        """
        get an array of ozone generators True/False (ON/OFF) status
        (just information, cannot be set)
        """
        return [
            x["value"] == "ON"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "OZONE"
        ]

    def get_blower(self, blower_number=0):
        """
        get blower state HIGH = True, OFF = False
        :param blower_number: My pool has no blowers
        """
        # update fresh info
        # self.refresh()
        return next(
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "BLOWER" and x["port"] == str(blower_number)
        )

    def set_blower(self, blower_number=0, state=False):
        """
        Enable/disable blower. Untested as I don't have blowers.
        :param blower_number: blower number starting at 0
        :param state: False to furn off, True to turn on
        """
        self._post_json(
            "/spa-command/component-state",
            {
                "state": ("HIGH" if state else "OFF"),
                "deviceNumber": blower_number,
                "componentType": "blower",
                "spaId": self._info["_id"],
                "via": "MOBILE",
            },
        )
        # update the local info
        self.refresh()

    @property
    def blowers(self):
        """
        get an array of blowers True/False (ON/OFF) status
        """
        return [
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "BLOWER"
        ]

    @blowers.setter
    def blowers(self, array):
        """
        set blowers ON/OFF based on array of True/False
        :param array: array of True/False
        """
        for i, state in enumerate(array):
            self.set_blower(i, state)

    def get_light(self, light_number=0):
        """
        get light state HIGH = True, OFF = False
        :param light_number: My pool has light 0
        """
        # update fresh info
        # self.refresh()
        return next(
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "LIGHT" and x["port"] == str(light_number)
        )

    def set_light(self, light_number=0, state=False):
        """
        Enable/disable light
        :param jet_number: My pool has lights 0, 1 and 2
        :param state: False to furn off, True to turn on
        """
        self._post_json(
            "/spa-command/component-state",
            {
                "state": ("HIGH" if state else "OFF"),
                "deviceNumber": light_number,
                "componentType": "light",
                "spaId": self._info["_id"],
                "via": "MOBILE",
            },
        )
        # update the local info
        self.refresh()

    @property
    def lights(self):
        """
        get an array of lights True/False (ON/OFF) status
        """
        return [
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "LIGHT"
        ]

    @lights.setter
    def lights(self, array):
        """
        set lights ON/OFF based on array of True/False
        :param array: array of True/False
        """
        for i, state in enumerate(array):
            self.set_light(i, state)

    def get_serial(self):
        """
        Get spa serial number
        """
        return self._info["serialNumber"]

    @property
    def online(self):
        """
        Get the spa online status
        """
        return self._info["currentState"]["online"]
