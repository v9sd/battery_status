#!/bin/python3

import pyudev 
import math
import re
import argparse
import colorama

class BatteryParseSettings:
    def __init__(self):
        self.name_property_type

class BatteryStatus:

    @staticmethod
    def _check_init_args(args):
        result = hasattr(args, "subsystem_value")
        result = result and type(args.subsystem_value) is str

        result = result and hasattr(args, "type_name")
        result = result and type(args.type_name) is str

        result = result and hasattr(args, "type_value")
        result = result and type(args.type_value) is str

        result = result and hasattr(args, "charge_full_name")
        result = result and type(args.charge_full_name) is str

        result = result and hasattr(args, "charge_now_name")
        result = result and type(args.charge_now_name) is str
        return result

    def __init__(self, args):
        context = pyudev.Context()
        self.device = None
        self.charge_full = None
        self.charge_now = None
        for device in context.list_devices(subsystem=args.subsystem_value):
            dev_property_charge_full=None
            dev_property_charge_now=None
            dev_properties = device.properties
            if dev_properties is None:
                continue
            dev_property_type =  dev_properties[args.type_name]
            if dev_property_type is None or dev_property_type != args.type_value:
                continue

            for charge_full_name_item in args.charge_full_name:
                try:
                    dev_property_charge_full=dev_properties[charge_full_name_item]
                except KeyError:
                    continue
                if dev_property_charge_full is None:
                    continue

            for charge_now_name_item in args.charge_now_name:
                try:
                    dev_property_charge_now=dev_properties[charge_now_name_item]
                except KeyError:
                    continue
                if dev_property_charge_now is None:
                    continue

            if (dev_property_charge_full is not None) and (dev_property_charge_now is not None):
                self.device = device
                self.charge_now = int(dev_property_charge_now)
                self.charge_full = int(dev_property_charge_full)
                break

    @property
    def percent(self):
        if self.charge_now is None or self.charge_full is None:
            return math.nan
        return int(self.charge_now / self.charge_full * 100)


def argument_parse():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--subsystem-value", 
            default="power_supply",
            type=str,
            nargs=1)

    arg_parser.add_argument("--type-name", 
            default="POWER_SUPPLY_TYPE",
            type=str,
            nargs=1)

    arg_parser.add_argument("--type-value", 
            default="Battery",
            type=str,
            nargs=1)

    arg_parser.add_argument("--charge-full-name", 
            default="POWER_SUPPLY_CHARGE_FULL",
            type=str,
            nargs=1)

    arg_parser.add_argument("--charge-now-name", 
            default="POWER_SUPPLY_CHARGE_NOW",
            type=str,
            nargs=1)
    return arg_parser.parse_args()


def main():
    args = argument_parse()
    battery = BatteryStatus(args)
    percent = battery.percent
    if percent is math.nan:
        percent = "!"
    else:
        percent = "{}%".format(percent)

    colorama.init()
    print(colorama.Fore.RED + percent + colorama.Fore.RESET)

def DebugInfo():
    context = pyudev.Context()
    #hwmod
    for device in context.list_devices(subsystem="power_supply"):
        print(device.device_path)
        print(device.subsystem)
        print("path={}".format(device.device_path))
        print("type={}".format(device.device_type))
        print("type={}".format(device.device_node))
        dev_properties = device.properties
        dev_attributes = device.attributes
        print(type(dev_properties))
        print(type(dev_attributes.available_attributes))
        print("Properties:")
        for dev_properties_key in dev_properties:
            print("\t{}={}".format(dev_properties_key, dev_properties[dev_properties_key]))
            #print(dev_properties.asint(0))
            #print(dev_properties_key)
            #print(dev_attributes.get(dev_properties_key))
            
            #print("{}={}".format(dev_properties_key, dev_properties_val))
        #print(dev_properties.keys())
        #print("\tproperties amount={}".format(dev_properties.))

#DebugInfo()


main()
