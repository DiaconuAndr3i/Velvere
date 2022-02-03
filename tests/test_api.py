import unittest
import requests
import time


def generateTimestamp():
    elem = str(time.time()).split(".")
    return "".join(elem)


class ApiTest(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api"
    refreshToken = ""
    accessToken = ""
    email = ""
    password = ""
    timestamp = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = generateTimestamp()

    def test1_register(self):
        data = {
            "nickname": f"{self.timestamp}",
            "email": f"{self.timestamp}@{self.timestamp}.com",
            "password": "Test123!"
        }
        self.email = data["email"]
        self.password = data["password"]

        response = requests.post(self.URL + "/auth/register", json=data)
        self.assertEqual(response.status_code, 201)
        print("Test 1 completed")

    def test2_login(self):
        data = {
            "email": F"{self.email}",
            "password": f"{self.password}"
        }
        response = requests.post(self.URL + "/auth/login", json=data)
        self.assertEqual(response.status_code, 200)
        self.refreshToken = response.json()["user"]["refresh"]
        print("Test 2 completed")

    def test3_refreshToken(self):
        headers = {"Authorization": f"Bearer {self.refreshToken}"}
        response = requests.get(self.URL + "/auth/refresh/token", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.accessToken = response.json()["access"]
        print("Test 3 completed")

    def test4_getAllPlants(self):
        response = requests.get(self.URL + "/infoPlants/getPlants")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        print("Test 4 completed")

    def test5_insertPlant(self):
        data = {
            "name": "Lalea",
            "origin_country": "Europa",
            "opt_humidity": "0.5",
            "opt_temperature": "23"
        }
        headers = {"Authorization": f"Bearer {self.accessToken}"}
        response = requests.post(self.URL + "/infoPlants/insert", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        print("Test 5 completed")

    def test6_scanPlant(self):
        response = requests.get(self.URL + "/plantScanner/scanResponse")
        self.assertEqual(response.status_code, 200)
        print("Test 6 completed")

    def test7_showPlantFromGreenHouse(self):
        response = requests.get(self.URL + "/plantScanner/showPlantFromGreenHouse")
        self.assertEqual(response.status_code, 200)
        print("Test 7 completed")

    def test8_putPlantInGreenHouse(self):
        data = {
            "name": "Trandafir",
            "opt_humidity": "0.3",
            "opt_temperature": "21.5",
            "origin_country": "America de Nord, Europa, Asia, Africa de Nord-Vest"
        }
        headers = {"Authorization": f"Bearer {self.accessToken}"}
        response = requests.post(self.URL + "/plantScanner/putPlantInGreenHouse", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        print("Test 8 completed")

    def test9_sensorForHumidityTemperature(self):
        data = {
            "humidity": "0.3",
            "temperature": "23"
        }
        headers = {"Authorization": f"Bearer {self.accessToken}"}
        response = requests.post(self.URL + "/humidityTemperatureSensor/sensorForHumidityTemperature", json=data,
                                 headers=headers)

        self.assertIn(response.status_code, [201, 404])
        print("Test 9 completed")

    def test10_addUtilities(self):
        data = {
            "name": f"{self.timestamp}",
            "quantity": "5",
            "unit_measure": "kg"
        }
        headers = {"Authorization": f"Bearer {self.accessToken}"}
        response = requests.post(self.URL + "/utilities/addUtilities", json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        print("Test 10 completed")

    def test11_getUtilities(self):
        headers = {"Authorization": f"Bearer {self.accessToken}"}
        response = requests.get(self.URL + "/utilities/getUtilities", headers=headers)
        self.assertEqual(response.status_code, 200)
        print("Test 11 completed")

    def test12_updateUtility(self):
        data = {
            "name": f"{self.timestamp}",
            "quantity": "1"
        }
        headers = {"Authorization": f"Bearer {self.accessToken}"}
        response = requests.put(self.URL + "/utilities/updateUtility", json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        print("Test 12 completed")


if __name__ == "__main__":
    tester = ApiTest()
    tester.test1_register()
    tester.test2_login()
    tester.test3_refreshToken()
    tester.test4_getAllPlants()
    tester.test5_insertPlant()
    tester.test6_scanPlant()
    tester.test7_showPlantFromGreenHouse()
    tester.test8_putPlantInGreenHouse()
    tester.test9_sensorForHumidityTemperature()
    tester.test10_addUtilities()
    tester.test11_getUtilities()
    tester.test12_updateUtility()
