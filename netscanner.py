#!/usr/bin/env python

# this code uses <scapy> module, which I can't get to run on windows for whatever reason.
# troubleshooting: consider making sure scapy or scapy-winpcap are installed on your windows machine.

import scapy.all as scapy
import argparse
import getpass

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True, help="Target IP / IP range.")
    return parser.parse_args()

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n----------------------------------")
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}")

args = get_arguments()
username = getpass.getuser()
print("----------------------------------")
print("NetScan requested by:\t" + username)
print("----------------------------------")
scan_result = scan(args.target)
print_result(scan_result)
