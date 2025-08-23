import unittest
import base64

from controlmyspa import ControlMySpa
import responses


class ControlMySpaTestCase(unittest.TestCase):
    exampleusername = "example@example.com"
    examplepassword = "password123"

    def setUp(self):
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.idm = {
            "_links": {
                "refreshEndpoint": {
                    "href": "https://iamqacontrolmyspa.b2clogin.com/iamqacontrolmyspa.onmicrosoft.com/oauth2/v2.0/token?p=B2C_1_CMS_USER_PWD"
                },
                "tokenEndpoint": {"href": "https://iot.controlmyspa.com/auth/login"},
                "whoami": {},
            },
            "mobileClientId": "abcd1234",
            "mobileClientSecret": "abcd1234",
        }

        self.responses.add(
            responses.GET,
            "https://iot.controlmyspa.com/idm/tokenEndpoint",
            status=200,
            json=self.idm,
        )
        self.iam = {
            "data": {
                "accessToken": "12345678-9abc-def0-1234-56789abcdef0",
                "refreshToken": "12345678-9abc-def0-1234-56789abcdef0",
            },
            "message": "Log in successful.",
            "statusCode": 200,
        }

        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/auth/login",
            status=200,
            json=self.iam,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    {
                        "grant_type": "password",
                        "password": self.examplepassword,
                        "scope": "openid user_name",
                        "email": self.exampleusername,
                    }
                )
            ],
        )
        self.list = {
            "data": {
                "page": {"number": 0, "size": 20, "totalElements": 1, "totalPages": 0},
                "spas": [
                    {
                        "_class": "com.tritonsvc.messageprocessor.model.Spa",
                        "_id": "abcd1234",
                        "alerts": [
                            {
                                "__v": 0,
                                "_id": "abcd1234",
                                "celcius": True,
                                "code": 16,
                                "controllerType": "NGSC",
                                "createdAt": "2025-08-06T18:12:07.490Z",
                                "dealerId": "abcd1234",
                                "faultLogReceivedTimestamp": "2025-05-06T22:16:00.000Z",
                                "number": 23,
                                "oemId": "abcd1234",
                                "ownerId": "abcd1234",
                                "sensorATemp": 72,
                                "sensorBTemp": 78,
                                "severity": "ERROR",
                                "spaId": "abcd1234",
                                "targetTemp": 73,
                                "timestamp": "2025-05-06T22:16:00.000Z",
                                "updatedAt": "2025-08-06T18:12:07.490Z",
                            }
                        ],
                        "brokerId": None,
                        "buildNumber": "1130/130",
                        "c8zCurrentState": {
                            "c8zHeaterState": "OFF",
                            "c8zStatus": "C8Z_STATUS_NOT_PRESENT",
                        },
                        "currentState": {
                            "ABDisplay": False,
                            "accessLocked": False,
                            "alertState": "ERROR",
                            "allSegsOn": False,
                            "ambientTemp": 0,
                            "blowout": False,
                            "bluetoothStatus": "NOT_PRESENT",
                            "celsius": True,
                            "changeUV": False,
                            "cleanupCycle": False,
                            "components": [
                                {
                                    "alertState": None,
                                    "availableValues": [],
                                    "componentId": None,
                                    "componentType": "GATEWAY",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "GATEWAY",
                                    "port": None,
                                    "registeredTimestamp": "2025-08-23T13:19:58.550Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": None,
                                },
                                {
                                    "alertState": None,
                                    "availableValues": [],
                                    "componentId": None,
                                    "componentType": "CONTROLLER",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "CONTROLLER",
                                    "port": None,
                                    "registeredTimestamp": "2025-08-23T13:19:58.550Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": None,
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "ON", "DISABLED"],
                                    "componentId": None,
                                    "componentType": "FILTER",
                                    "durationMinutes": 120,
                                    "hour": 0,
                                    "materialType": None,
                                    "minute": 0,
                                    "name": "FILTER",
                                    "port": "0",
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "OFF",
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "ON", "DISABLED"],
                                    "componentId": None,
                                    "componentType": "FILTER",
                                    "durationMinutes": 120,
                                    "hour": 8,
                                    "materialType": None,
                                    "minute": 0,
                                    "name": "FILTER",
                                    "port": "1",
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "DISABLED",
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "ON"],
                                    "componentId": None,
                                    "componentType": "OZONE",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "OZONE",
                                    "port": None,
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "ON",
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "HIGH"],
                                    "componentId": None,
                                    "componentType": "PUMP",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "PUMP",
                                    "port": "0",
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "OFF",
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "HIGH"],
                                    "componentId": None,
                                    "componentType": "PUMP",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "PUMP",
                                    "port": "1",
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "OFF",
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "HIGH"],
                                    "componentId": None,
                                    "componentType": "PUMP",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "PUMP",
                                    "port": "2",
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "OFF",
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "HIGH"],
                                    "componentId": None,
                                    "componentType": "CIRCULATION_PUMP",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "CIRCULATION_PUMP",
                                    "port": None,
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "HIGH",
                                },
                                {
                                    "alertState": None,
                                    "availableValues": ["OFF", "HIGH"],
                                    "componentId": None,
                                    "componentType": "LIGHT",
                                    "durationMinutes": None,
                                    "hour": None,
                                    "materialType": None,
                                    "minute": None,
                                    "name": "LIGHT",
                                    "port": "0",
                                    "registeredTimestamp": "2025-08-23T13:19:58.551Z",
                                    "serialNumber": "abcd1234",
                                    "targetValue": None,
                                    "value": "OFF",
                                },
                            ],
                            "controllerType": "NGSC",
                            "currentTemp": "87.80",
                            "day": 0,
                            "demoMode": False,
                            "desiredTemp": "98.60",
                            "ecoMode": False,
                            "elapsedTimeDisplay": False,
                            "engineeringMode": False,
                            "errorCode": 0,
                            "ethernetPluggedIn": True,
                            "flowSwitchClosed": False,
                            "futureSentTimestamp": 0,
                            "heatExternallyDisabled": False,
                            "heaterCooling": False,
                            "heaterMode": "READY",
                            "hiLimitTemp": 0,
                            "hour": 16,
                            "invert": False,
                            "latchingMessage": False,
                            "lightCycle": False,
                            "maintenanceLocked": False,
                            "messageSeverity": 0,
                            "military": True,
                            "minute": 19,
                            "month": 0,
                            "offlineAlert": False,
                            "online": True,
                            "overrangeEnabled": False,
                            "panelLock": False,
                            "panelMode": "PANEL_MODE_NGSC",
                            "primaryTZLStatus": "TZL_NOT_PRESENT",
                            "primingMode": False,
                            "registrationLockout": False,
                            "reminderCode": None,
                            "reminderDaysClearRay": 0,
                            "reminderDaysFilter1": 0,
                            "reminderDaysFilter2": 0,
                            "reminderDaysWater": 0,
                            "repeat": False,
                            "rs485AcquiredAddress": 18,
                            "rs485ConnectionActive": True,
                            "runMode": "Ready",
                            "secondaryFiltrationMode": "AWAY",
                            "secondaryTZLStatus": "TZL_NOT_PRESENT",
                            "sentTimestamp": 0,
                            "settingsLock": False,
                            "setupParams": {
                                "drainModeEnabled": False,
                                "gfciEnabled": False,
                                "highRangeHigh": 104,
                                "highRangeLow": 80,
                                "lastUpdateTimestamp": "2025-08-23T13:20:01.792Z",
                                "lowRangeHigh": 99,
                                "lowRangeLow": 50,
                            },
                            "shouldShowAlert": False,
                            "soakMode": False,
                            "soundAlarm": False,
                            "spaOverheatDisabled": False,
                            "spaRunState": None,
                            "specialTimeouts": False,
                            "staleTimestamp": "2025-08-23T13:22:58.546Z",
                            "stirring": False,
                            "swimSpaMode": "SWIM_MODE_OTHER",
                            "swimSpaModeChanging": False,
                            "systemInfo": {
                                "controllerSoftwareVersion": "M100_226 " "V43.0",
                                "currentSetup": 7,
                                "dipSwitches": [
                                    {"on": False, "slotNumber": 1},
                                    {"on": False, "slotNumber": 2},
                                    {"on": False, "slotNumber": 3},
                                    {"on": True, "slotNumber": 4},
                                    {"on": False, "slotNumber": 5},
                                    {"on": False, "slotNumber": 6},
                                    {"on": False, "slotNumber": 7},
                                    {"on": False, "slotNumber": 8},
                                    {"on": False, "slotNumber": 9},
                                    {"on": False, "slotNumber": 10},
                                ],
                                "heaterPower": 3,
                                "heaterType": 0,
                                "lastUpdateTimestamp": "2025-08-23T13:20:07.307Z",
                                "mfrSSID": 100,
                                "minorVersion": 0,
                                "modelSSID": 226,
                                "packMajorVersion": 0,
                                "packMinorVersion": 0,
                                "serialNumber": 0,
                                "versionSSID": 43,
                            },
                            "targetDesiredTemp": "98.6",
                            "tempLock": False,
                            "tempRange": "LOW",
                            "temperatureReached": False,
                            "testMode": False,
                            "timeNotSet": False,
                            "tvLiftState": 0,
                            "uiCode": 0,
                            "uiSubCode": 0,
                            "updateIntervalSeconds": 0,
                            "uplinkTimestamp": "2025-08-23T13:19:58.546Z",
                            "waterLevel1": False,
                            "waterLevel2": False,
                            "wifiConnectionHealth": None,
                            "wifiUpdateIntervalSeconds": 0,
                            "year": 0,
                        },
                        "dealerId": {
                            "_class": "com.bwg.iot.model.Dealer",
                            "_id": "abcd1234",
                            "active": True,
                            "address": {
                                "_id": "abcd1234",
                                "address1": "Tehdaskatu 7",
                                "city": "SALO",
                                "country": "Finland",
                                "links": [],
                                "state": "Varsinais-Suomi",
                                "zip": "24100",
                            },
                            "cmsCode": "abcd1234",
                            "code": "abcd1234",
                            "email": "huolto@novitek.fi",
                            "links": [],
                            "logo": {
                                "_id": "5bc449b428381aee3670d907",
                                "fileId": "5bc449b428381aee3670d908",
                                "links": [],
                                "name": "novitek-logo-musta.png",
                            },
                            "logoUrl": "https://bwgcmsstorage.blob.core.windows.net/attachments/6fbcf27b-4435-4030-b48f-db2d112c13da.png",
                            "modifiedDate": "2024-06-05T19:07:14.637Z",
                            "name": "Novitek",
                            "oemId": "5a04e66f283885d17ed233f2",
                            "oemName": "Oy Nordic",
                            "phone": "+3582737270",
                            "updatedAt": "2024-06-05T19:07:14.637Z",
                        },
                        "dealerName": "Novitek",
                        "ipAddress": "",
                        "isDefault": True,
                        "lastAlertDate": "2025-04-13T19:19:21.840Z",
                        "manufacturedDate": "2021-09-07T14:27:06.851Z",
                        "model": "Default Spa",
                        "oemId": {
                            "_class": "com.bwg.iot.model.Oem",
                            "_id": "5a04e66f283885d17ed233f2",
                            "active": True,
                            "address": {
                                "_id": "5c90a2d02838c70773a4ef7d",
                                "address1": "Tehdaskatu 7",
                                "city": "Salo  ",
                                "country": "Finland",
                                "links": [],
                                "state": "--",
                                "zip": "FIN-24100",
                            },
                            "adminEmail": "jp.fager@novitek.fi",
                            "adminId": "5bc42e9028381aee3670d876",
                            "adminName": "Jukka-Pekka Fager",
                            "code": "PDS",
                            "createdDate": "2017-11-09T23:36:15.587Z",
                            "customerNumber": "12345678",
                            "email": "jp.fager@novitek.fi",
                            "links": [],
                            "logo": {
                                "_id": "5bc4327528381aee3670d87c",
                                "fileId": "5bc4327528381aee3670d87d",
                                "links": [],
                                "name": "novitek-logo-musta.png",
                            },
                            "logoUrl": "https://bwgcmsstorage.blob.core.windows.net/attachments/8a3b0c6d-1084-4ac7-bda2-cd7191ff82db.png",
                            "modifiedDate": "2024-06-05T19:07:00.995Z",
                            "name": "Oy Nordic Spa Ltd",
                            "phone": "+358-2-737270",
                            "updatedAt": "2024-06-05T19:07:00.996Z",
                        },
                        "oemName": "Oy Nordic Spa Ltd",
                        "ownerEmail": "example@example.com",
                        "ownerId": {
                            "_class": "com.bwg.iot.model.User",
                            "_id": "abcd1234",
                            "active": True,
                            "address": {
                                "_id": "abcd1234",
                                "address1": "example@example.com",
                                "address2": "",
                                "city": "Turku",
                                "country": "Finland",
                                "state": "Turku",
                                "zip": "",
                            },
                            "createdDate": "2023-01-23T15:48:16.278Z",
                            "dealerId": "abcd1234",
                            "dealerName": "Novitek",
                            "deviceToken": "abcd1234",
                            "deviceType": "IOS",
                            "email": "example@example.com",
                            "firstName": "first",
                            "fullName": "first last",
                            "lastLogin": "2025-08-23T13:20:17.970Z",
                            "lastName": "last",
                            "links": [],
                            "notes": "",
                            "oemId": "abcd1234",
                            "oemName": "Oy Nordic Spa Ltd",
                            "phone": "00123456789",
                            "roles": ["OWNER"],
                            "spaId": "abcd1234",
                            "timeZone": "Europe/Helsinki",
                            "updatedAt": "2025-08-23T13:20:17.970Z",
                        },
                        "ownerName": "first last",
                        "p2pAPPassword": "",
                        "p2pAPSSID": "abcd1234",
                        "productName": "Default Spa",
                        "regKey": "abcd1234",
                        "registrationDate": "2025-05-05T18:16:33.424Z",
                        "salesDate": "2021-09-07T14:27:18.117Z",
                        "serialNumber": "abcd1234",
                        "updatedAt": "2025-08-23T13:20:20.344Z",
                    }
                ],
            },
            "message": "Spas retrieved successfully.",
            "statusCode": 200,
        }

        self.responses.add(
            responses.GET,
            "https://iot.controlmyspa.com/spas",
            match=[
                responses.matchers.query_param_matcher(
                    {
                        "username": self.exampleusername,
                    }
                )
            ],
            status=200,
            json=self.list,
        )

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def test_init_config(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.assertEqual(cms._email, self.exampleusername)
        self.assertEqual(cms._password, self.examplepassword)
        # there should have been 4 API calls
        self.assertAlmostEqual(len(self.responses.calls), 3, delta=1)
        # test the basic auth of login
        self.assertLessEqual(
            {
                "Authorization": "Basic "
                + base64.b64encode(
                    (
                        self.idm["mobileClientId"]
                        + ":"
                        + self.idm["mobileClientSecret"]
                    ).encode("ascii")
                ).decode("ascii")
            }.items(),
            self.responses.calls[1].request.headers.items(),
        )
        # test token authentication of spas
        self.assertLessEqual(
            {"Authorization": "Bearer 12345678-9abc-def0-1234-56789abcdef0"}.items(),
            self.responses.calls[2].request.headers.items(),
        )
        self.assertDictEqual(cms._idm, self.idm)
        self.assertDictEqual(cms._iam, self.iam)
        self.assertDictEqual(cms._list, self.list)

    def test_current_temp_get(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.assertEqual(cms.current_temp, 31)

    def test_desired_temp_get(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.assertEqual(cms.desired_temp, 37)

    def test_current_temp_get_fahrenheit(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        cms._info["currentState"]["celsius"] = False
        self.assertEqual(cms.current_temp, 87.80)

    def test_desired_temp_get_fahrenheit(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        cms._info["currentState"]["celsius"] = False
        self.assertEqual(cms.desired_temp, 98.60)

    def test_desired_temp_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/temperature/value",
            match=[
                responses.matchers.json_params_matcher(
                    {"value": 96.8, "spaId": "abcd1234", "via": "MOBILE"}
                )
            ],
            json={},
        )
        cms.desired_temp = 36

    def test_desired_temp_set_fahrenheit(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        cms._info["currentState"]["celsius"] = False
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/temperature/value",
            match=[
                responses.matchers.json_params_matcher(
                    {"value": 96, "spaId": "abcd1234", "via": "MOBILE"}
                )
            ],
            json={},
        )
        cms.desired_temp = 96

    def test_temp_range(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # Default data in test set is "LOW"
        self.assertEqual(cms.temp_range, False)
        cms._info["currentState"]["tempRange"] = "HIGH"
        self.assertEqual(cms.temp_range, True)

    def test_temp_range_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/temperature/range",
            match=[
                responses.matchers.json_params_matcher(
                    {"range": "HIGH", "spaId": "abcd1234", "via": "MOBILE"}
                )
            ],
            json={},
        )
        cms.temp_range = True
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/temperature/range",
            match=[
                responses.matchers.json_params_matcher(
                    {"range": "LOW", "spaId": "abcd1234", "via": "MOBILE"}
                )
            ],
            json={},
        )
        cms.temp_range = False

    def test_panel_lock(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # Default data in test set is unlocked
        self.assertEqual(cms.panel_lock, False)
        cms._info["currentState"]["panelLock"] = True
        self.assertEqual(cms.panel_lock, True)

    def test_panel_lock_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/panel/state",
            match=[
                responses.matchers.json_params_matcher(
                    {"state": "LOCK_PANEL", "spaId": "abcd1234", "via": "MOBILE"}
                )
            ],
            json={},
        )
        cms.panel_lock = True
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/panel/state",
            match=[
                responses.matchers.json_params_matcher(
                    {"state": "UNLOCK_PANEL", "spaId": "abcd1234", "via": "MOBILE"}
                )
            ],
            json={},
        )
        cms.panel_lock = False

    def test_jets(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        #  default all jets are off
        self.assertEqual(cms.jets, [False, False, False])
        self.assertEqual(cms.get_jet(0), False)
        self.assertEqual(cms.get_jet(1), False)
        self.assertEqual(cms.get_jet(2), False)
        # manually enable all pumps/jets
        for component in cms._info["currentState"]["components"]:
            if component["componentType"] == "PUMP":
                component["value"] = "HIGH"
        self.assertEqual(cms.jets, [True, True, True])
        self.assertEqual(cms.get_jet(0), True)
        self.assertEqual(cms.get_jet(1), True)
        self.assertEqual(cms.get_jet(2), True)

    def test_jets_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-command/component-state",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "state": "HIGH",
                        "deviceNumber": 0,
                        "componentType": "jet",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.set_jet(0, True)
        cms.jets = [True]
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-command/component-state",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "state": "OFF",
                        "deviceNumber": 0,
                        "componentType": "jet",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.set_jet(0, False)
        cms.jets = [False]

    def test_jets_empty(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # test correct handling if there were no jets at all
        cms._info["currentState"]["components"] = [
            x
            for x in cms._info["currentState"]["components"]
            if x["componentType"] != "PUMP"
        ]
        self.assertEqual(cms.jets, [])

    def test_blower_empty(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        #  default all blowers are off
        self.assertEqual(cms.blowers, [])

    def test_blower(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # my test data contains no blower. creating a synthetic one to be able to test
        cms._info["currentState"]["components"].append(
            {
                "availableValues": ["OFF", "HIGH"],
                "componentType": "BLOWER",
                "materialType": "BLOWER",
                "name": "BLOWER",
                "port": "0",
                "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                "targetValue": "OFF",
                "value": "OFF",
            }
        )
        self.assertEqual(cms.blowers, [False])
        self.assertEqual(cms.get_blower(0), False)
        # manually enable
        for component in cms._info["currentState"]["components"]:
            if component["componentType"] == "BLOWER":
                component["value"] = "HIGH"
        self.assertEqual(cms.blowers, [True])
        self.assertEqual(cms.get_blower(0), True)

    def test_blowers_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-command/component-state",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "state": "HIGH",
                        "deviceNumber": 0,
                        "componentType": "blower",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.set_blower(0, True)
        cms.blowers = [True]

        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-command/component-state",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "state": "OFF",
                        "deviceNumber": 0,
                        "componentType": "blower",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.set_blower(0, False)
        cms.blower = [False]

    def test_lights(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        #  default all jets are off
        self.assertEqual(cms.lights, [False])
        self.assertEqual(cms.get_light(0), False)
        # manually enable all lights
        for component in cms._info["currentState"]["components"]:
            if component["componentType"] == "LIGHT":
                component["value"] = "HIGH"
        self.assertEqual(cms.lights, [True])
        self.assertEqual(cms.get_light(0), True)

    def test_lights_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-command/component-state",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "state": "HIGH",
                        "deviceNumber": 0,
                        "componentType": "light",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.set_light(0, True)
        cms.lights = [True]

        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-command/component-state",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "state": "OFF",
                        "deviceNumber": 0,
                        "componentType": "light",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.set_light(0, False)
        cms.lights = [False]

    def test_lights_empty(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # test correct handling if there were no jets at all
        cms._info["currentState"]["components"] = [
            x
            for x in cms._info["currentState"]["components"]
            if x["componentType"] != "LIGHT"
        ]
        self.assertEqual(cms.lights, [])

    def test_serialnumber(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.assertEqual(cms.get_serial(), self.list["data"]["spas"][0]["serialNumber"])

    def test_heater_mode(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        #  default heater mode READY
        self.assertEqual(cms.heater_mode, True)
        # set heater mode REST
        cms._info["currentState"]["heaterMode"] = "REST"
        self.assertEqual(cms.heater_mode, False)

    def test_heater_mode_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/temperature/heater-mode",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "mode": "READY",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.heater_mode = True

        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/spa-commands/temperature/heater-mode",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "mode": "REST",
                        "spaId": "abcd1234",
                        "via": "MOBILE",
                    }
                )
            ],
            json={},
        )
        cms.heater_mode = False

    def test_circulation_pumps(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        #  default all circulation pumps are on
        self.assertEqual(cms.circulation_pumps, [True])

        # manually enable all lights
        for component in cms._info["currentState"]["components"]:
            if component["componentType"] == "CIRCULATION_PUMP":
                component["value"] = "OFF"
        self.assertEqual(cms.circulation_pumps, [False])

    def test_circulation_pumps_empty(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # test correct handling if there were no jets at all
        cms._info["currentState"]["components"] = [
            x
            for x in cms._info["currentState"]["components"]
            if x["componentType"] != "CIRCULATION_PUMP"
        ]
        self.assertEqual(cms.circulation_pumps, [])

    def test_ozone_generators(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        #  default all circulation pumps are on
        self.assertEqual(cms.ozone_generators, [True])

        # manually enable all lights
        for component in cms._info["currentState"]["components"]:
            if component["componentType"] == "OZONE":
                component["value"] = "OFF"
        self.assertEqual(cms.ozone_generators, [False])

    def test_ozone_generators_empty(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # test correct handling if there were no jets at all
        cms._info["currentState"]["components"] = [
            x
            for x in cms._info["currentState"]["components"]
            if x["componentType"] != "OZONE"
        ]
        self.assertEqual(cms.ozone_generators, [])

    def test_online(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # in the example dataset the spa is online
        self.assertEqual(cms.online, True)


if __name__ == "__main__":
    unittest.main()
