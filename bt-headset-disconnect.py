import time
import Bluetoothctl as blctl
import utils as utils
import argparse
import pulsectl
import sys

logger = utils.getLogger()
bl = blctl.Bluetoothctl()
headset = utils.getHeadsetDetails()

def disconnect():
    """Disconnects from the device and sleeps for a bit"""
    logger.info("Trying to disconnect to headset")
    bl.disconnect(headset['mac_address'])
    time.sleep(5)


def main():
    disconnect()
    logger.info("Device is disconnected. Exiting")


if __name__ == "__main__":
    main()