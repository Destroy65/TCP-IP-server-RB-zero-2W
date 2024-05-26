#!/bin/bash

sudo systemctl start NetworkManager

wait 2000

sudo nmcli device wifi hotspot ssid "raspWIFI" password "raspwifi"

