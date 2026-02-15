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

def process_packet(packet):
    try :
        source_port = packet.sport
        dest_port = packet.dport
        src_mac = packet.src
    except Exception:
        return
    if ((source_port , dest_port) in connection2pid.keys()) and (src_mac not in get_all_network_adapter_macs()):
        pid = connection2pid[(source_port , dest_port)]
        pid2traffic[pid]+=len(packet)

    