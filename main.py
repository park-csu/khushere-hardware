import sys

import options as options
import wifi.wifi


def main():
    wifi_scanner = wifi.wifi.WiFi(options.ADAPTER, options.DUMP_DIR+'/capture.pcapng', filter_oui=True, scan_time=options.SCAN_TIME, oui_path=options.PROJECT_DIR+'/ieee8802/oui.txt', ignore_randomization=False, filter_rssi=True, rssi_limit=-70)

    while True:
        try:
            wifi_scanner.discover_devices()
        
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

if __name__ == '__main__':
    main()