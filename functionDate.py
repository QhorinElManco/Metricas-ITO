import time
from datetime import datetime
from dateutil.relativedelta import *


formatTime = '%Y-%m-%d %H:%M:%S'

# Funcion para castear a formato datetime


def formatDate(date):
    return datetime.strptime(datetime.fromtimestamp(int(date)).strftime(formatTime), formatTime)

# Funcion para castear a formato unixtime


def dateUnix(date):
    return str(int(time.mktime(date.timetuple())))

# Funcion para la fecha actual


def currentDate():
    return datetime.strptime(datetime.now().strftime(formatTime), formatTime)

# Funcion para obtener el mes anterior a partir de la una fecha
# por defecto la calcula con la fecha actual


def lastMonth(currentMonth=currentDate()):
    return (currentMonth - relativedelta(months=1))

# Funcion para calcular la diferencia entre dos fechas en minutos


def dateDifference(firsDate, lastDate):
    dateDifference = (lastDate - firsDate).total_seconds()/60
    return dateDifference
