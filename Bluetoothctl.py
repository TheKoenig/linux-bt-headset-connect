#!/usr/bin/python3.6

import time
import pexpect
import subprocess
import sys
import utils as utils

logger = utils.getLogger()
bose_headset = utils.getBoseHeadset()

class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        subprocess.check_output("rfkill unblock bluetooth", shell=True)
        self.process = pexpect.spawn("bluetoothctl", echo=False)

    def send(self, command, pause=0):
        self.process.send(f"{command}\n")
        time.sleep(pause)
        self.process.expect(["bluetooth", pexpect.EOF, pexpect.TIMEOUT], timeout=5)
        #    raise Exception(f"failed after {command}")

    def get_output(self, *args, **kwargs):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.send(*args, **kwargs)
        return self.process.before.decode('unicode_escape').split("\r\n")

    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            self.send("scan on")
        except Exception as e:
            logger.error(e)

    def make_discoverable(self):
        """Make device discoverable."""
        try:
            self.send("discoverable on")
        except Exception as e:
            logger.error(e)

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        if not any(keyword in info_string for keyword in block_list):
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
                    if len(attribute_list) > 2:
                        device = {
                            "mac_address": attribute_list[1],
                            "name": attribute_list[2],
                        }
        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        available_devices = []
        try:
            out = self.get_output("devices")
        except Exception as e:
            logger.error(e)
        else:
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)
        return available_devices

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        paired_devices = []
        try:
            out = self.get_output("paired-devices")
        except Exception as e:
            output = self.process.before.decode('utf_8').split("\r\n")
            print(output)
            logger.error(e)
        else:
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)
        return paired_devices

    def get_discoverable_devices(self):
        """Filter paired devices out of available."""
        available = self.get_available_devices()
        paired = self.get_paired_devices()
        return [d for d in available if d not in paired]

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            out = self.get_output(f"info {mac_address}")
        except Exception as e:
            logger.error(e)
            return False
        else:
            return out

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            self.send(f"pair {mac_address}", 4)
        except Exception as e:
            logger.error(e)
            return False
        else:
            res = self.process.expect(
                ["Failed to pair", "Pairing successful", pexpect.EOF]
            )
            return res == 1

    def trust(self, mac_address):
        try:
            self.send(f"trust {mac_address}", 4)
        except Exception as e:
            logger.error(e)
            return False
        else:
            res = self.process.expect(
                ["Failed to trust", "Pairing successful", pexpect.EOF]
            )
            return res == 1

    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        try:
            self.send(f"remove {mac_address}", 3)
        except Exception as e:
            logger.error(e)
            return False
        else:
            res = self.process.expect(
                ["not available", "Device has been removed", pexpect.EOF]
            )
            return res == 1

    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            self.send(f"connect {mac_address}", 2)
        except Exception as e:
            logger.error(e)
            return False
        else:
            res = self.process.expect(
                ["Failed to connect", "Connection successful", pexpect.EOF]
            )
            return res == 1

    def disconnect(self, mac_address):
        """Try to disconnect to a device by mac address."""
        try:
            self.send(f"disconnect {mac_address}", 2)
        except Exception as e:
            logger.error(e)
            return False
        else:
            res = self.process.expect(
                ["Failed to disconnect", "Successful disconnected", pexpect.EOF]
            )
            return res == 1

    def is_paired_with_headset(self):
        """Returns true if headset is paired (not connected)"""
        try:
            paired_devices = self.get_paired_devices()
            if len(paired_devices) > 0:
                contains = False
                for paired_device in paired_devices:
                    if paired_device['name'] == bose_headset['name'] or paired_device['mac_address'] == bose_headset['mac_address']:
                        contains = True
                        logger.info("Bose headset paired")
                        return True
                if not contains:
                    logger.info("Only other devices paired")
                    return False
            else:
                logger.info("No device paired")
                return False
        except Exception as e:
            logger.error(e)
            return False

    def is_connected_with_headset(self):
        """Returns true if headset is connected"""
        try:
            device_info = self.get_device_info(bose_headset['mac_address'])
            if "\tConnected: yes" in device_info:
                logger.info("Bose headset connected")
                return True
            else:
                logger.info("Bose headset not connected")
                return False
        except Exception as e:
            logger.error(e)
            return False
