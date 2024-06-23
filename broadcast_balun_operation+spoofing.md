Operation and Spoofing of the BTS Broadcast HDMI Baluns - John Lucas 25/05/2022
===============================================================================

The BTS Broadcast baluns convert HDMI signals to multicast IP data for transmission over Ethernet
networks. Being IP, they can go through network switches with no problems (unlike traditional
passive "HDMI over Cat5" baluns, which only change the physical transmission medium, rather
than re-encoding the signals to follow a totally different standard).

Owing to being multicast with regards to their mode of operation, these baluns MUST be used on
an isolated switch or VLAN.

The broadcast baluns use the unchangeable multicast address 226.2.2.2 for transmission of video 
on UDP port 2068. Each balun also has a unicast IP address which is used for control and 
management signals. The default management IP addresses are as follows:

Sender: 192.168.168.55
Receiver: 192.168.168.56

By manually placing a computer on the 192.168.168.xxx/24 wired network with the baluns, their
configuration webpages may be accessed, by entering their management unicast address into a browser.


How a sender and receiver balun communicate:
--------------------------------------------

1. When placed on the same network as a sender, the receiver sends out an ARP "who-has" discovery
   packet. This allows it to pinpoint the unicast _management_ IP address of the sender;

2. The sender responds, identifying itself to the receiver. At this stage, the receiver knows the
   management IP address of the sender, and starts periodically transmitting unicast "keepalive"
   packets to the sender over UDP. For as long as the sender is receiving these keepalive
   packets (typically at an interval of a few seconds), it distributes video on multicast
   address 226.2.2.2;

3. The sender encodes the original HDMI video as a multicast UDP stream of JPEG images 
   (MJPEG, in essence) which the receiver then re-assembles and converts back to a local HDMI 
   port for a screen/projector;
   
4. Since the sender produces multicast, this means that, on one VLAN/network, one sender can
   distribute video to many receivers - all of which "listen out" to the same multicast stream;
   
5. If the sender balun stops receiving the keepalive packets from the receiver balun(s), it ceases
   to transmit multicast video. This is probably for power saving reasons.
   

Extracting a sender's multicast stream with a computer:
-------------------------------------------------------

To be able to extract video onto a computer _directly_ from the multicast data stream (i.e. with
no intermediate receiver balun), the following steps are required. Owing to the basic nature of the
encoding used by these baluns, it is _not_ simply possible to enter the baluns' multicast address 
directly in VLC Media Player's "Open Network Stream" box:

1. The computer must be connected _only_ to the network/VLAN occupied by the receiver balun. It
   must also have its IP settings manually changed so that it resides on the 192.168.168.xxx/24
   unicast management network, with no IP address conflist relative to the other balun(s) on the
   network;
   
2. The computer must send out "spoofed" keepalive packets to the unicast management address of   
   the sender, in order to keep the sender in a transmissive state. In the case of the attached
   program, I achieved this by Wireshark-ing the output of a genuine receiver balun and extracting
   the periodic keepalive packets from the flood of multicast video;
   
3. The computer must process the UDP stream emanating from the sender and convert it into a
   viewable format. For this, I used the Python script from the following very useful webpage
   (which, incidentally, covers much the same process with a slightly older balun):
   
   https://blog.danman.eu/reverse-engineering-lenkeng-hdmi-over-ip-extender/
   
   This script extracts the JPEG images from the UDP stream and outputs them into a format
   which VLC Media Player can understand. It then pipes this image stream into VLC.
   

How my program works:
---------------------

Essentially, the program makes a Linux computer pretend to be a receiver balun.

My program, which is based on the script in the above webpage, ties together all the various
processes which much be carried out in order to successfully extract video from the sender
balun's multicast UDP output. My final program consists of the following scripts/files:

1. `balun_capture_full.py`:	The _main program_ which calls upon other smaller scripts
				and mediates the various tasks (as listed above) which must be
				carried out to extract the video feed.
				
2. `balun_capture.py`:		The script (called by the main program) 
				from the above website which does the main
				conversion between the UDP multicast stream and a usable set
				of JPEG images which VLC can handle.
				
3. `balun_trigger.py`:		A script (called by `balun_capture_full`)
				which periodically uses tcprepeat to regurgitate the
				keepalive packet to the sender's management unicast IP address.

4. `ethernetAddress.txt`	A text file which serves as a means to interface between the
				`balun_capture_full.py` and balun_trigger.py scripts. The user
				inputs the name of their computer's Ethernet interface in
				`balun_capture_full`, and it is then passed, by means of this
				text file, to `balun_trigger`, and used as a necessary argument
				in tcprepeat.

5. `balun_capture_2.pcap`	The packet-captured keepalive packet. This is what tcprepeat,
   				in `balun_trigger.py`, sends repeatedly to the sender balun 
				to keep it transmitting.
   

Required packages for my program to function correctly:
-------------------------------------------------------

- VLC Media player:	Used to display (and record/re-stream, if necessary) the output of the
			balun_capture.py decode script.
			
- TCPrepeat:		Used to regurgitate the keepalive packet.

- Python2:		Not Python3!


Notes and quirks:
-----------------

- Sometimes, the first time the program is run, VLC will not display anything. If this is the
  case, `Ctrl+C` to stop the program, and re-run it. For some strange reason, second time
  always works!
  
- The `balun_capture.py` script is actually designed to operate with a similar but older multicast HDMI 
  balun from a different manufacturer. This particular older model of balun had a bug whereby some UDP
  packets emanating from it were malformed. To extract data from this buggy datastream, a raw
  socket was needed in `balun_capture.py`. The BTS baluns do not suffer from this bug, and therefore
  balun_capture.py could be probably modified to operate over a UDP, rather than a raw, socket.







 
