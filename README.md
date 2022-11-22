# khushere-hardware
KHUSHERE is an app dedicated to show traffic of certain places in Kyung Hee University. It can detect how many people are nearby by counting mobile devices'. Since most of university students carry at least one mobile devices, it can pretty certainly provide traffic with quite an accuracy.


This system can be used not only for providing whether enclosed space is crowded but preventing accidents like [Itaewon Halloween Crowd Crush](https://www.koreaherald.com/view.php?ud=20221030000006). You can even use it for controlling lighting and heating to save fossil fuel usage!


It reports MAC addresses and their signal strangth every 60 seconds. Server applies Kalman filter to smooth spikes. It also handles MAC address randomization by filtering patterns of randomized MAC address.

# Hardware
This project is based on Raspberry PI 3 B+ and RTL8192eu(Iptime N400UA)

# Prerequisites
## Installation
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

## Monitor Mode
khushere-hardware uses wlan0 as monitoring interface. To enable interface, use the following script
```
sudo ./enable_monitor
```
