import time
import os

eth_address=open("ethernetAddress.txt","r")
interface=eth_address.read()
eth_address.close()

command=("sudo tcpreplay -i "+interface+" balun_capture_2.pcap")

while True:
	os.system(command)
	time.sleep(2)
