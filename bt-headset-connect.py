#!/usr/bin/python3.6

import time
import Bluetoothctl as blctl
import utils as utils

logger = utils.getLogger()
bose_headset = utils.getBoseHeadset()

def main():
    bl = blctl.Bluetoothctl()

    logger.info("Checking if headset is connected")
    connected = bl.is_connected_with_headset()
    while not connected:
        logger.info("Trying to connect to headset")
        bl.connect(bose_headset['mac_address'])
        time.sleep(5)
        connected = bl.is_connected_with_headset()
        
    #else:
    #    bl.disconnect(bose_headset['mac_address'])

    logger.info("Device is connected. Exiting")

if __name__ == "__main__":
    main()