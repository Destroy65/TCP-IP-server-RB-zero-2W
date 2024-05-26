from tkinter import *
from tkinter import ttk
import re

#arpFile = "arp.txt"
arpFile = "/proc/net/arp"
devNameFile = "devices.txt"


def updateDevices(devices):
    devIP = dict()
    f = open(arpFile, "r")
    f.readline()
    for line in f:
        print(line)
        ip = re.search("(\\b25[0-5]|\\b2[0-4][0-9]|\\b[01]?[0-9][0-9]?)(\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}", line)
        mac = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
        print(ip)
        print(mac)
        devIP[mac[0]] = ip[0]
    f.close()

    print(devIP)

    f = open(devNameFile, "r")
    for line in f:
        mac = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
        if devIP.get(mac[0]):
            name = re.findall("\t(.+)$", line)
            devices[devIP[mac[0]]] = name[0]
    f.close()
    print(devices)

    for mac in devIP:
        if not devices.get(devIP[mac]):
            devices[devIP[mac]] = "Unknown"
    devIP.clear()

    print(devices)
    



def main():
    devices = dict()
    mutes = dict()
    defeans = dict()
    root = Tk()
    root.title("Comunication Control")
    root.minsize(400,200)
    frm = ttk.Frame(root, padding=20)
    frm.grid(column=0,row=0, columnspan=3,rowspan=5)
    updateDevices(devices)
    
    ttk.Label(frm, text="Broadcast Channel").grid(column=0, row=0, columnspan=3)
    ttk.Label(frm, text="Mute").grid(column=1, row=1)
    ttk.Label(frm, text="Defean").grid(column=2, row=1)
    count = 2
    for dev in devices:
        mutes[dev] = IntVar()
        defeans[dev] = IntVar()
        ttk.Label(frm, text=devices[dev]).grid(column=0, row=count)
        ttk.Checkbutton(frm, variable=mutes[dev]).grid(column=1, row=count)
        ttk.Checkbutton(frm, variable=defeans[dev]).grid(column=2, row=count)
        count += 1
    frm2 = ttk.Frame(root, padding=20)
    frm2.grid(column=3,row=0, columnspan=2, rowspan=4)
    private_d1_mute = IntVar()
    private_d2_mute = IntVar()
    ttk.Label(frm2, text="Private Channel 1").grid(column=6,row=0, columnspan=2)
    ttk.Label(frm2, text="Mute").grid(column=7, row=1)
    ttk.Label(frm2, text="Device 1").grid(column=6, row=2)
    ttk.Checkbutton(frm2, variable=private_d1_mute).grid(column=7, row=2)
    ttk.Label(frm2, text="Device 2").grid(column=6, row=3)
    ttk.Checkbutton(frm2, variable=private_d2_mute).grid(column=7, row=3)
    frm3 = ttk.Frame(root, padding=10)
    frm3.grid(column=6,row=5, columnspan=2)
    ttk.Button(frm3, text="Quit", command=root.destroy).grid(column=6, row=5, columnspan=2)
    root.mainloop()

main()
