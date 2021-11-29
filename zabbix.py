import sys
import logging
from pyzabbix.api import ZabbixAPI


#logger = logging.getLogger("pyzabbix")
#logger.setLevel(logging.DEBUG)
#handler = logging.StreamHandler(sys.stdout)
#logger.addHandler(handler)


zabbix = ZabbixAPI(url='http://190.5.99.234:81/', user='mpineda', password='Agrega.2021')
