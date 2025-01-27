#!/usr/bin/env python

# this code uses <scapy> module, which I can't get to run on windows for whatever reason.
# troubleshooting: consider making sure scapy or scapy-winpcap are installed on your windows machine.

import scapy.all as scapy
import argparse
import getpass
from termcolor import colored

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
    print(colored("\nIP\t\t\tMAC Address", "blue"))
    print(colored("----------------------------------", "cyan"))
    for client in results_list:
        print(f"{colored(client['ip'], 'green')}\t\t{colored(client['mac'], 'yellow')}")

args = get_arguments()
username = getpass.getuser()
print(colored("\n----------------------------------", "cyan"))
print(colored(f"NetScan requested by:", "magenta") + colored(f"\t{username}", "yellow"))
print(colored("----------------------------------", "cyan"))
scan_result = scan(args.target)
print_result(scan_result)
print(colored("\n[+] Scan completed!", "green"))
