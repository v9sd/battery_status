#!/bin/python3

import pyudev 
import re

class BatteryParseSettings:
    def __init__(self):
        self.type_property_name;

class BatteryStatus:
    PROPERTY_TYPE="POWER_SUPPLY_TYPE"
    PROPERTY_CHARGE_FULL="POWER_SUPPLY_CHARGE_FULL"
    PROPERTY_CHARGE_NOW="POWER_SUPPLY_CHARGE_NOW"
    def __init__(self):
        context = pyudev.Context()
        self.device = None
        self.charge_full = None
        self.charge_now = None
        for device in context.list_devices(subsystem="power_supply"):
            dev_properties = device.properties
            if dev_properties is None:
                continue
            dev_property_type =  dev_properties[self.PROPERTY_TYPE]
            if dev_property_type is None or dev_property_type != "Battery":
                continue
            dev_property_charge_full=dev_properties[self.PROPERTY_CHARGE_FULL]
            if dev_property_charge_full is None:
                continue
            dev_property_charge_now=dev_properties[self.PROPERTY_CHARGE_NOW]
            if dev_property_charge_now is None:
                continue
            self.device = device
            self.charge_now = int(dev_property_charge_now)
            self.charge_full = int(dev_property_charge_full)
            break

    @property
    def percent(self):
        return int(self.charge_now / self.charge_full * 100)




def main():
    battery = BatteryStatus()
    print("{}%".format(battery.percent))

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
        for dev_properties_key in dev_properties:
            print("{}={}".format(dev_properties_key, dev_properties[dev_properties_key]))
            #print(dev_properties.asint(0))
            #print(dev_properties_key)
            #print(dev_attributes.get(dev_properties_key))
            
            #print("{}={}".format(dev_properties_key, dev_properties_val))
        #print(dev_properties.keys())
        #print("\tproperties amount={}".format(dev_properties.))

main()
