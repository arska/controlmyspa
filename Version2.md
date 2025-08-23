= New controlmyspa v4 App and API April 2025

On April 30, 2025, Balboa published the new version 4 of the mobile Android/IOS app and API. Some time in August 2025 they turned off the previous version of the API, which this library was using 2023-2025.

The authentication remained the same, but the API calls to get and set spa information was changed to support multiple spas for the same logged-in user.

From the API error messages and some [MITM](https://www.mitmproxy.org/) of the mobile application I was able to capture the new requests that my spa supports/exposes and reverse engineer the calls to update this library. Here are the GET and POST requests I was able to capture and use:

```
GET https://iot.controlmyspa.com/spas
{
    "_id": "abcd1234",
    "_class": "com.tritonsvc.messageprocessor.model.Spa",
    "serialNumber": "123456789",
    "productName": "Default Spa",
    "model": "Default Spa",
    "dealerId": {
        "_id": "5bc449b728381aee3670d90a",
        "_class": "com.bwg.iot.model.Dealer",
        "oemId": "5a04e66f283885d17ed233f2",
        "oemName": "Oy Nordic",
        "code": "12345",
        "cmsCode": "PDS-12345",
        "name": "Novitek",
        "address": {
            "_id": "6343c4c18c150fb26d673294",
            "address1": "Tehdaskatu 7",
            "city": "SALO",
            "state": "Varsinais-Suomi",
            "country": "Finland",
            "zip": "24100",
            "links": []
        },
        "email": "huolto@novitek.fi",
        "phone": "+3582737270",
        "logo": {
            "_id": "5bc449b428381aee3670d907",
            "fileId": "5bc449b428381aee3670d908",
            "name": "novitek-logo-musta.png",
            "links": []
        },
        "modifiedDate": "2024-06-05T19:07:14.637Z",
        "active": true,
        "links": [],
        "logoUrl": "https://bwgcmsstorage.blob.core.windows.net/attachments/6fbcf27b-4435-4030-b48f-db2d112c13da.png",
        "updatedAt": "2024-06-05T19:07:14.637Z"
    },
    "dealerName": "Novitek",
    "oemId": {
        "_id": "5a04e66f283885d17ed233f2",
        "_class": "com.bwg.iot.model.Oem",
        "name": "Oy Nordic Spa Ltd",
        "customerNumber": "12345678",
        "code": "PDS",
        "address": {
            "_id": "5c90a2d02838c70773a4ef7d",
            "address1": "Tehdaskatu 7",
            "city": "Salo  ",
            "state": "--",
            "country": "Finland",
            "zip": "FIN-24100",
            "links": []
        },
        "email": "jp.fager@novitek.fi",
        "phone": "+358-2-737270",
        "logo": {
            "_id": "5bc4327528381aee3670d87c",
            "fileId": "5bc4327528381aee3670d87d",
            "name": "novitek-logo-musta.png",
            "links": []
        },
        "createdDate": "2017-11-09T23:36:15.587Z",
        "modifiedDate": "2024-06-05T19:07:00.995Z",
        "active": true,
        "links": [],
        "adminEmail": "jp.fager@novitek.fi",
        "adminId": "5bc42e9028381aee3670d876",
        "adminName": "Jukka-Pekka Fager",
        "updatedAt": "2024-06-05T19:07:00.996Z",
        "logoUrl": "https://bwgcmsstorage.blob.core.windows.net/attachments/8a3b0c6d-1084-4ac7-bda2-cd7191ff82db.png"
    },
    "oemName": "Oy Nordic Spa Ltd",
    "currentState": {
        "runMode": "Ready",
        "desiredTemp": "80.60",
        "targetDesiredTemp": "98.6",
        "currentTemp": "88.70",
        "controllerType": "NGSC",
        "errorCode": 0,
        "shouldShowAlert": false,
        "cleanupCycle": false,
        "uplinkTimestamp": "2025-08-23T05:35:58.267Z",
        "staleTimestamp": "2025-08-23T05:38:58.267Z",
        "heaterMode": "READY",
        "hour": 8,
        "minute": 36,
        "online": false,
        "celsius": true,
        "demoMode": false,
        "timeNotSet": false,
        "settingsLock": false,
        "spaOverheatDisabled": false,
        "bluetoothStatus": "NOT_PRESENT",
        "updateIntervalSeconds": 0,
        "wifiUpdateIntervalSeconds": 0,
        "components": [
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "GATEWAY",
                "componentType": "GATEWAY",
                "value": null,
                "availableValues": [],
                "registeredTimestamp": "2025-08-23T05:35:58.271Z",
                "port": null,
                "hour": null,
                "minute": null,
                "durationMinutes": null
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "CONTROLLER",
                "componentType": "CONTROLLER",
                "value": null,
                "availableValues": [],
                "registeredTimestamp": "2025-08-23T05:35:58.271Z",
                "port": null,
                "hour": null,
                "minute": null,
                "durationMinutes": null
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "FILTER",
                "componentType": "FILTER",
                "value": "OFF",
                "availableValues": [
                    "OFF",
                    "ON",
                    "DISABLED"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": "0",
                "hour": 0,
                "minute": 0,
                "durationMinutes": 120
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "FILTER",
                "componentType": "FILTER",
                "value": "DISABLED",
                "availableValues": [
                    "OFF",
                    "ON",
                    "DISABLED"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": "1",
                "hour": 8,
                "minute": 0,
                "durationMinutes": 120
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "OZONE",
                "componentType": "OZONE",
                "value": "OFF",
                "availableValues": [
                    "OFF",
                    "ON"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": null,
                "hour": null,
                "minute": null,
                "durationMinutes": null
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "PUMP",
                "componentType": "PUMP",
                "value": "OFF",
                "availableValues": [
                    "OFF",
                    "HIGH"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": "0",
                "hour": null,
                "minute": null,
                "durationMinutes": null
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "PUMP",
                "componentType": "PUMP",
                "value": "OFF",
                "availableValues": [
                    "OFF",
                    "HIGH"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": "1",
                "hour": null,
                "minute": null,
                "durationMinutes": null
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "PUMP",
                "componentType": "PUMP",
                "value": "OFF",
                "availableValues": [
                    "OFF",
                    "HIGH"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": "2",
                "hour": null,
                "minute": null,
                "durationMinutes": null
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "CIRCULATION_PUMP",
                "componentType": "CIRCULATION_PUMP",
                "value": "OFF",
                "availableValues": [
                    "OFF",
                    "HIGH"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": null,
                "hour": null,
                "minute": null,
                "durationMinutes": null
            },
            {
                "componentId": null,
                "serialNumber": "123456789",
                "alertState": null,
                "materialType": null,
                "targetValue": null,
                "name": "LIGHT",
                "componentType": "LIGHT",
                "value": "OFF",
                "availableValues": [
                    "OFF",
                    "HIGH"
                ],
                "registeredTimestamp": "2025-08-23T05:35:58.272Z",
                "port": "0",
                "hour": null,
                "minute": null,
                "durationMinutes": null
            }
        ],
        "setupParams": {
            "lowRangeLow": 50,
            "lowRangeHigh": 99,
            "highRangeLow": 80,
            "highRangeHigh": 104,
            "gfciEnabled": false,
            "drainModeEnabled": false,
            "lastUpdateTimestamp": "2025-08-23T05:36:02.839Z"
        },
        "systemInfo": {
            "serialNumber": 0,
            "packMinorVersion": 0,
            "packMajorVersion": 0,
            "heaterType": 0,
            "minorVersion": 0,
            "versionSSID": 43,
            "modelSSID": 226,
            "mfrSSID": 100,
            "heaterPower": 3,
            "dipSwitches": [
                {
                    "slotNumber": 1,
                    "on": false
                },
                {
                    "slotNumber": 2,
                    "on": false
                },
                {
                    "slotNumber": 3,
                    "on": false
                },
                {
                    "slotNumber": 4,
                    "on": true
                },
                {
                    "slotNumber": 5,
                    "on": false
                },
                {
                    "slotNumber": 6,
                    "on": false
                },
                {
                    "slotNumber": 7,
                    "on": false
                },
                {
                    "slotNumber": 8,
                    "on": false
                },
                {
                    "slotNumber": 9,
                    "on": false
                },
                {
                    "slotNumber": 10,
                    "on": false
                }
            ],
            "currentSetup": 7,
            "controllerSoftwareVersion": "M100_226 V43.0",
            "lastUpdateTimestamp": "2025-08-23T05:36:04.353Z"
        },
        "ethernetPluggedIn": true,
        "rs485ConnectionActive": true,
        "rs485AcquiredAddress": 18,
        "sentTimestamp": 0,
        "futureSentTimestamp": 0,
        "messageSeverity": 0,
        "uiCode": 0,
        "uiSubCode": 0,
        "invert": false,
        "allSegsOn": false,
        "panelLock": false,
        "military": true,
        "tempRange": "LOW",
        "primingMode": false,
        "soundAlarm": false,
        "repeat": false,
        "panelMode": "PANEL_MODE_NGSC",
        "swimSpaMode": "SWIM_MODE_OTHER",
        "swimSpaModeChanging": false,
        "heaterCooling": false,
        "latchingMessage": false,
        "lightCycle": false,
        "elapsedTimeDisplay": false,
        "tvLiftState": 0,
        "specialTimeouts": false,
        "ABDisplay": false,
        "stirring": false,
        "ecoMode": false,
        "soakMode": false,
        "overrangeEnabled": false,
        "heatExternallyDisabled": false,
        "testMode": false,
        "tempLock": false,
        "primaryTZLStatus": "TZL_NOT_PRESENT",
        "secondaryTZLStatus": "TZL_NOT_PRESENT",
        "secondaryFiltrationMode": "AWAY",
        "offlineAlert": false,
        "alertState": "ERROR",
        "wifiConnectionHealth": null,
        "spaRunState": null,
        "ambientTemp": 0,
        "day": 0,
        "month": 0,
        "year": 0,
        "reminderCode": null,
        "reminderDaysClearRay": 0,
        "reminderDaysWater": 0,
        "reminderDaysFilter1": 0,
        "reminderDaysFilter2": 0,
        "blowout": false,
        "waterLevel1": false,
        "waterLevel2": false,
        "flowSwitchClosed": false,
        "changeUV": false,
        "hiLimitTemp": 0,
        "registrationLockout": false,
        "engineeringMode": false,
        "accessLocked": false,
        "maintenanceLocked": false,
        "temperatureReached": false
    },
    "c8zCurrentState": null,
    "salesDate": "2021-09-07T14:27:18.117Z",
    "registrationDate": "2025-05-05T18:16:33.424Z",
    "manufacturedDate": "2021-09-07T14:27:06.851Z",
    "p2pAPSSID": "CMS_SPA_123456789",
    "buildNumber": "1130/130",
    "p2pAPPassword": "",
    "alerts": [
        {
            "spaId": "123456789",
            "ownerId": "123456789",
            "dealerId": "5bc449b728381aee3670d90a",
            "oemId": "5a04e66f283885d17ed233f2",
            "controllerType": "NGSC",
            "code": 16,
            "number": 23,
            "timestamp": "2025-05-06T22:16:00.000Z",
            "faultLogReceivedTimestamp": "2025-05-06T22:16:00.000Z",
            "severity": "ERROR",
            "targetTemp": 73,
            "sensorATemp": 72,
            "sensorBTemp": 78,
            "celcius": true,
            "_id": "68939af77cf82457256e1bf9",
            "createdAt": "2025-08-06T18:12:07.490Z",
            "updatedAt": "2025-08-06T18:12:07.490Z",
            "__v": 0
        }
    ],
    "lastAlertDate": "2025-04-13T19:19:21.840Z",
    "isDefault": true,
    "ownerEmail": "email@example.com",
    "ownerId": {
        "_id": "123456789",
        "_class": "com.bwg.iot.model.User",
        "dealerId": "5bc449b728381aee3670d90a",
        "dealerName": "Novitek",
        "oemId": "5a04e66f283885d17ed233f2",
        "oemName": "Oy Nordic Spa Ltd",
        "lastName": "lastname",
        "firstName": "firstname",
        "phone": "00123456789",
        "email": "email@example.com",
        "address": {
            "address1": "email@example.com",
            "address2": "",
            "city": "city",
            "state": "state",
            "country": "country",
            "zip": "",
            "_id": "123456789"
        },
        "roles": [
            "OWNER"
        ],
        "createdDate": "2023-01-23T15:48:16.278Z",
        "notes": "",
        "active": true,
        "spaId": "abcd1234",
        "deviceToken": "abcd1234",
        "deviceType": "IOS",
        "links": [],
        "lastLogin": "2025-08-23T07:40:05.998Z",
        "updatedAt": "2025-08-23T07:40:05.998Z",
        "fullName": "firstname lastname",
        "timeZone": "Europe/Helsinki"
    },
    "ownerName": "firstname lastname",
    "updatedAt": "2025-08-23T05:39:16.885Z",
    "regKey": "abcd1234",
    "ipAddress": "",
    "brokerId": null
}

POST https://iot.controlmyspa.com/spa-commands/temperature/value
    {
        "spaId": "abcd1234",
        "via": "MOBILE",
        "value": "99",
    }

POST https://iot.controlmyspa.com/spa-command/component-state
    {
        "spaId": "abcd1234",
        "via": "MOBILE",
        "state": "HIGH",
        "deviceNumber": 0,
        "componentType": "jet"
    }
    {
        "spaId": "abcd1234",
        "state": "HIGH",
        "via": "MOBILE",
        "deviceNumber": 0,
        "componentType": "light"
    }
    {
        "componentType": "light",
        "state": "OFF",
        "spaId": "abcd1234",
        "via": "MOBILE",
        "deviceNumber": 0
    }

POST https://iot.controlmyspa.com/spa-commands/panel/state
    {
        "spaId": "abcd1234",
        "via": "MOBILE",
        "state": "LOCK_PANEL"
    }
    {
        "state": "UNLOCK_PANEL",
        "via": "MOBILE",
        "spaId": "abcd1234"
    }

POST https://iot.controlmyspa.com/spa-commands/temperature/heater-mode
    {
        "spaId": "abcd1234",
        "mode": "REST",
        "via": "MOBILE"
    }
    {
        "spaId": "abcd1234",
        "via": "MOBILE",
        "mode": "READY"
    }

POST https://iot.controlmyspa.com/spa-commands/temperature/range
    {
        "spaId": "abcd1234",
        "via": "MOBILE",
        "range": "HIGH"
    }
    {
        "spaId": "abcd1234",
        "range": "LOW",
        "via": "MOBILE"
    }
```
