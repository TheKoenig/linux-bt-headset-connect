#!/usr/bin/env python3

import logging

def getLogger():
    logger = logging.getLogger("btctl")
    logger.setLevel(logging.DEBUG)

    # Enable logging to console
    if len(logger.handlers) < 1:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(ch)

    return logger

def getHeadsetDetails():
    headset_details = {'name': "LE-Bose AE2 SoundLink", 'mac_address': "2C:41:A1:FC:7F:5F"}
    return headset_details

def replaceColonWithUnderline(str):
    return str.replace(':', '_')