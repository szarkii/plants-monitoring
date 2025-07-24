## Instalation and configuration

Create database file:

```
cd db
cp empty.db data.db
```

Add Adafruit library:

```
cd measure
python -m venv env
source env/bin/activate
python -m pip install adafruit-circuitpython-dht lgpio RPi.GPIO
```

Configure crontab:

```
*/10 * * * * <path>/plants-monitoring/measure/env/bin/python <path>/plants-monitoring/measure/measure.py
```
