import sys
import requests
import json

import options
import scanner.wifi as wifi


def main():
    wifi_scanner = wifi.WiFi(options.ADAPTER, options.DUMP_DIR+'/capture.pcapng', filter_oui=True, scan_time=options.SCAN_TIME, oui_path=options.PROJECT_DIR+'/ieee8802/oui.txt', ignore_randomization=False, filter_rssi=True, rssi_limit=-70)

    while True:
        try:
            count = wifi_scanner.discover_devices()
            requests.post(options.URL+'update', data=json.dumps({'region': options.REGION, 'traffic': count}))
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

if __name__ == '__main__':
    main()