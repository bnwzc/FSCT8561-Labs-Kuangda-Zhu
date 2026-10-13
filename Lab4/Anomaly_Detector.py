from scapy.all import rdpcap, TCP, UDP, IP

packets = rdpcap("botnet-capture-20110812-rbot.pcap")

TCP_UDP_pkt = []
alert_system = {}
sus = []
tcp_count = 0
udp_count = 0
for pkt in packets:
  if IP in pkt:
    if TCP in pkt:
      TCP_UDP_pkt.append(pkt)
      tcp_count += 1
    elif UDP in pkt:
      TCP_UDP_pkt.append(pkt)
      udp_count += 1

for pkt in TCP_UDP_pkt:
  if pkt[IP].src not in alert_system:
    alert_system[pkt[IP].src] = [float(pkt.time)]
  else:
    alert_system[pkt[IP].src].append(float(pkt.time))

  alert_system[pkt[IP].src].sort()
  for i in range(len(alert_system[pkt[IP].src])):
    if (alert_system[pkt[IP].src][-1] - 5.0) <= alert_system[pkt[IP].src][i]:
      alert_system[pkt[IP].src] = alert_system[pkt[IP].src][i:]
      if len(alert_system[pkt[IP].src]) > 20 and pkt[IP].src not in sus:
        print(f"WARNING: Too many packets from {pkt[IP].src}")
        sus.append(pkt[IP].src)
      break

print(f"\nTotal TCP packets: {tcp_count}")
print(f"Total UDP packets: {udp_count}")
print(f"Total suspicious IPs: {len(sus)}")