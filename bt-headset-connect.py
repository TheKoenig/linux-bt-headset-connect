#!/usr/bin/python3.6

import time
import Bluetoothctl as blctl
import utils as utils
import argparse

logger = utils.getLogger()
bose_headset = utils.getBoseHeadset()
args = None


def handleArguments():
    parser = argparse.ArgumentParser(
        description="A tool which tries to keep a Bluetooth headset connection alive."
    )
    parser.add_argument(
        "--keep_alive", "-k", help="Set a flag whether to keep function alive. Take True/False as value")
    parser.add_argument("--version", "-v", action="version",
                        version="%(prog)s " + "0.0.1")
    global args
    args = parser.parse_args()

def main():
    handleArguments()

    bl = blctl.Bluetoothctl()

    logger.info("Checking if headset is connected")
    connected = bl.is_connected_with_headset()
    while not connected:
        logger.info("Trying to connect to headset")
        bl.connect(bose_headset['mac_address'])
        time.sleep(5)
        connected = bl.is_connected_with_headset()
        
    if args.keep_alive:
        time.sleep(10)
        main()

    logger.info("Device is connected. Exiting")

if __name__ == "__main__":
    main()