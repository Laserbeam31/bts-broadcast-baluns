Documentation for BTS BirdDog NDI HDMI IP Senders
=================================================

The BTS BirdDog senders can send or receive HDMI video over NDI. Unlike the "broadcast baluns", the
NDI stream handled by the BirdDogs is not broadcast/multicast and can be sent nicely over a shared IP 
network without the need for a segregated VLAN per stream.

A further advantage of distributing video over NDI is that a computer on the same network as the NDI senders 
(e.g. the BTS Mac Pro) can ingest or send NDI video directly via its network card, reducing the need for 
physical video connections on the machine.

Configuration access:
---------------------

Each BirdDog has a network-accessible web interface. To access this interface, enter the unit's IP address into a web browser on the
same network as the senders. A password is required:

Password: [REDACTED]

**NB: Do not use Safari to access the BirdDog web interface. There are a number of bugs in the way in which Safari displays/processes the BirdDog
interface which can lead to irritating problems, such as NDI streams not showing up for selection when in 'Decode' mode**

IP settings:
------------

The BirdDogs are set to use self-assigned static IP addresses in the 10.10.100.0/24 subnet. This corresponds to the "Video Control" VLAN on the
touring networks. Using self-assigned static IP addresses allows the BirdDogs to also be used on networks other than the touring racks, where there
may be no DHCP server running.

Each BirdDog has a number and the following hostname format: `BIRDDOG-X` Where `X` is the unit-specific number.
Each BirdDog has the following self-assigned IP address: `10.10.100.X` Where `X` is the unit-specific number.

Although unimportant for typical operation, the gateway IP address setting on each sender is pointed at `10.10.100.254` - the local address of the 
touring racks' EdgeRouter.

**These IP settings should be sufficient for correct BirdDog operation on any BTS event. Please do not change them as this makes it difficult for the
next user to pin down the IP address**

Colour space:
-------------

Particular attention should be paid to the "colour space" used by the BirdDogs. Colour space is changed separately for NDI "encode" (HDMI-NDI) and
NDI "decode" (NDI-HDMI) operaions.

HDMI - their output connection - supports RGB or YUV (effectively compressed RGB). However, it is possible (and indeed, in the case of BTS, probable) 
to convert HDMI to DVI with a passive adapter. DVI devices do not tend to use YUV; only RGB. The colour space on the BirdDogs is therefore usually 
set to RGB in order to maximise compatibility.

HDMI-NDI (encode) operation:
----------------------------

To use a BirdDog to ingest HDMI, log into the web interface and navigate to `A/V -> Device Settings -> Operation Mode` and select `Encode`.
Scroll to the bottom section of the `A/V` page and click `Apply`.

Once the changes have been applied and an HDMI source connected, the BirdDog in question will appear to other NDI-enabled devices on the same
network as a video source.

The `NDI Encode` section of the `A/V` control page on the BirdDogs' web interface can change NDI encoding settings. For regular use, there is no need to
change anything here.

NDI-HDMI (decode) operation:
----------------------------

To use a BirdDog to decode NDI back to HDMI, log into the web interface and navigate to `A/V -> Device Settings -> Operation Mode` and select `Decode`.
Scroll to the bottom section of the `A/V` page and click `Apply`.

For decode use, it is necessary to tell the BirdDog which NDI stream to decode. This is done in the `NDI Decode` section of the `A/V` control page.
Select the source to be decoded from the 'Available NDI Sources' dropdown menu. If a known-good source is not showing up in this dropdown, click the
`Refresh` button at the bottom of the `NDI Decode` settings or try using a different browser.

Aside from the `Decode Screensaver` option (which serves to act as a 'No NDI signal' indicator on the output display), no other options in `NDI Decode`
need be changed for regular use.

Standing config:
----------------

Network:
- DHCP: disabled
- IP address:   10.10.100.x (where x is the BirdDog number, as written on the front)
- Subnet mask:  255.255.255.0
- Gateway:      10.10.100.254
- Hostname:     BIRDDOG-x (where x is the BirdDog number, as written on the front)

System:
- Preferred transmit method:    TCP
- preferred receive method:     TCP
- NDI discovery server:         Off

A/V:
- Operation mode:               [User-adjustable based on intended event-specific use]; leave as `Decode`
- Video input format:           Auto
- HDMI input colour space:      RGB
- Analogue in gain:             [Disabled]
- Analogue out gain:            [Disabled]
- HDMI tally:                   Off
- Headset mode:                 Decode
- HDMI colour space:            RGB
- Current source:               [User-adjustable based on intended event-specific use]
- Decode stream select:         Full
- Decode screensaver:           [User-adjustable based on intended event-specicic use]; leave as `BirdDog`
- Bitrate management:           NDI managed
- NDI output bandwidth:         [Disabled]
- NDI audio:                    Active
- Onboard tally:                Off
- Encode Failover source name:  [User-adjustable based on intended event-specific use]
- Encode Failover source IP:    [User-adjustable based on intended event-specific use]
