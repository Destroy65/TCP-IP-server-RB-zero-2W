#!/bin/bash

sudo nmcli device disconnect wlan0

sudo nmcli connection up MIWIFI_2G_HXTi --ask
