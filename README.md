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

[+] packet_sniffer.py
Takes input of interface (i.e. eth0, wlan0, etc.)
Can be used in conjunction with arp_spoofer.py, while conducting MITM attack
Outputs HTTP requests the target is making, and searches for possible usernames or passwords passed in clear text
Future versions will allow user to specify what traffic to filter by
Future version will also show source IP address for utilization across a network

[+] dns_spoofer.py
Used to modify target DNS requests to redirect to malicous web server
Currently not very user friendly and need to add arguments and error messages
Future version will allow for user input website name to spoof
will also have ability to automatically create and flush iptables queue
