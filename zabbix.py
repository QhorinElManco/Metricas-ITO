import sys
import logging
from pyzabbix.api import ZabbixAPI


#logger = logging.getLogger("pyzabbix")
#logger.setLevel(logging.DEBUG)
#handler = logging.StreamHandler(sys.stdout)
#logger.addHandler(handler)


zabbix = ZabbixAPI(url='', user='', password='')
