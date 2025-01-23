#!/usr/bin/env python

# Simple Packet Sniffer
# Captures and displays basic packet information on a specified interface

import scapy.all as scapy

def sniff(interface):
    print(f"[+] Sniffing packets on {interface}...")
    scapy.sniff(iface=interface, store=False, prn=process_packet)

def process_packet(packet):
    if packet.haslayer(scapy.IP):
        src_ip = packet[scapy.IP].src
        dst_ip = packet[scapy.IP].dst
        protocol = packet[scapy.IP].proto

        if packet.haslayer(scapy.TCP):
            print(f"[+] TCP: {src_ip} -> {dst_ip} (Port: {packet[scapy.TCP].dport})")
        elif packet.haslayer(scapy.UDP):
            print(f"[+] UDP: {src_ip} -> {dst_ip} (Port: {packet[scapy.UDP].dport})")
        elif packet.haslayer(scapy.ARP):
            print(f"[+] ARP: {packet[scapy.ARP].psrc} is at {packet[scapy.ARP].hwsrc}")

sniff("eth0")
