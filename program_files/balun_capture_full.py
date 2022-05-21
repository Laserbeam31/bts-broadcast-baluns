#!usr/bin/env/python

#MASTER PYTHON2 SCRIPT TO EXTRACT VIDEO STREAM FROM BTS BROADCAST BALUNS - J. LUCAS 21/05/2022

#Pings transmitter to check connection, and decodes sender's UDP stream of JPEG images, whilst
#continually sending the necessary "keepalive" packets (captured in wireshark from a real receiver)
#to keep the sender in a sending state.

#Connection principle between real receiver and sender baluns
#------------------------------------------------------------
#1. ARP "who-is" request from receiver to work out IP address of sender. This is achieved through the "pinging transmitter" stage of this program;
#2. Receiver starts sending "keepalive" messages to the sender;
#3. The sender balun sends a UDP stream of JPEG frames on multicast address 226.2.2.2;
#4. The receiver balun decodes the stream and sends it on an HDMI output. In this program, the
#   decoding is done by a separate script called in the "running conversion" stage, the output of which is piped into VLC Media Player

#Program prerequisites
#---------------------
#1. Computer must be on the same VLAN/network as the broadcast sender to which it wants to connect;
#2. Computer must have a non-conflicting IP address in the 192.168.168.xxx/24 range. The default IP address of a sender broadcast balun is
#   192.168.168.55 and the default IP address of a receiver broadcast balun is 192.168.168.56;
#3. VLC and tcpreplay must be installed on the system.

#Potential uses for these scripts
#--------------------------------
#1. Diagnostic purposes: checking the presence of broadcast video on a particular VLAN;
#2. A means of getting an HDMI feed into a computer without an (expensive) capture care.



#Imports
import time
import os
import subprocess

#Get custom inputs if Option 2 selected
def gatherCustomInputs():

	#Input IP address of sender
	pingCommand=("ping -c 3 "+raw_input("Enter IP address of sender here: "))	

	#File to store Ethernet interface name
	eth_address=open("ethernetAddress.txt","w+")
	eth_address_temp=raw_input("Enter Ethernet interface name: ")
	eth_address.write(eth_address_temp)
	eth_address.close()

	return(pingCommand)

#Loop to ask user's choice
escape = False
while escape==False:
	print('''
	############################################################################
	####		BROADCAST BALUN COMPUTER INTERFACE PROGRAM		####
	####			JOHN LUCAS - 21/05/2022				####
	############################################################################
	#									   #
	#		Options:						   #
	#		1. Continue with default interface settings		   #
	#		2. Continue with custom interface settings                 #
	#		3. Quit							   #
	#									   #
	############################################################################
	''')

	selection=raw_input("Enter option: ")

	if selection=="1":
		escape = True
		eth_address=open("ethernetAddress.txt","w+")
	        eth_address_temp="eno1"
	        eth_address.write(eth_address_temp)
	        eth_address.close()
		pingCommand=("ping -c 3 192.168.168.55")
	elif selection=="2":
		escape = True
		pingCommand=gatherCustomInputs()
	elif selection=="3":
		escape = True
		quit()
	else:
		print("Invalid input. Please enter option number 1-3")
		escape = False

#Kill any existing VLC processes
print("--------------------------------------------------------------------")
print("Killing pre-existing VLC process(es)")
print("--------------------------------------------------------------------")
time.sleep(0.5)
os.system("sudo pkill vlc")
time.sleep(3)

#Ping transmitter balun 3 times to achieve ARP resolution and also check connectivity
print("--------------------------------------------------------------------")
print("Pinging transmitter 3 times")
print("--------------------------------------------------------------------")
time.sleep(0.5)
os.system(pingCommand)

#Send keepalive packet to transmitter using tcpreplay
print("--------------------------------------------------------------------")
print("Waking up sender!")
print("--------------------------------------------------------------------")
time.sleep(0.5)
subprocess.Popen(["python", "balun_trigger.py", ">/dev/null"])
time.sleep(3)

try:
	#Run conversion script, including pipe into new VLC instance
	print("--------------------------------------------------------------------")
	print("Running conversion script and piping into VLC")
	print("Press Ctrl+C at any time to quit!")
	print("--------------------------------------------------------------------")
	time.sleep(3)
	os.system("sudo python balun_capture.py | vlc -")
finally:
	os.system("sudo pkill -9 -f balun_trigger.py")
	quit()

