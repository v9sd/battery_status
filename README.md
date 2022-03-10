# battery_status
Python script for get battery percent charging status from udev

usage: battery_status.py [-h] [--subsystem-value SUBSYSTEM_VALUE]
                         [--type-name TYPE_NAME] [--type-value TYPE_VALUE]
                         [--charge-full-name CHARGE_FULL_NAME]
                         [--charge-now-name CHARGE_NOW_NAME]

optional arguments:
  -h, --help            show this help message and exit
  --subsystem-value SUBSYSTEM_VALUE (default power_supply)
  --type-name TYPE_NAME (default POWER_SUPPLY_TYPE)
  --type-value TYPE_VALUE (default Battery)
  --charge-full-name CHARGE_FULL_NAME (default POWER_SUPPLY_CHARGE_FULL)
  --charge-now-name CHARGE_NOW_NAME (default POWER_SUPPLY_CHARGE_NOW)

Example of using:
battery_status.py  --charge-full-name POWER_SUPPLY_ENERGY_FULL --charge-now-name POWER_SUPPLY_ENERGY_NOW
