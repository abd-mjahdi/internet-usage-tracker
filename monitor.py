from scapy.all import *
import psutil
from collections import defaultdict

connection2pid = {}
pid2traffic = defaultdict(int)


def get_all_network_adapter_macs():
    all_mac_addresses = {iface.mac for iface in ifaces.values()}
    return all_mac_addresses

def track_connections():
    for con in psutil.net_connections():
        try:
            local_port = con.laddr.port
            remote_port = con.raddr.port
            con_pid = con.pid 
        except Exception:
            continue

        connection2pid[( local_port , remote_port )]=con_pid    
        connection2pid[( remote_port , local_port )]=con_pid


