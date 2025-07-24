## Instalation and configuration

Create database file:

```
cd db
cp empty.db data.db
```

Add Adafruit library:

```
cd sensors
python -m venv env
source env/bin/activate
python -m pip install adafruit-circuitpython-dht lgpio RPi.GPIO
```
