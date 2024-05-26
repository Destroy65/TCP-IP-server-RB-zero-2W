#!/bin/bash

sudo systemctl start NetworkManager

sudo nmcli device wifi hotspot ssid "raspWIFI" password "raspwifi"

