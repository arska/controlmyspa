import unittest
import base64

from controlmyspa import ControlMySpa
import responses


def suite():
    """Define all the tests of the module."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ControlMySpaTestCase))
    return suite


class ControlMySpaTestCase(unittest.TestCase):
    exampleusername = "example@example.com"
    examplepassword = "password123"

    def setUp(self):
        self.responses = responses.RequestsMock()
        self.responses.start()
        self.idm = {
            "_links": {
                "refreshEndpoint": {
                    "href": "https://idmqa.controlmyspa.com/oxauth/restv1/token"
                },
                "tokenEndpoint": {
                    "href": "https://idmqa.controlmyspa.com/oxauth/restv1/token"
                },
                "whoami": {"href": "https://iot.controlmyspa.com/mobile/auth/whoami"},
            },
            "mobileClientId": "@!1234.5678.9ABC.DEF0!1234!5678.9ABC!DEF0!1234.5678",
            "mobileClientSecret": "mobile",
        }
        self.responses.add(
            responses.GET,
            "https://iot.controlmyspa.com/idm/tokenEndpoint",
            status=200,
            json=self.idm,
        )
        self.token = {
            "access_token": "12345678-9abc-def0-1234-56789abcdef0",
            "expires_in": 14399,
            "id_token": "ewogICJraWQiOiAiMTIzNDU2NzgtOWFiYy1kZWYwLTEyMzQtNTY3ODlhYmNkZWYwIiwKICAidHlwIjogIkpXVCIsCiAgImFsZyI6ICJSUzI1NiIKfQ.ewogICJpc3MiOiAiaHR0cHM6Ly9pZG1xYS5jb250cm9sbXlzcGEuY29tIiwKICAiYXVkIjogIkAhMTIzNC41Njc4LjlBQkMuREVGMCExMjM0ITU2NzguOUFCQyFERUYwITEyMzQuNTY3OCIsCiAgImV4cCI6IDE2MzE3MjI5MjQsCiAgImlhdCI6IDE2MzE2MzY1MjQsCiAgIm94T3BlbklEQ29ubmVjdFZlcnNpb24iOiAib3BlbmlkY29ubmVjdC0xLjAiLAogICJzdWIiOiAiQCExMjM0LjU2NzguOUFCQy5ERUYwITEyMzQhNTY3OC45QUJDIURFRjAhMTIzNC41Njc4Igp9.yaWUF4vghbDRqS7ceFK55NPbOQvQIO_F-FIZmQkdCO2XQKtRq_X2nNmqYVEf35YlAsB09AD7P-NSPD_NPPwJeD1v0EECWZdI7qGzaegX34eM7aJU0j3LHHKT28n68AZ9NsfOuoQDLUmHUtXLkPb3522iHqqWclfZLqMX_Ug5vWej9IujFsHPLct8_a4OR7Xt07yPriKPC__qjSl_qFVFeJwoC2bNSh8kUja1p7G7e_cqUTEydK7ZVQxkpqG_HLOBjY3IoJBkRal2Rsh8PtgUhE0SJJJlLuYUWAW2DpU6ceFTA1ocGjv1c7ShDoD2zCedgynKIvogkpbdnoBzkECyOA",
            "refresh_token": "12345678-9abc-def0-1234-56789abcdef0",
            "scope": "openid user_name",
            "token_type": "bearer",
        }
        self.responses.add(
            responses.POST,
            "https://idmqa.controlmyspa.com/oxauth/restv1/token",
            status=200,
            json=self.token,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    {
                        "grant_type": "password",
                        "password": self.examplepassword,
                        "scope": "openid user_name",
                        "username": self.exampleusername,
                    }
                )
            ],
        )
        self.user = {
            "_id": "0123456789abcdef01234567",
            "_links": {
                "logo": {
                    "href": "https://iot.controlmyspa.com/mobile/attachments/0123456789abcdef01234567"
                },
                "self": {
                    "href": "https://iot.controlmyspa.com/mobile/users/0123456789abcdef01234567"
                },
                "spa": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567{?projection}",
                    "templated": True,
                },
                "user": {
                    "href": "https://iot.controlmyspa.com/mobile/users/0123456789abcdef01234567"
                },
            },
            "active": True,
            "address": {
                "address1": "Streetaddress 123",
                "city": "City ",
                "country": "Country",
                "zip": "12345",
            },
            "dealerId": "0123456789abcdef01234567",
            "dealerName": "MySpaDealer",
            "deviceToken": "0123456789abcdef01234567",
            "deviceType": "IOS",
            "email": self.exampleusername,
            "firstName": "Firstname",
            "fullName": "Firstname Lastname",
            "lastName": "Lastname",
            "oemId": "0123456789abcdef01234567",
            "oemName": "The Spa Producing Company Ltd",
            "password": self.examplepassword,
            "phone": "00123456789",
            "roles": ["OWNER"],
            "spaId": "0123456789abcdef01234567",
            "username": self.exampleusername,
        }
        self.responses.add(
            responses.GET,
            "https://iot.controlmyspa.com/mobile/auth/whoami",
            status=200,
            json=self.user,
        )
        self.info = {
            "_id": "0123456789abcdef01234567",
            "_links": {
                "AC Current measurements": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567/measurements?measurementType=AC_CURRENT"
                },
                "Ambient Temp measurements": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567/measurements?measurementType=AMBIENT_TEMP"
                },
                "events": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567/events"
                },
                "faultLogs": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567/faultLogs"
                },
                "owner": {
                    "href": "https://iot.controlmyspa.com/mobile/users/0123456789abcdef01234567"
                },
                "recipes": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567/recipes"
                },
                "self": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567"
                },
                "spa": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567{?projection}",
                    "templated": True,
                },
                "spaTemplate": {
                    "href": "https://iot.controlmyspa.com/mobile/spaTemplates/0123456789abcdef01234567"
                },
                "turnOffSpa": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567/recipes/0123456789abcdef01234567/run"
                },
                "wifiStats": {
                    "href": "https://iot.controlmyspa.com/mobile/spas/0123456789abcdef01234567/wifiStats"
                },
            },
            "buildNumber": "1101/101",
            "currentState": {
                "abdisplay": False,
                "allSegsOn": False,
                "bluetoothStatus": "NOT_PRESENT",
                "celsius": True,
                "cleanupCycle": False,
                "components": [
                    {
                        "componentType": "HEATER",
                        "materialType": "HEATER",
                        "name": "HEATER",
                        "port": "0",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "value": "OFF",
                    },
                    {
                        "availableValues": ["OFF", "ON", "DISABLED"],
                        "componentType": "FILTER",
                        "durationMinutes": 120,
                        "hour": 20,
                        "materialType": "FILTER",
                        "name": "FILTER",
                        "port": "0",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "value": "ON",
                    },
                    {
                        "availableValues": ["OFF", "ON", "DISABLED"],
                        "componentType": "FILTER",
                        "durationMinutes": 120,
                        "hour": 8,
                        "materialType": "FILTER",
                        "name": "FILTER",
                        "port": "1",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "value": "OFF",
                    },
                    {
                        "availableValues": ["OFF", "ON"],
                        "componentType": "OZONE",
                        "materialType": "OZONE",
                        "name": "OZONE",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "value": "ON",
                    },
                    {
                        "availableValues": ["OFF", "HIGH"],
                        "componentType": "PUMP",
                        "materialType": "PUMP",
                        "name": "PUMP",
                        "port": "0",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "targetValue": "OFF",
                        "value": "OFF",
                    },
                    {
                        "availableValues": ["OFF", "HIGH"],
                        "componentType": "PUMP",
                        "materialType": "PUMP",
                        "name": "PUMP",
                        "port": "1",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "targetValue": "OFF",
                        "value": "OFF",
                    },
                    {
                        "availableValues": ["OFF", "HIGH"],
                        "componentType": "PUMP",
                        "materialType": "PUMP",
                        "name": "PUMP",
                        "port": "2",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "targetValue": "OFF",
                        "value": "OFF",
                    },
                    {
                        "availableValues": ["OFF", "HIGH"],
                        "componentType": "CIRCULATION_PUMP",
                        "materialType": "CIRCULATION_PUMP",
                        "name": "CIRCULATION_PUMP",
                        "registeredTimestamp": "2021-09-14T17:35:17.430+0000",
                        "value": "HIGH",
                    },
                    {
                        "availableValues": ["OFF", "HIGH"],
                        "componentType": "LIGHT",
                        "materialType": "LIGHT",
                        "name": "LIGHT",
                        "port": "0",
                        "registeredTimestamp": "2021-09-14T17:35:17.446+0000",
                        "targetValue": "HIGH",
                        "value": "OFF",
                    },
                    {
                        "_links": {
                            "component": {
                                "href": "https://iot.controlmyspa.com/mobile/components/0123456789abcdef01234567"
                            }
                        },
                        "componentId": "0123456789abcdef01234567",
                        "componentType": "GATEWAY",
                        "materialType": "GATEWAY",
                        "name": "ControlMySpa Gateway",
                        "registeredTimestamp": "2021-09-14T17:35:17.446+0000",
                        "serialNumber": "12345***1234567890",
                    },
                    {
                        "componentType": "CONTROLLER",
                        "materialType": "CONTROLLER",
                        "name": "CONTROLLER",
                        "registeredTimestamp": "2021-09-14T17:35:17.446+0000",
                    },
                ],
                "controllerType": "NGSC",
                "currentTemp": "100.4",
                "demoMode": False,
                "desiredTemp": "99.5",
                "ecoMode": False,
                "elapsedTimeDisplay": False,
                "errorCode": 0,
                "ethernetPluggedIn": True,
                "heatExternallyDisabled": False,
                "heaterCooling": False,
                "heaterMode": "READY",
                "hour": 20,
                "invert": False,
                "latchingMessage": False,
                "lightCycle": False,
                "messageSeverity": 0,
                "military": True,
                "minute": 35,
                "offlineAlert": False,
                "online": True,
                "overrangeEnabled": False,
                "panelLock": False,
                "panelMode": "PANEL_MODE_NGSC",
                "primaryTZLStatus": "TZL_NOT_PRESENT",
                "primingMode": False,
                "repeat": False,
                "rs485AcquiredAddress": 16,
                "rs485ConnectionActive": True,
                "runMode": "Ready",
                "secondaryFiltrationMode": "AWAY",
                "secondaryTZLStatus": "TZL_NOT_PRESENT",
                "settingsLock": False,
                "setupParams": {
                    "drainModeEnabled": False,
                    "gfciEnabled": False,
                    "highRangeHigh": 104,
                    "highRangeLow": 80,
                    "lastUpdateTimestamp": "1970-01-01T00:00:03.436+0000",
                    "lowRangeHigh": 99,
                    "lowRangeLow": 50,
                },
                "shouldShowAlert": False,
                "soakMode": False,
                "soundAlarm": False,
                "spaOverheatDisabled": False,
                "specialTimeouts": False,
                "staleTimestamp": "2021-09-14T17:37:02.430+0000",
                "stirring": False,
                "swimSpaMode": "SWIM_MODE_OTHER",
                "swimSpaModeChanging": False,
                "systemInfo": {
                    "controllerSoftwareVersion": "M100_226 V43.0",
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
                    "lastUpdateTimestamp": "1970-01-01T00:00:06.449+0000",
                    "mfrSSID": 100,
                    "modelSSID": 226,
                    "swSignature": -148899849,
                    "versionSSID": 43,
                },
                "targetDesiredTemp": "96.8",
                "tempLock": False,
                "tempRange": "HIGH",
                "testMode": False,
                "timeNotSet": False,
                "tvLiftState": 0,
                "uiCode": 0,
                "uiSubCode": 0,
                "updateIntervalSeconds": 0,
                "uplinkTimestamp": "2021-09-14T17:35:17.430+0000",
                "wifiUpdateIntervalSeconds": 0,
            },
            "dealerId": "0123456789abcdef01234567",
            "dealerName": "MySpaDealer",
            "demo": False,
            "manufacturedDate": "2021-09-07T14:27:06.851+0000",
            "model": "Default Spa",
            "oemId": "0123456789abcdef01234567",
            "oemName": "The Spa Producing Company Ltd",
            "online": True,
            "owner": {
                "_id": "0123456789abcdef01234567",
                "_links": {
                    "address": {
                        "href": "https://iot.controlmyspa.com/mobile/addresses/0123456789abcdef01234567"
                    },
                    "self": {
                        "href": "https://iot.controlmyspa.com/mobile/users/0123456789abcdef01234567"
                    },
                },
                "active": True,
                "address": {
                    "address1": "Streetaddress 123",
                    "city": "City ",
                    "country": "Country",
                    "zip": "12345",
                },
                "dealerId": "0123456789abcdef01234567",
                "dealerName": "MySpaDealer",
                "deviceToken": "0123456789abcdef01234567",
                "deviceType": "IOS",
                "email": self.exampleusername,
                "firstName": "Firstname",
                "fullName": "Firstname Lastname",
                "lastName": "Lastname",
                "oemId": "0123456789abcdef01234567",
                "oemName": "The Spa Producing Company Ltd",
                "password": self.examplepassword,
                "phone": "00123456789",
                "roles": ["OWNER"],
                "spaId": "0123456789abcdef01234567",
                "username": self.exampleusername,
            },
            "p2pAPSSID": "CMS_SPA_12345***1234567890",
            "productName": "Default Spa",
            "registrationDate": "2021-09-06T13:13:29.705+0000",
            "salesDate": "2021-09-07T14:27:18.117+0000",
            "serialNumber": "12345***1234567890",
            "sold": "true",
            "templateId": "0123456789abcdef01234567",
            "transactionCode": "A1B2C3D4",
        }
        self.responses.add(
            responses.GET,
            "https://iot.controlmyspa.com/mobile/spas/search/findByUsername?username="
            + self.exampleusername,
            status=200,
            json=self.info,
        )

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def test_init_config(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.assertEqual(cms._email, self.exampleusername)
        self.assertEqual(cms._password, self.examplepassword)
        # there should have been 4 API calls
        self.assertAlmostEqual(len(self.responses.calls), 4, delta=1)
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
            self.responses.calls[2].request.headers.items(),
        )
        # test token authentication of whoami
        self.assertLessEqual(
            {"Authorization": "Bearer 12345678-9abc-def0-1234-56789abcdef0"}.items(),
            self.responses.calls[3].request.headers.items(),
        )
        # test token authentication of search
        self.assertLessEqual(
            {"Authorization": "Bearer 12345678-9abc-def0-1234-56789abcdef0"}.items(),
            self.responses.calls[4].request.headers.items(),
        )
        self.assertDictEqual(cms._idm, self.idm)
        self.assertDictEqual(cms._token, self.token)
        self.assertDictEqual(cms._user, self.user)
        self.assertDictEqual(cms._info, self.info)

    def test_current_temp_get(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.assertEqual(cms.current_temp, 38)

    def test_desired_temp_get(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.assertEqual(cms.desired_temp, 37.5)

    def test_current_temp_get_fahrenheit(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        cms._info["currentState"]["celsius"] = False
        self.assertEqual(cms.current_temp, 100.4)

    def test_desired_temp_get_fahrenheit(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        cms._info["currentState"]["celsius"] = False
        self.assertEqual(cms.desired_temp, 99.5)

    def test_desired_temp_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setDesiredTemp",
            match=[responses.matchers.json_params_matcher({"desiredTemp": 96.8})],
            json={},
        )
        cms.desired_temp = 36

    def test_desired_temp_set_fahrenheit(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        cms._info["currentState"]["celsius"] = False
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setDesiredTemp",
            match=[responses.matchers.json_params_matcher({"desiredTemp": 96})],
            json={},
        )
        cms.desired_temp = 96

    def test_temp_range(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        # Default data in test set is "HIGH"
        self.assertEqual(cms.temp_range, True)
        cms._info["currentState"]["tempRange"] = "LOW"
        self.assertEqual(cms.temp_range, False)

    def test_temp_range_set(self):
        cms = ControlMySpa(self.exampleusername, self.examplepassword)
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setTempRange",
            match=[responses.matchers.json_params_matcher({"desiredState": "HIGH"})],
            json={},
        )
        cms.temp_range = True
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setTempRange",
            match=[responses.matchers.json_params_matcher({"desiredState": "LOW"})],
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
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setPanel",
            match=[
                responses.matchers.json_params_matcher({"desiredState": "LOCK_PANEL"})
            ],
            json={},
        )
        cms.panel_lock = True
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setPanel",
            match=[
                responses.matchers.json_params_matcher({"desiredState": "UNLOCK_PANEL"})
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
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setJetState",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "desiredState": "HIGH",
                        "deviceNumber": 0,
                        "originatorId": "optional-Jet",
                    }
                )
            ],
            json={},
        )
        cms.set_jet(0, True)
        cms.jets = [True]
        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setJetState",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "desiredState": "OFF",
                        "deviceNumber": 0,
                        "originatorId": "optional-Jet",
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
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setBlowerState",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "desiredState": "HIGH",
                        "deviceNumber": 0,
                        "originatorId": "optional-Blower",
                    }
                )
            ],
            json={},
        )
        cms.set_blower(0, True)
        cms.blowers = [True]

        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setBlowerState",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "desiredState": "OFF",
                        "deviceNumber": 0,
                        "originatorId": "optional-Blower",
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
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setLightState",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "desiredState": "HIGH",
                        "deviceNumber": 0,
                        "originatorId": "optional-Light",
                    }
                )
            ],
            json={},
        )
        cms.set_light(0, True)
        cms.lights = [True]

        self.responses.add(
            responses.POST,
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/setLightState",
            match=[
                responses.matchers.json_params_matcher(
                    {
                        "desiredState": "OFF",
                        "deviceNumber": 0,
                        "originatorId": "optional-Light",
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
        self.assertEqual(cms.get_serial(), self.info["serialNumber"])

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
            "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/toggleHeaterMode",
            match=[responses.matchers.json_params_matcher({"originatorId": ""})],
            json={},
        )
        # test READY -> READY (no-op)
        cms.heater_mode = True

        # test READY -> REST
        cms.heater_mode = False
        cms._info["currentState"]["heaterMode"] = "REST"

        # test REST -> REST (no-op)
        cms.heater_mode = False

        # test REST -> READY
        cms.heater_mode = True
        cms._info["currentState"]["heaterMode"] = "READY"

        #  check that toggle was called exactly 2 times and not for the no-ops
        self.assertTrue(
            self.responses.assert_call_count(
                "https://iot.controlmyspa.com/mobile/control/0123456789abcdef01234567/toggleHeaterMode",
                2,
            )
        )

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
