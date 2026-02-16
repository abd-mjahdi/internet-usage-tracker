"""
Simple internet usage tracker — Ethernet only.
Run as Administrator on Windows. Needs Npcap installed.
"""
from scapy.all import *
import psutil
from collections import defaultdict
from threading import Thread
import os
import time

# Which (local_port, remote_port) belongs to which process
connection_to_pid = {}
# How many bytes each process has downloaded
pid_to_bytes = defaultdict(int)
# Previous total per pid (to show speed)
prev_bytes = {}


def get_our_macs():
    return {iface.mac for iface in ifaces.values()}

OUR_MACS = get_our_macs()


def update_connections():
    """Learn which ports belong to which process."""
    while True:
        time.sleep(1)
        for con in psutil.net_connections():
            try:
                local_port = con.laddr.port
                remote_port = con.raddr.port
                pid = con.pid
            except Exception:
                continue
            connection_to_pid[(local_port, remote_port)] = pid
            connection_to_pid[(remote_port, local_port)] = pid


def on_packet(packet):
    """Count download bytes: packet from network to us, on a known connection."""
    try:
        if packet.haslayer(TCP):
            sport, dport = packet[TCP].sport, packet[TCP].dport
        elif packet.haslayer(UDP):
            sport, dport = packet[UDP].sport, packet[UDP].dport
        else:
            return
    except Exception:
        return

    key = (sport, dport)
    if key not in connection_to_pid:
        return
    # Only count packets coming *from* the network (not from this PC)
    if packet.haslayer(Ether) and packet[Ether].src in OUR_MACS:
        return

    pid = connection_to_pid[key]
    pid_to_bytes[pid] += len(packet)

def format_size(size):
    for t in ['', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.2f}{t}B/s"
        size /= 1024
    return f"{size:.2f}PB/s"



def show_stats():
    """Print each process and its download speed once per second."""
    global prev_bytes
    while True:
        time.sleep(1)
        rows = []
        for pid, total in pid_to_bytes.items():
            try:
                name = psutil.Process(pid).name()
            except psutil.NoSuchProcess:
                continue
            speed = total - prev_bytes.get(pid, 0)
            prev_bytes[pid] = total
            rows.append((name, speed))
        rows.sort(key=lambda x: x[1], reverse=True)
        os.system("cls")
        for name, speed in rows:
            #print(f"{name}: {speed} bytes/s")
            print(f"{name}: {format_size(speed)}")


if __name__ == "__main__":
    print("Ethernet usage tracker. Press Enter to start...")
    input()

    Thread(target=update_connections, daemon=True).start()
    Thread(target=show_stats, daemon=True).start()

    sniff(prn=on_packet, store=False, filter="tcp or udp")                              


       