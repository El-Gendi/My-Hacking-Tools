#!/usr/bin/env python

import subprocess
import argparse
import re
from termcolor import colored

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    args = parser.parse_args()
    if not args.interface:
        parser.error(colored("[-] Please specify an interface, use --help for more info.", "red"))
    elif not args.new_mac:
        parser.error(colored("[-] Please specify a new MAC address, use --help for more info.", "red"))
    return args

def change_mac(interface, new_mac):
    print(colored(f"[+] Changing MAC address for {interface} to {new_mac}", "yellow"))
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(colored("[-] Could not read MAC address.", "red"))

options = get_arguments()
current_mac = get_current_mac(options.interface)
print(colored(f"\n[Current MAC]", "cyan") + f" = {current_mac}")

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(colored(f"\n[+] MAC address was successfully changed to {current_mac}", "green"))
else:
    print(colored("\n[-] MAC address did not get changed.", "red"))
