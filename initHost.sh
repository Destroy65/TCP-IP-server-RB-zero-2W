#!/bin/bash

sudo systemctl start NetworkManager

wait

sudo nmcli device wifi hotspot ssid "raspWIFI" password "raspwifi"

