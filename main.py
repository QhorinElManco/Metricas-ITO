from zabbix import zabbix
from pyzabbix import ZabbixMetric, ZabbixSender
from functionDate import *
from metricas import metricas, metricas2
# OBTENER LOS HOSTS


def getHosts(hostid=''):
    if hostid == '':
        hosts = zabbix.host.get(output=('host', 'hostid'),
                                selectTags="extend",
                                selectInterfaces=["interfaceid"], sortfield='hostid', sortorder='ASC')
        return hosts
    else:
        hosts = zabbix.host.get(output=('host', 'hostid'), hostid=hostid,
                                selectTags="extend",
                                selectInterfaces=["interfaceid"], sortfield='hostid', sortorder='ASC')
        return hosts
    return print('NO HAY HOSTS')

# OBTENER LOS EVENTOS DEL HOST


currentDate = currentDate()
previewMonth = lastMonth(currentDate)
currentDate = dateUnix(currentDate)
previewMonth = dateUnix(previewMonth)


def getEvents(hostid):
    events = zabbix.event.get(output=('eventid', 'clock', 'r_eventid'), hostids=hostid,
                              select_acknowledges=('clock'),
                              #time_from=previewMonth, time_till=currentDate,
                              filter={'name': 'Unavailable by ICMP ping'},
                              sortfield='clock', sortorder='ASC')
    return events


########################################################################################
hosts = getHosts()

