import time
from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import *

zone_local = timezone('America/Tegucigalpa')
formatTime = '%Y-%m-%d %H:%M:%S'

# Funcion para castear a formato datetime


def formatDate(date):
    date = datetime.strptime(datetime.fromtimestamp(
        int(date)).strftime(formatTime), formatTime)
    return date

# Funcion para castear a formato unixtime


def dateUnix(date):
    return str(int(date.timestamp()))


# Funcion para la fecha actual


def currentDate():
    date = datetime.strptime(datetime.now(zone_local)
                             .strftime(formatTime), formatTime)
    return date


# Funcion para calcular la diferencia entre dos fechas en minutos


def dateDifference(firsDate, lastDate):
    dateDifference = (lastDate - firsDate).total_seconds()/60
    return dateDifference
