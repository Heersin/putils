from scapy.all import *
import sys



def main():
    if len(sys.argv) != 2:
        print("python client.py [Your server]")
        exit(1)

    YOUR_ICMP_SERVER = sys.argv[1]

    while True:
        cmd = input("Your Cmd > ")

        # payload => cmd
        # Protocol Type: Ping
        # IP protocol Type: IPv4
        pinger = IP(dst=YOUR_ICMP_SERVER)/ICMP(id=0x0, seq=0x0)/cmd
        ans, unans = sr(pinger)
        response = ans[0][1]
        recv = response.load
        result = recv.decode('utf-8')

        print("Server Response : {}".format(result))

if __name__ == "__main__":
    main()

