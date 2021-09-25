"""
Python module to get metrics from and control Balboa ControlMySpa whirlpools
"""

import requests


class ControlMySpa:
    """
    Class representing Balboa ControlMySpa whirlpools
    """

    _email = None
    _password = None

    def __init__(self, email, password):
        """
        Initialize connection to Balboa ControlMySpa cloud API
        :param email: email address used to log in
        :param password: password used to log in
        """
        self._email = email
        self._password = password

        # log in and fetch pool info
        self._get_idm()
        self._do_login()
        self._get_whoami()
        self._get_info()

    def _get_idm(self):
        """
        Get URL and basic auth to log in to IDM
        """
        response = requests.get("https://iot.controlmyspa.com/idm/tokenEndpoint")
        response.raise_for_status()
        self._idm = response.json()
        return self._idm

    def _do_login(self):
        """
        Log in and get API access tokens
        """
        response = requests.post(
            self._idm["_links"]["tokenEndpoint"]["href"],
            data={
                "grant_type": "password",
                "password": self._password,
                "scope": "openid user_name",
                "username": self._email,
            },
            auth=(self._idm["mobileClientId"], self._idm["mobileClientSecret"]),
        )
        response.raise_for_status()
        self._token = response.json()
        return self._token

    def _get_whoami(self):
        """
        Get information about the logged in user, the owner
        """
        response = requests.get(
            self._idm["_links"]["whoami"]["href"],
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        self._user = response.json()
        return self._user

    def _get_info(self):
        """
        Get all the details for the whirlpool of the logged in user
        """
        response = requests.get(
            "https://iot.controlmyspa.com/mobile/spas/search/findByUsername",
            params={"username": self._email},
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        self._info = response.json()
        return self._info

    @property
    def current_temp(self):
        """
        Get current pool temperature
        """
        # update fresh info
        # self._get_info()
        if self._info["currentState"]["celsius"]:
            return round(
                (float(self._info["currentState"]["currentTemp"]) - 32) * 5 / 9, 1
            )
        return float(self._info["currentState"]["currentTemp"])

    @property
    def desired_temp(self):
        """
        Get desired pool temperature
        """
        # update fresh info
        # self._get_info()
        if self._info["currentState"]["celsius"]:
            return round(
                (float(self._info["currentState"]["desiredTemp"]) - 32) * 5 / 9, 1
            )
        return float(self._info["currentState"]["desiredTemp"])

    @desired_temp.setter
    def desired_temp(self, temperature):
        """
        Set the desired temperature of the whirlpool
        :param temperature: temperature, in celsius if the whirlpool is set to celsius or
                        in fahrenheit if the whirlpool is set to fahrenheit
        """
        if self._info["currentState"]["celsius"]:
            # convert to fahrenheit since the API always expects fahrenheit
            temperature = round(temperature / 5 * 9 + 32, 1)
        response = requests.post(
            "https://iot.controlmyspa.com/mobile/control/"
            + self._info["_id"]
            + "/setDesiredTemp",
            json={"desiredTemp": temperature},
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        # update the local info
        self._get_info()
        return response.json()

    @property
    def temp_range(self):
        """
        Get temp range HIGH (True) or LOW (False)
        """
        # update fresh info
        # self._get_info()
        return self._info["currentState"]["tempRange"] == "HIGH"

    @temp_range.setter
    def temp_range(self, temp_range=True):
        """
        Set temp range HIGH or LOW
        :param temp_range: True for HIGH, False for LOW
        """
        response = requests.post(
            "https://iot.controlmyspa.com/mobile/control/"
            + self._info["_id"]
            + "/setTempRange",
            json={"desiredState": ("HIGH" if temp_range else "LOW")},
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        # update the local info
        self._get_info()
        return response.json()

    @property
    def panel_lock(self):
        """
        Get panel lock status, Locked = True, unlocked = False
        """
        # update fresh info
        # self._get_info()
        return self._info["currentState"]["panelLock"]

    @panel_lock.setter
    def panel_lock(self, lock=True):
        """
        Set panel lock
        :param lock: True for locked, False for unlocked
        """
        response = requests.post(
            "https://iot.controlmyspa.com/mobile/control/"
            + self._info["_id"]
            + "/setPanel",
            json={"desiredState": ("LOCK_PANEL" if lock else "UNLOCK_PANEL")},
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        # update the local info
        self._get_info()
        return response.json()

    def get_jet(self, jet_number=0):
        """
        get jet state HIGH = True, OFF = False
        :param jet_number: My pool has jets 0, 1 and 2
        """
        # update fresh info
        # self._get_info()
        return [
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "PUMP" and x["port"] == str(jet_number)
        ][0]

    def set_jet(self, jet_number=0, state=False):
        """
        Enable/disable jet
        :param jet_number: My pool has jets 0, 1 and 2
        :param state: False to furn off, True to turn on
        """
        response = requests.post(
            "https://iot.controlmyspa.com/mobile/control/"
            + self._info["_id"]
            + "/setJetState",
            json={
                "desiredState": ("HIGH" if state else "OFF"),
                "deviceNumber": jet_number,
                "originatorId": "optional-Jet",
            },
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        # update the local info
        self._get_info()
        return response.json()

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

    def get_blower(self, blower_number=0):
        """
        get blower state HIGH = True, OFF = False
        :param blower_number: My pool has no blowers
        """
        # update fresh info
        # self._get_info()
        return [
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "BLOWER" and x["port"] == str(blower_number)
        ][0]

    def set_blower(self, blower_number=0, state=False):
        """
        Enable/disable jet
        :param jet_number: My pool has blowers 0, 1 and 2
        :param state: False to furn off, True to turn on
        """
        response = requests.post(
            "https://iot.controlmyspa.com/mobile/control/"
            + self._info["_id"]
            + "/setBlowerState",
            json={
                "desiredState": ("HIGH" if state else "OFF"),
                "deviceNumber": blower_number,
                "originatorId": "optional-Blower",
            },
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        # update the local info
        self._get_info()
        return response.json()

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
        # self._get_info()
        return [
            x["value"] == "HIGH"
            for x in self._info["currentState"]["components"]
            if x["componentType"] == "LIGHT" and x["port"] == str(light_number)
        ][0]

    def set_light(self, light_number=0, state=False):
        """
        Enable/disable light
        :param jet_number: My pool has lights 0, 1 and 2
        :param state: False to furn off, True to turn on
        """
        response = requests.post(
            "https://iot.controlmyspa.com/mobile/control/"
            + self._info["_id"]
            + "/setLightState",
            json={
                "desiredState": ("HIGH" if state else "OFF"),
                "deviceNumber": light_number,
                "originatorId": "optional-Light",
            },
            headers={"Authorization": "Bearer " + self._token["access_token"]},
        )
        response.raise_for_status()
        # update the local info
        self._get_info()
        return response.json()

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
