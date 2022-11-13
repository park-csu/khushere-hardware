import os
import sys
import subprocess
import time
import re

from collections import defaultdict

import wifi.oui

class WiFi:
    def __init__(self, adapter: str, dump_path: str, scan_time: int = 30, filter_oui: bool = False, oui_path: str = "", filter_rssi: bool = False, rssi_limit: int = -70, ignore_randomization: bool = False):
        self.dump_path = dump_path
        self.scan_time = scan_time

        self.oui_list = {}
        if filter_oui:
            self.oui_list = self.load_oui(oui_path)

        self.adapter = adapter
        self.filter_oui = filter_oui
        self.filter_rssi = filter_rssi
        self.rssi_limit = rssi_limit
        self.ignore_randomization = ignore_randomization
        self.known_manufacturers = [
            "Motorola Mobility LLC, a Lenovo Company",
            "GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD",
            "Huawei Symantec Technologies Co.,Ltd.",
            "Microsoft",
            "HTC Corporation",
            "Samsung Electronics Co.,Ltd",
            "SAMSUNG ELECTRO-MECHANICS(THAILAND)",
            "BlackBerry RTS",
            "LG ELECTRONICS INC",
            "Apple, Inc.",
            "LG Electronics",
            "OnePlus Tech (Shenzhen) Ltd",
            "Xiaomi Communications Co Ltd",
            "LG Electronics (Mobile Communications)"]
    
    def discover_devices(self):
        scan_command = ['tshark', '-l', '-i', self.adapter, '-a', 'duration:'+str(self.scan_time), '-w', self.dump_path, '-f', 'subtype probe-req']
        scan_tshark = subprocess.Popen(
            scan_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        scan_stdout, _ = scan_tshark.communicate()
        print('TSHARK SCAN:\n', scan_stdout.decode('utf-8'))
        scan_timestamp = float(time.time())

        read_command = ['tshark', '-r', self.dump_path, '-T', 'fields', '-e', 'wlan.sa', '-e', 'wlan_radio.signal_dbm', '-V', 'wlan.ssid eq ""']
        read_tshark = subprocess.Popen(
            read_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        read_stdout, _ = read_tshark.communicate()
        read_data = read_stdout.decode('utf-8').split('\n')  # mac\trssi\n

        found_devices = defaultdict(list)
        for line in read_data:
            if line.strip() == "":
                continue

            mac, rssi = line.split('\t')
            if not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac):
                continue

            found_devices[mac].append(int(rssi))
        
        filtered_devices = defaultdict(dict)
        for mac, rssi in found_devices.items():
            average_rssi = float(sum(rssi))/float(len(rssi))
            if self.filter_rssi and average_rssi > self.rssi_limit:
                continue
            
            if not self.filter_oui:
                filtered_devices[mac] = {"average_rssi": average_rssi, "oui_info": "NotAvilable"}
                continue

            company = "Unregistered"
            mac_oui = mac[:8]
            if mac_oui in self.oui_list:
                company = mac_oui

            print(self.is_mac_randomized(mac))
            if self.filter_oui and company not in self.known_manufacturers:
                if not self.ignore_randomization and self.is_mac_randomized(mac) and company not in self.oui_list:
                    filtered_devices[mac] = {"average_rssi": average_rssi, "oui_info": "Randomized"}
                continue

            filtered_devices[mac] = {"average_rssi": average_rssi, "oui_info": company}

        if len(filtered_devices) == 0:
            print('Found no devices')
            return 0
        
        print(filtered_devices)
        return len(filtered_devices)

    def is_mac_randomized(self, mac: str):
        return mac.lower()[1] in ['0', '2', 'a', 'e']

    def load_oui(self, oui_path):
        if not os.path.isfile(oui_path):
            print('Downloading OUI information...')
            wifi.oui.download_oui(oui_path)

        oui_list = wifi.oui.load_oui(oui_path)
        if not oui_list:
            print(f'Failed to load {oui_path}')
            sys.exit(1)
        
        return oui_list
    