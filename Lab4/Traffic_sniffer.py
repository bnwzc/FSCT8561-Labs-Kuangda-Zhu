from scapy.all import rdpcap, TCP, UDP, IP

packets = rdpcap("botnet-capture-20110812-rbot.pcap")

tcp_count = 0
udp_count = 0
for pkt in packets:
  if IP in pkt:
    if TCP in pkt:
      tcp_count += 1
      protocol = "TCP"
    elif UDP in pkt:
      udp_count += 1
      protocol = "UDP"
    else:
      protocol = "Unknown"

    if protocol in ("TCP", "UDP"):
      print(f"Source: {pkt[IP].src} Destination: {pkt[IP].dst} Protocol: {protocol} Source port: {pkt[protocol].sport} Destination port: {pkt[protocol].dport}")
    
    if tcp_count + udp_count == 20:
      break
print(f"\nTotal TCP packets: {tcp_count}")
print(f"Total UDP packets: {udp_count}")