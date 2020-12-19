import glob
import json
import sys
import time
import traceback
from datetime import datetime
import logging

import firebase_admin
from firebase_admin import credentials, firestore

import Adafruit_DHT

class MyFirebase:
    def __init__(self):
        self.path = "HomeTemperatures"

        self.cred = credentials.Certificate("test-b5d28-firebase-adminsdk-vl2t6-ae26d4dd10.json")
        firebase_admin.initialize_app(self.cred)
        self.firestore_db = firestore.client()

    def addReading(self, Temperature, Humidity):
        dic = {'time': datetime.now(), 'temperature': Temperature, 'humidity': Humidity}
        self.firestore_db.collection(self.path).add(dic)
        print(dic)

    def readAllAndPrint(self):
        snapshots = list(self.firestore_db.collection(self.path).get())
        for snapshot in snapshots:
            print(snapshot.to_dict())


if __name__ == '__main__':
    logger = logging.getLogger('log')
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    db = MyFirebase()
    starttime = time.time()
    while(True):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(11, 4,delay_seconds=0)
            db.addReading(temperature, humidity)
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
        except Exception as e:
            logging.error("Loop failed", exc_info=True)
            traceback.print_stack()
            time.sleep(1 * 60)

