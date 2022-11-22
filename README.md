# khushere-hardware
Hardware for detecting human presense in project KhusHere

## Installation
This project is based on Raspberry PI 3 B+ and RTL8192eu(Iptime N400UA)

## Prerequisites
### Installation
[tshark](https://www.wireshark.org/docs/man-pages/tshark.html) is required to capture probe requests.
```
sudo add-apt-repository -y ppa:wireshark-dev/stable
sudo apt install -y tshark
```

For security reasons, I **strongly** recommand to change permissions of tcpdump instead of tshark.
```
groupadd pcap
usermod -a -G pcap nonrootuser

chgrp pcap /usr/sbin/tcpdump
chmod 750 /usr/sbin/tcpdump

setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
```

This Project uses [PDM](https://pdm.fming.dev/latest/) to manage python dependancies. To install required libraries, use:
```
pdm install
```

### Monitor Mode
