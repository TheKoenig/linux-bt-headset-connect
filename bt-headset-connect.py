#!/usr/bin/python3.6

import time
import Bluetoothctl as blctl
import utils as utils
import argparse
import pulsectl
import sys

logger = utils.getLogger()
bl = blctl.Bluetoothctl()
pulse = pulsectl.Pulse('pulse-bt')
headset = utils.getHeadsetDetails()
args = None


def handleArguments():
    """Handles CLI arguments and saves them globally"""
    parser = argparse.ArgumentParser(
        description="A tool which tries to keep a Bluetooth headset connection alive."
    )
    parser.add_argument(
        "--keep_alive", "-k", help="Set a flag whether to keep function alive. Take True/False as value")
    parser.add_argument("--version", "-v", action="version",
                        version="%(prog)s " + "0.0.1")
    global args
    args = parser.parse_args()

def isSinkA2dp():
    """Checks whether current headset sink is A2DP sink"""
    sink_list = pulse.sink_list()
    if len(sink_list) < 1:
        logger.error("No sinks detected")
        return False
    for sink in sink_list:
        try:
            if headset["mac_address"] == sink.proplist["device.string"]:
                if "a2dp" in sink.name:
                    logger.info("Current sink is A2DP sink")
                    return True
                else:
                    logger.info("Current sink is not A2DP sink: {}".format(sink.name))
                    return False
        except KeyError:
            logger.warn("Sink does not have property 'device.string': {}".format(str(sink)))
            continue
    # in case none of the sinks are related to the headset
    return False

def getHeadsetCard():
    """Returns sound card which matches with headset description"""
    card_list = pulse.card_list()
    if len(card_list) < 1:
        logger.error("No cards detected")
        sys.exit(1)
    for card in card_list:
        if utils.replaceColonWithUnderline(headset["mac_address"]) in card.name:
            return card
        else:
            logger.debug("Card name ({}) does not match headset MAC address ({}). Trying next".format(card.name, headset["mac_address"]))
    logger.error("No card found. Available card names: {}".format(card_list))
    sys.exit(1)    

def changeCardActiveProfileToA2dp(card):
    """Changes active profile of card to A2DP"""
    a2dp_profile_filter_result = filter(lambda x : x.name == "a2dp_sink", card.profile_list)
    a2dp_profile_filter_result_list = list(a2dp_profile_filter_result)
    if len(a2dp_profile_filter_result_list) != 1:
        logger.error("No or multiple A2DP profile(s) found")
        sys.exit(1)
    a2dp_profile = a2dp_profile_filter_result_list[0]
    if card.profile_active == a2dp_profile:
        logger.info("Current card profile is A2DP")
    else:
        logger.info("Current card profile not A2DP: {}".format(card.profile_active.name))
        logger.info("Trying to change to A2DP profile")
        pulse.card_profile_set(card, a2dp_profile)

def ensureConnected():
    """Checks the connection state to the headset and eventually tries to reconnect"""
    logger.info("Checking if headset is connected")
    connected = bl.is_connected_with_headset()
    while not connected:
        logger.info("Trying to connect to headset")
        bl.connect(headset['mac_address'])
        time.sleep(5)
        connected = bl.is_connected_with_headset()

def ensureA2dp():
    """Checks the card profile state and eventually sets it to A2DP"""
    logger.info("Checking if headset is in A2DP mode")
    is_a2dp = isSinkA2dp()
    while not is_a2dp:
        logger.info("Trying to disconnect headset to enforce A2DP mode")
        changeCardActiveProfileToA2dp(getHeadsetCard())
        time.sleep(5)
        is_a2dp = isSinkA2dp()

def main():
    handleArguments()

    ensureConnected()
    ensureA2dp()
        
    if args.keep_alive:
        time.sleep(10)
        main()

    logger.info("Device is connected and in A2DP mode. Exiting")

if __name__ == "__main__":
    main()