for host in hosts:
    hini = ''
    hend = ''
    # CALCULO DE METRICAS
    events = getEvents(host['hostid'])
    if len(events) != 0:
        # COMPROBAR SI ES UN SERVICIO CON HORA DE INICIO Y HORA FIN
        if len(host['tags']) != 0:
            for tag in host['tags']:
                if tag['tag'] == 'HINI':
                    hini = tag['value']
                elif tag['tag'] == 'HFIN':
                    hend = tag['value']
        # VERIFICA SI ES SERVICIO O NO PARA DEFINIR QUE CALCULO DE METRICA USAR
        if hini != '' and hend != '':
            metrica = metricas2(events, int(hini), int(hend))
        else:
            metrica = metricas(events)
        print(f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
               MTTD: {metrica['MTTD']}
               MTTA: {metrica['MTTA']}
               MTTR: {metrica['MTTR']}
               MTBF: {metrica['MTBF']}
               ''')
        # ITEM PARA MTTD
        items = zabbix.item.get(
            filter={'name': 'metrica.'+host['host']+'.mttd'})
        if len(items) != 0:
            item = zabbix.item.update(itemid=items[0]['itemid'],
                                      description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTTD: {metrica['MTTD']['MTTD']}, 
                                        INCIDENCIAS: {metrica['MTTD']['INCIDENCIAS']}, 
                                        TIEMPO: {metrica['MTTD']['TIEMPO']}
                                        ''')
        else:
            item1 = zabbix.item.create(hostid=host['hostid'], name='metrica.'+host['host']+'.mttd',
                                       key_='metrica.'+host['host']+'.mttd', type=2,
                                       value_type=0, interfaceid=host["interfaces"][0]["interfaceid"],
                                       units='mins',
                                       tags=[{'tag': 'Metrica ITO'},
                                             {'tag': 'metrica', 'value': 'MTTD'}],
                                       description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTTD: {metrica['MTTD']['MTTD']}, 
                                        INCIDENCIAS: {metrica['MTTD']['INCIDENCIAS']}, 
                                        TIEMPO: {metrica['MTTD']['TIEMPO']}
                                        ''',
                                       delay=3600)
        # ITEM PARA MTTA
        items = zabbix.item.get(output="itemid",
                                filter={'name': 'metrica.'+host['host']+'.mtta'})
        if len(items) != 0:
            item = zabbix.item.update(itemid=items[0]['itemid'],
                                      description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTTA: {metrica['MTTA']['MTTA']}, 
                                        INCIDENCIAS: {metrica['MTTA']['INCIDENCIAS']}, 
                                        TIEMPO AL ACKNOWLEDGE: {metrica['MTTA']['TIEMPO AL ACKNOWLEDGE']}
                                        ''')
        else:
            item1 = zabbix.item.create(hostid=host['hostid'], name='metrica.'+host['host']+'.mtta',
                                       key_='metrica.'+host['host']+'.mtta', type=2,
                                       value_type=0, interfaceid=host["interfaces"][0]["interfaceid"],
                                       units='mins',
                                       tags=[{'tag': 'Metrica ITO'},
                                             {'tag': 'metrica', 'value': 'MTTA'}],
                                       description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTTA: {metrica['MTTA']['MTTA']}, 
                                        INCIDENCIAS: {metrica['MTTA']['INCIDENCIAS']}, 
                                        TIEMPO AL ACKNOWLEDGE: {metrica['MTTA']['TIEMPO AL ACKNOWLEDGE']}  
                                        ''',
                                       delay=3600)
        # ITEM PARA MTTR
        items = zabbix.item.get(
            filter={'name': 'metrica.'+host['host']+'.mttr'})
        if len(items) != 0:
            item = zabbix.item.update(itemid=items[0]['itemid'],
                                      description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTTR: {metrica['MTTR']['MTTR']}, 
                                        INCIDENCIAS: {metrica['MTTR']['INCIDENCIAS']}, 
                                        TIEMPO TOTAL DE REPARACION: {metrica['MTTR']['TIEMPO']}
                                        ''')
        else:
            item1 = zabbix.item.create(hostid=host['hostid'], name='metrica.'+host['host']+'.mttr',
                                       key_='metrica.'+host['host']+'.mttr', type=2,
                                       value_type=0, interfaceid=host["interfaces"][0]["interfaceid"],
                                       units='mins',
                                       tags=[{'tag': 'Metrica ITO'},
                                             {'tag': 'metrica', 'value': 'MTTR'}],
                                       description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTTR: {metrica['MTTR']['MTTR']}, 
                                        INCIDENCIAS: {metrica['MTTR']['INCIDENCIAS']}, 
                                        TIEMPO TOTAL DE REPARACION: {metrica['MTTR']['TIEMPO']}
                                        ''',
                                       delay=3600)
        # ITEM PARA MTBF
        items = zabbix.item.get(
            filter={'name': 'metrica.'+host['host']+'.mtbf'})
        if len(items) != 0:
            item = zabbix.item.update(itemid=items[0]['itemid'],
                                      description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTBF: {metrica['MTBF']['MTBF']}, 
                                        INCIDENCIAS: {metrica['MTBF']['INCIDENCIAS']}, 
                                        TIEMPO TOTAL DISPONIBLE: {metrica['MTBF']['TIEMPO TOTAL DISPONIBLE']}                
                                        TIEMPO INACTIVO: {metrica['MTBF']['TIEMPO INACTIVO']}      
                                        HOLA
                                        ''')
        else:
            item1 = zabbix.item.create(hostid=host['hostid'], name='metrica.'+host['host']+'.mtbf',
                                       key_='metrica.'+host['host']+'.mtbf', type=2,
                                       value_type=0, interfaceid=host["interfaces"][0]["interfaceid"],
                                       units='mins',
                                       tags=[{'tag': 'Metrica ITO'},
                                             {'tag': 'metrica', 'value': 'MTBF'}],
                                       description=f'''Hostname: {host["host"]} con hostid: {host["hostid"]}
                                        MTBF: {metrica['MTBF']['MTBF']}, 
                                        INCIDENCIAS: {metrica['MTBF']['INCIDENCIAS']}, 
                                        TIEMPO TOTAL DISPONIBLE: {metrica['MTBF']['TIEMPO TOTAL DISPONIBLE']}                
                                        TIEMPO INACTIVO: {metrica['MTBF']['TIEMPO INACTIVO']}      
                                        ''',
                                       delay=3600)
        # CREACION Y ENVIO DE METRICAS
        packet = [
            ZabbixMetric(host['host'], 'metrica.' +
                         host['host']+'.mttd', metrica['MTTD']['MTTD']),
            ZabbixMetric(host['host'], 'metrica.' +
                         host['host']+'.mtta', metrica['MTTA']['MTTA']),
            ZabbixMetric(host['host'], 'metrica.' +
                         host['host']+'.mttr', metrica['MTTR']['MTTR']),
            ZabbixMetric(host['host'], 'metrica.' +
                         host['host']+'.mtbf', metrica['MTBF']['MTBF'])
        ]
        result = ZabbixSender(
            zabbix_server='190.5.99.234', zabbix_port=10051).send(packet)
    else:
        print(
            f'No hay incidencias en host: {host["host"]} con hostid: {host["hostid"]}')
