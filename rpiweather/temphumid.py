from dht11 import dht11
import logging
import threading
from rpiweather.sampler import Sampler
from rpiweather.data import insert_data
from collections import deque
import time
import datetime
import pytz
from rpiweather import config

PIN_DHT = config.temphumid['dht11']['pin'] 
SAMPLE_INTERVAL = config.temphumid['sample_interval']

logger = logging.getLogger(__name__)

temp_sensor = dht11.DHT11(pin=PIN_DHT)


def measure():
    return temp_sensor.read()


def sample():
    record = measure()
    if record.is_valid():
        logger.debug("Record: temp_avg:%r hum_avg:%r" %
                     (record.temperature, record.humidity))
        now = datetime.datetime.now(pytz.utc)
        insert_data(now, "temperature", record.temperature)
        insert_data(now, "humidity", record.humidity)


sampler = Sampler(SAMPLE_INTERVAL, sample)


def start_recording():
    logger.info("Start sampling")
    sampler.start()
