from tools.table import *
from scapy.all import *
import ipaddress
import socket
import subprocess
from tools.utils import *

class NetworkTable(Table):


    def probe_network(self, network_address, subnet_mask, tmo):
        if not request_root():
            return 0
        hosts = []
        network = ipaddress.IPv4Network((network_address, subnet_mask), strict=False)
        
        # Loop through all the IP addresses in the network and print them
        for ip_address in network:
            ans = srp1(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=str(ip_address)), verbose=0, timeout = tmo)
            if ans is not None:
                mac = find_between_r(str(ans),"at","says")
                hosts.append({Network_Keys.IP_ADDRESS.name:str(ip_address), Network_Keys.MAC_ADDRESS.name:str(mac)})
        self.data = hosts
        return 1

class Network_Keys(Enum):
    IP_ADDRESS = 1
    MAC_ADDRESS = 2


