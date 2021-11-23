
from functionDate import *

# FUNCION PARA METRICAS CON HORARIO 24/7


def metricas(events):
    minsInactive = 0
    minsAck = 0
    numberEvents = 0
    numberAck = 0
    firstEvent = ''
    lastEvent = ''
    mttd = 0
    mtta = 0
    mttr = 0
    mtbf = 0
    metricas = {'MTTD': {}, 'MTTA': {}, 'MTTR': {}, 'MTBF': {}}
    for event in events:
        if event['r_eventid'] != '0':
            hourResolve = ''
            for eventResolve in events:
                if eventResolve['eventid'] == event['r_eventid']:
                    hourResolve = eventResolve['clock']
                    break
            hourProblem = formatDate(event['clock'])
            hourResolve = formatDate(hourResolve)
            minsInactive += dateDifference(hourProblem, hourResolve)
            numberEvents += 1
        # DATOS PARA MTTA
        if len(event['acknowledges']) != 0:
            hourProblem = formatDate(event['clock'])
            hourAck = event['acknowledges'][0]['clock']
            hourAck = formatDate(hourAck)
            minsAck += dateDifference(hourProblem, hourAck)
            numberAck += 1

    # MTTD
    if minsInactive != 0:
        mttd = round(numberEvents/minsInactive, 6)
    metricas['MTTD'] = {'INCIDENCIAS': numberEvents,
                        'TIEMPO': round(minsInactive, 2), 'MTTD': mttd}

    # MTTA
    if numberAck != 0:
        mtta = round(minsAck/numberAck, 2)
    metricas['MTTA'] = {'INCIDENCIAS': numberAck,
                        'TIEMPO AL ACKNOWLEDGE': round(minsAck, 2), 'MTTA': mtta}

    # MTTR
    if numberEvents != 0:
        mttr = round(minsInactive/numberEvents, 2)
    metricas['MTTR'] = {'INCIDENCIAS': numberEvents,
                        'TIEMPO': round(minsInactive, 2), 'MTTR': mttr}

    # MTBF
    firstEvent = formatDate(events[0]['clock'])
    lastEvent = formatDate(events[len(events) - 1]['clock'])
    timeAvailable = dateDifference(firstEvent, lastEvent)
    mtbf = round((timeAvailable-minsInactive)/numberEvents, 2)
    metricas['MTBF'] = {'INCIDENCIAS': numberEvents,
                        'TIEMPO TOTAL DISPONIBLE': round(timeAvailable, 2), 'TIEMPO INACTIVO': round(minsInactive, 2), 'MTBF': mtbf}

    return metricas

# FUNCION PARA VERIFICAR EL HORARIO L-V DE 8-5


def validateDate(clock, hini, hend):
    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
    day = formatDate(clock)
    if (day.strftime('%A') in days) and hini <= day.hour <= hend:
        return True
    else:
        return False

# FUNCION PARA METRICAS CON HORARIO 8/5 (L-V Y 8AM-5PM)


def metricas2(events, hini, hend):
    minsInactive = 0
    minsAck = 0
    numberEvents = 0
    numberAck = 0
    firstEvent = ''
    lastEvent = ''
    mttd = 0
    mtta = 0
    mttr = 0
    mtbf = 0
    metricas = {'MTTD': {}, 'MTTA': {}, 'MTTR': {}, 'MTBF': {}}
    for event in events:
        # VERIFICAMOS QUE SEA UN PROBLEMA Y QUE ESTE DENTRO DEL HORARIO ESTABLECIDO
        if event['r_eventid'] != '0' and validateDate(event['clock'], hini, hend):
            # OBTENEMOS EL PRIMER PROBLEMA /// IMPORTANTE PARA MTBF
            if firstEvent == '':
                firstEvent = formatDate(event['clock'])
            hourResolve = ''
            # BUSCAMOS EL EVENTO DE LA SOLUCION
            for eventResolve in events:
                if eventResolve['eventid'] == event['r_eventid']:
                    hourResolve = eventResolve['clock']
                    break
            hourProblem = formatDate(event['clock'])
            hourResolve = formatDate(hourResolve)
            minsInactive += dateDifference(hourProblem, hourResolve)
            numberEvents += 1
            # GUARDAMOS EL ULTIMO EVENTO DENTRO DEL HORARIO ESTABLECIDO
            lastEvent = formatDate(event['clock'])
        # DATOS PARA MTTA
        # VERIFICAMOS QUE SEA UN PROBLEMA CON UN ACK Y QUE ESTE DENTRO DEL HORARIO ESTABLECIDO
        if (len(event['acknowledges']) != 0) and validateDate(event['clock'], hini, hend):
            # OBTENEMOS LA HORA EN QUE SE PRODUJO EL ACKNOWLEDGE
            hourProblem = formatDate(event['clock'])
            hourAck = event['acknowledges'][0]['clock']
            hourAck = formatDate(hourAck)
            minsAck += dateDifference(hourProblem, hourAck)
            numberAck += 1

    # MTTD
    if minsInactive != 0:
        mttd = round(numberEvents/minsInactive, 6)
    metricas['MTTD'] = {'INCIDENCIAS': numberEvents,
                        'TIEMPO': round(minsInactive, 2), 'MTTD': mttd}

    # MTTA
    if numberAck != 0:
        mtta = round(minsAck/numberAck, 2)
    metricas['MTTA'] = {'INCIDENCIAS': numberAck,
                        'TIEMPO AL ACKNOWLEDGE': round(minsAck, 2), 'MTTA': mtta}

    # MTTR
    if numberEvents != 0:
        mttr = round(minsInactive/numberEvents, 2)
    metricas['MTTR'] = {'INCIDENCIAS': numberEvents,
                        'TIEMPO': round(minsInactive, 2), 'MTTR': mttr}

    # MTBF
    lastEvent = formatDate(events[len(events) - 1]['clock'])
    timeAvailable = dateDifference(firstEvent, lastEvent)
    mtbf = round((timeAvailable-minsInactive)/numberEvents, 2)
    metricas['MTBF'] = {'INCIDENCIAS': numberEvents,
                        'TIEMPO TOTAL DISPONIBLE': round(timeAvailable, 2), 'TIEMPO INACTIVO': round(minsInactive, 2), 'MTBF': mtbf}

    return metricas
