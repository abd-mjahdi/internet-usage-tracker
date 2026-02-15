from scapy.all import *
import psutil
from collections import defaultdict

connection2pid = {}
pid2traffic = defaultdict(int)


def get_all_network_adapter_macs():
    all_mac_addresses = {iface.mac for iface in ifaces.values()}
    return all_mac_addresses

