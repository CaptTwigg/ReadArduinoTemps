import json
from datetime import datetime

import firebase_admin
import serial
from firebase_admin import credentials, firestore

from firebaseTest import myFirebase


# firestore_db.collection(u'songs').add({'song': 'Imagine', 'artist': 'John Lennon'})
# firestore_db.collection(path).add({'time': datetime.now(), 'temperature': 22, 'humidity': 40})

# snapshots = list(firestore_db.collection(path).get())
# for snapshot in snapshots:
#     print(snapshot.to_dict())
class MyFirebase:
    def __init__(self):
        self.path = "HomeTemperatures"

        self.cred = credentials.Certificate("test-b5d28-firebase-adminsdk-vl2t6-ae26d4dd10.json")
        firebase_admin.initialize_app(self.cred)
        self.firestore_db = firestore.client()

    def addReading(self, Temperature, Humidity):
        self.firestore_db.collection(self.path).add(
            {'time': datetime.now(), 'temperature': Temperature, 'humidity': Humidity})

    def readAllAndPrint(self):
        snapshots = list(self.firestore_db.collection(self.path).get())
        for snapshot in snapshots:
            print(snapshot.to_dict())


class MySerial:
    def __init__(self):
        self.com = serial.Serial(port="COM3", baudrate=9600)

    def readLine(self) -> dict:
        rawData = self.com.readline().decode("utf-8")
        return json.loads(rawData)


if __name__ == '__main__':
    db = MyFirebase()
    ser = MySerial()
    db.addReading(**ser.readLine())
    db.readAllAndPrint()
