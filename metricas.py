from functionDate import *
from zabbix import zabbix


def metricas(events, startDate, finalDate):
    data = {'failures': 0, 'inactive': 0,
            'available': 0, 'timeAck': 0}
    data['available'] = round(dateDifference(startDate, finalDate), 1)

    # SI HAY EVENTOS CALCULA LAS METRICAS
    if len(events) != 0:
        for event in events:

            # HORA DE PROBLEMA
            hourProblem = formatDate(event['clock'])
            data['failures'] += 1

            # SI EL EVENTO FUE SOLUCIONADO OBTENEMOS EL EVENTO DE RESOLUCION
            if event['r_eventid'] != '0':

                # OBTENER EVENTO DE RESOLUCIÓN
                eventResolve = zabbix.event.get(
                    output=('eventid', 'clock'), eventids=event['r_eventid'])

                # HORA DE RESOLUCION
                hourResolve = formatDate(eventResolve[0]['clock'])

                # CASO 1
                if finalDate > hourProblem >= startDate and hourResolve > finalDate:
                    data['inactive'] += dateDifference(hourProblem, finalDate)
                    inactive = dateDifference(hourProblem, finalDate)
                    caso = 1
                # CASO 2
                elif finalDate > hourResolve >= startDate and startDate > hourProblem:
                    data['inactive'] += dateDifference(startDate, hourResolve)
                    inactive = dateDifference(startDate, hourResolve)
                    caso = 2
                # CASO 3
                elif startDate > hourProblem and hourResolve > finalDate:
                    data['inactive'] += dateDifference(startDate, finalDate)
                    inactive = dateDifference(startDate, finalDate)
                    caso = 3
                # CASO 4
                elif finalDate > hourProblem >= startDate and finalDate > hourResolve >= startDate:
                    data['inactive'] += dateDifference(
                        hourProblem, hourResolve)
                    inactive = dateDifference(hourProblem, hourResolve)
                    caso = 4

            # AUN NO TIENE RESOLUCIÓN
            else:
                hourResolve = "No resuelto aún"
                # EL PROBLEMA INICIÓ ANTES DEL MES A PROCESAR?
                if hourProblem < startDate:
                    data['inactive'] += dateDifference(startDate, finalDate)
                    inactive = dateDifference(startDate, finalDate)
                    caso = 6
                else:
                    data['inactive'] += dateDifference(hourProblem, finalDate)
                    inactive = dateDifference(hourProblem, finalDate)
                    caso = 7

            #print(f'''
            #NUEVO EVENTO
            #-Caso problema: {caso}
            #-Falla el: {hourProblem}
            #-Resolucion el: {hourResolve}''')

            # SI EL PROBLEMA TIENE ESTADO ACKNOWLEDGE
            if len(event['acknowledges']) != 0:
                # HORA DEL ACKNOWLEDGE
                hourAck = formatDate(event['acknowledges'][0]['clock'])

                data['timeAck'] += dateDifference(hourProblem, hourAck)
                ack = dateDifference(hourProblem, hourAck)
                casoAck = 6

            # AUN NO TIENE ACKNOWLEDGE
            else:
                hourAck = "Sin acknowledge"

                data['timeAck'] += dateDifference(hourProblem, finalDate)
                ack = dateDifference(hourProblem, finalDate)
                casoAck = 8
            #print(f'''
            #      -Caso acknowlegde: {casoAck}
            #      -Acknowlegde: {hourAck}
            #      -Inactivo: {inactive}
            #      -Tiempo al acknowledge: {ack}
            #      
            #      ''')
        data['inactive'] = round(data['inactive'], 1)
        data['timeAck'] = round(data['timeAck'], 1)

    return data
