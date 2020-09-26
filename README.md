# Simple-Python-Scripts
Fairly simple python scripts used for pen testing

[+] mac_changer.py
Takes an input of what interface you want to change the MAC address of (i.e. eth0, wlan0, etc.)
Takes input of MAC address, must be put in the format of 00:00:00:00:00:00
Future version will allow option of manual entry of MAC address or randomized MAC address
Future version will also allow for timing of address change, such as every 2 minutes

[+] network_scanner.py
Takes an input of IP address or IP range in format of 10.0.0.1/24
Uses scapy to create ARP packets to discover IPs on the network and associates them to their MAC address
Useful for device discovery on a network without utilizing ping sweeps
Future version will guess manufacturer of device based on MAC address

[+] arp_spoofer.py
Takes input of target machine you want to conduct MITM attack on, and the gateway ip address
Uses scapy to create ARP packets to sends ARP responses to both devices so that traffic is passed through the attacker machine
Once attack has concluded, exit script with CTRL + C. This will restore the ARP tables on the devices
