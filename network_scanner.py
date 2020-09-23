#!/usr/bin/env python3

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='range of IP addresses to scan i.e. 10.1.1.1/24')
    options = parser.parse_args()
    if not options.target:
        parser.error('[-] Please specify an ip range, use --help for more info.')
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        clients_dict = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list


def print_result(results_list):
    print('IP\t\t\tMAC Address\n-----------------------------------------')
    for client in results_list:
        print(client['ip'] + '\t\t' + client['mac'])


ip_range = get_arguments()
scan_result = scan(ip_range.target)
print_result(scan_result)
