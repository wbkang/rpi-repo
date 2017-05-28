from threading import Lock
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, asc, desc
from sqlalchemy.sql import select
from sqlalchemy.types import TIMESTAMP, Float
from rpiweather import config
import logging

logger = logging.getLogger(__name__)
metadata = MetaData()

meteo_table = Table('meteo', metadata,
                          Column('time', TIMESTAMP(timezone=True)),
                          Column('type', String),
                          Column('value', Float))

data_lock = Lock()

engine = None

def init():
    global engine
    db_path = config.data['conn_string']
    engine = create_engine(db_path, echo=False)
    metadata.create_all(engine)

def insert_data(dt, type_, value):
    with data_lock:
        with engine.connect() as conn:
            logger.debug("Inserting data (%s, %s, %s)" % (dt, type_, value))
            ins = meteo_table.insert().values(time=dt, type=type_, value=value)
            conn.execute(ins)



def get_recent_datapoints():
    with data_lock:
        with engine.connect() as conn:
            sel = select([meteo_table]).\
                    order_by(asc("time"))
            return list(conn.execute(sel))
            

