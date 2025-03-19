#!/usr/bin/env python

import netfilterqueue

def process_packet(packet):
    print(packet)
    packet.accept()

queue_num = input("Enter the Queue Number you want to route intercepted packets to: ")
queue = netfilterqueue.NetfilterQueue()
queue.bind(queue_num, process_packet)
queue.run()
