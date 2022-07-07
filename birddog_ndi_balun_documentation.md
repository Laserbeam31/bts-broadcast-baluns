Documentation for BTS BirdDog NDI HDMI IP Baluns
================================================

The BTS BirdDog baluns can send or receive HDMI video over NDI. Unlike the broadcast baluns (see `broadcast_balun_operation+spoofing.md` file), the
NDI stream handled by the birddogs is not broadcast/multicast and  can be sent nicely over an IP network without the need for a segregated VLAN for 
each stream.

A further advatage of distributing video over NDI is that a computer on the same network as the NDI baluns (e.g. the BTS Mac Pro) can ingest or send NDI
video directly via its network card, thhus reducing the need for physical video output connections directly to the machine.

Configuration access:
---------------------

Each BirdDog has a network-accessible web interface. To access this interface, enter the correct IP address into a computer's web browser on the
same network as the baluns. A password is requested:

Password: [REDACTED]

**NB: Do not use Safari to access the BirdDog web interface. There are a number of bugs in the way in which Safari displays/processes the BirdDog
interface which can lead to irritating problems, such as NDI streams not showing up for selection when in 'Decode' mode**

IP settings:
------------

The BirdDogs are set to use self-assigned static IP addresses in the 10.10.100.0/24 subnet. This corresponds to the "video control" VLAN on the
touring networks. Using self-assigned static IP addresses allows the BirdDogs also to be used on networks other than the touring racks, on which there
might possibly be no DHCP server running.

Each BirdDog has a number and the following hostname format: `BIRDDOG-X` Where `X` is the balun-specific number.
Each BirdDog has the following self-assigned IP address: `10.10.100.X` Where `X` is the balun-specific number.

Although unimportant for typical operation, the gateway IP address setting on each balun is pointed at `10.10.100.254` - the address of the touring racks'
EdgeRouter.

**These IP settings should be sufficient for correct BirdDog operation on any BTS event. Please do not change them as this makes it difficult for the
next user to pin down their IP address**

Colour space:
-------------

Particular attention should be paid to the "colour space" used by the BirdDogs. Colour space is changed separately for NDI "encode" (HDMI-NDI) and
NDI "decode" (NDI-HDMI) operaions.

HDMI - their output connection - supports RGB or YUV (effectively 
compressed RGB). However, it is possible (and indeed, in the case of BTS, probable) to convert HDMI to DVI with a passive adapter. DVI does not
support YUV; only RGB. The colour space on the BirdDogs is therefore always left set to RGB, in order to maximise compatibility.

HDMI-NDI (encode) operation:
----------------------------

To use a BirdDog to ingest HDMI, log into the web interface and navigate to `A/V -> Device Settings -> Operation Mode` and select `Encode`.
Scroll to the bottom section of the `A/V` page and click `Apply`.

Once the changes have been applied and an HDMI source connected, the BirdDog in question will appear, to other NDI-enabled devices on the same
network, as a video source.

The `NDI Encode` section of the `A/V` control page on the BirdDogs' web interface can change NDI encoding settings. For regular use, there is no need to
change anything here.

NDI-HDMI (decode) operation:
----------------------------

To use a BirdDog to decode NDI back to HDMI, log into the web interface and navigate to `A/V -> Device Settings -> Operation Mode` and select `Decode`.
Scroll to the bottom section of the `A/V` page and click `Apply`.

For decode use, it is necessary to tell the BirdDog which NDI stream to decode. This is done in the `NDI Decode` section of the `A/V` control page.
Select the source to be decoded from the 'Available NDI Sources' dropdown menu. If a known-good source is not showing up on this dropdown, click the
`Refresh` button at the bottom of the `NDI Decode` settings, or try using a different browser.

Aside from the `Decode Screensaver` option (which serves to act as a 'No NDI signal' indicator on the output display), no other options in `NDI Decode`
need be changed for regular use.





