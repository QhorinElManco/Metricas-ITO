from zabbix import zabbix
from pyzabbix import ZabbixMetric, ZabbixSender
from functionDate import *
from metricas import metricas

# OBTENER LOS HOSTS


def getHosts(hostid=None, groupHost=None):
    if hostid == None and groupHost == None:
        hosts = zabbix.host.get(output=('host', 'hostid'),
                                selectParentTemplates=('templateid', 'name'),
                                sortfield='hostid', sortorder='ASC')
        return hosts
    elif hostid:
        hosts = zabbix.host.get(output=('host', 'hostid'), hostids=hostid,
                                selectParentTemplates=('templateid', 'name'),
                                sortfield='hostid', sortorder='ASC')
        return hosts
    elif groupHost:
        group = zabbix.hostgroup.get(output=('extend'),
                                     selectHosts=('hostid'),
                                     filter={'name': groupHost})
        group = group[0]['hosts']
        hosts = []
        for host in group:
            hosts.append(host['hostid'])
        hosts = getHosts(hostid=hosts)
        return hosts

# OBTENER LOS EVENTOS DEL HOST


def getEvents(hostid):
    events = zabbix.event.get(output=('eventid', 'clock', 'r_eventid'), hostids=hostid,
                              select_acknowledges=('extend'),
                              problem_time_from=timeFrom,
                              problem_time_till=timeTill,
                              filter={'name': 'Unavailable by ICMP ping'},
                              sortfield='clock', sortorder='ASC')
    
    return events


########################################################################################
#hosts = getHosts(groupHost='Network-Test')
data = {
    'freq': None,
    'days': None,
    'host': None,
}
#hostid = '10445'
hostid = None
groupHost = None
hosts = getHosts(hostid, groupHost)
for host in hosts:
    print((host['host']).center(70,'-'))
    # ESTABLECER FECHA INICIAL Y FECHA FINAL

    fechaReporte = currentDate()
    #fechaReporte = currentDate()

    timeTill = datetime(fechaReporte.year, fechaReporte.month, fechaReporte.day)
    timeFrom = timeTill - relativedelta(months=1)
    timeTill = timeTill-relativedelta(seconds=1)
    print(f'Eventos desde fecha: {timeFrom}')
    print(f'Eventos hasta fecha: {timeTill}')

    # CASTEO DE FORMATO DE FECHA
    timeTill = dateUnix(timeTill)
    timeFrom = dateUnix(timeFrom)

    # CALCULO DE METRICAS
    events = getEvents(host['hostid'])

    metrica = metricas(events, formatDate(timeFrom), formatDate(timeTill))
    print(metrica)

    # OBTENER EL ID DEL TEMPLATE METRICAS_ITO
    templateid = zabbix.template.get(
        output=('templateid'), filter={'name': 'Metricas_ITO'})

    # SI EL TEMPLATE NO EXISTE RETORNA UN MENSAJE
    if len(templateid) == 0:
        print('No existe el template')
        continue
    templateid = templateid[0]['templateid']

    # VERIFICAR SI EL HOST CUENTA CON EL TEMPLATE METRICAS_ITO
    templateExists = False
    for template in host['parentTemplates']:
        if template['templateid'] == templateid:
            templateExists = True
            break

    # AGREGAR EL TEMPLATE AL HOST EN CASO QUE NO CUENTE CON EL
    if not templateExists:
        template = zabbix.template.massadd(
            templates=(templateid),
            hosts=(host['hostid'])
        )
        time.sleep(60)

    # CREACION Y ENVIO DE METRICAS
    #packet = [
    #   ZabbixMetric(host['host'], 'metrica.fallas', metrica['failures']),
    #   ZabbixMetric(host['host'], 'metrica.inactivo', metrica['inactive']),
    #   ZabbixMetric(host['host'], 'metrica.acknowledge', metrica['timeAck'])
    #]
    #result = ZabbixSender(
    #   zabbix_server='mon.lab.agrega.com', zabbix_port=10051).send(packet)
    #print(result)
    print(f"""Los datos del dispositivo {host['host']} han sido enviados exitosamente
    {metrica}
    Result
    """)
zabbix.user.logout()
