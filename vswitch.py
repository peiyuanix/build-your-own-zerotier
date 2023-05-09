#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys

# parse parameters
server_port = None
if len(sys.argv) != 2:
  print("Usage: python3 vswitch.py {VSWITCH_PORT}")
  sys.exit(1)
else:
  server_port = int(sys.argv[1])
server_addr = ("0.0.0.0", server_port)

# 0. create UDP socket, bind to service port
vserver_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
vserver_sock.bind(server_addr)
print(f"[VSwitch] Started at {server_addr[0]}:{server_addr[1]}")

mac_table = {}

while True:
  # 1. read ethernet frame from VPort
  data, vport_addr = vserver_sock.recvfrom(1518)

  # 2. parse ethernet frame
  eth_header = data[:14]
  #    ethernet destination hardware address (MAC)
  eth_dst = ":".join("{:02x}".format(x) for x in eth_header[0:6])
  #    ethernet source hardware address (MAC)
  eth_src = ":".join("{:02x}".format(x) for x in eth_header[6:12])

  print(f"[VSwitch] vport_addr<{vport_addr}> "
        f"src<{eth_src}> dst<{eth_dst}> datasz<{len(data)}>")
  
  # 3. insert/update mac table
  if (eth_src not in mac_table or mac_table[eth_src] != vport_addr):
    mac_table[eth_src] = vport_addr
    print(f"    ARP Cache: {mac_table}")

  # 4. forward ethernet frame
  #    if dest in mac table, forward ethernet frame to it
  if eth_dst in mac_table:
    vserver_sock.sendto(data, mac_table[eth_dst])
    print(f"    Forwarded to: {eth_dst}")
  #    if dest is broadcast address, 
  #    broadcast ethernet frame to every known VPort except source VPort
  elif eth_dst == "ff:ff:ff:ff:ff:ff":
    brd_dst_macs = list(mac_table.keys())
    brd_dst_macs.remove(eth_src)
    brd_dst_vports = {mac_table[mac] for mac in brd_dst_macs}
    print(f"    Broadcasted to: {brd_dst_vports}")
    for brd_dst in brd_dst_vports:
      vserver_sock.sendto(data, brd_dst)
  #    otherwise, for simplicity, discard the ethernet frame
  else:
    print(f"    Discarded")