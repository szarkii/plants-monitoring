#!/usr/bin/python

import os
import sqlite3
import time
import numbers
import adafruit_dht
import board

dht_device = adafruit_dht.DHT11(board.D17)

def read_temperature_and_humidity():
    for i in range(10):
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if isinstance(temperature, numbers.Number) and isinstance(humidity, numbers.Number):
                return {"temperature": temperature, "humidity": humidity}
            
        except RuntimeError as err:
            print(err.args[0])

        time.sleep(2.0)

    raise Exception("Cannot measure temperature and humidity")


try:
    script_path = os.path.abspath(os.path.dirname(__file__))
    connection = sqlite3.connect(script_path + "/../db/data.db")
    cursor = connection.cursor()
    print("DB Init")

    measurments = read_temperature_and_humidity()
    print(measurments)
    cursor.execute("INSERT INTO humidity VALUES (datetime('now', 'localtime'), {})".format(measurments["humidity"]))
    cursor.execute("INSERT INTO air_temperature VALUES (datetime('now', 'localtime'), {})".format(measurments["temperature"]))

    cursor.close()

except sqlite3.Error as error:
    print("Error occurred -", error)

finally:
    if connection:
        connection.commit()
        connection.close()
        print("SQLite Connection closed")