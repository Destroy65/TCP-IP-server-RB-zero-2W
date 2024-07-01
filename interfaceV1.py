from tkinter import *
from tkinter.ttk import *
import re
import os
import time

arpFile = "arp.txt"
#arpFile = "/proc/net/arp"
devNameFile = "devices.txt"
debug = True

devices = dict()
mutes = dict()
defeans = dict()

def setupNetwork():
    os.system("sudo systemctl start NetworkManager")
    time.sleep(5)
    os.system("sudo nmcli device wifi hotspot ssid 'raspWIFI' password 'raspwifi'")
    

def updateDevices(frm):
    devIP = dict()
    f = open(arpFile, "r")
    f.readline()
    for line in f:
        ip = re.search("(\\b25[0-5]|\\b2[0-4][0-9]|\\b[01]?[0-9][0-9]?)(\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}", line)
        mac = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
        devIP[mac[0]] = ip[0]
    f.close()

    if(debug): print(devIP)

    f = open(devNameFile, "r")
    for line in f:
        mac = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
        if devIP.get(mac[0]):
            name = re.search("\t(.+)$", line)
            devices[devIP[mac[0]]] = name[0]
    f.close()
    if(debug): print(devices)

    for mac in devIP:
        if not devices.get(devIP[mac]):
            devices[devIP[mac]] = "Unknown"
    devIP.clear()

    print(devices)

    count = 2
    for dev in devices:
        mutes[dev] = IntVar()
        defeans[dev] = IntVar()
        Label(frm, text=devices[dev]).grid(column=0, row=count, columnspan=2)
        Checkbutton(frm, variable=mutes[dev]).grid(column=2, row=count)
        Checkbutton(frm, variable=defeans[dev]).grid(column=3, row=count)
        count += 1
    
    return count

def bradcastWindow(tab1, root):
    frm = Frame(tab1, padding=20)
    frm.grid(column=0,row=0)
    
    Label(frm, text="Mute").grid(column=2, row=1)
    Label(frm, text="Defean").grid(column=3, row=1)
    lastRow = updateDevices(frm)

    Button(frm, text="Refresh", command=lambda:updateDevices(frm)).grid(column=0, row=lastRow+1, columnspan=2)
    Button(frm, text="Quit", command=root.destroy).grid(column=6, row=lastRow+1, columnspan=2)

def privateWindow(tab2, root):
    frm = Frame(tab2, padding=20)
    frm.grid(column=0,row=0)
    
    Label(frm, text="Mute").grid(column=2, row=1)
    Label(frm, text="Walkie-1").grid(column=3, row=1)
    Label(frm, text="Walkie-2").grid(column=4, row=1)
    Label(frm, text="Walkie-3").grid(column=5, row=1)

    Label(frm, text="Walkie-1").grid(column=0, row=2)
    Checkbutton(frm, variable=IntVar()).grid(column=2, row=2)
    Checkbutton(frm, variable=IntVar(),state="disabled").grid(column=3, row=2)
    Checkbutton(frm, variable=IntVar()).grid(column=4, row=2)
    Checkbutton(frm, variable=IntVar()).grid(column=5, row=2)

    Label(frm, text="Walkie-2").grid(column=0, row=3)
    Checkbutton(frm, variable=IntVar()).grid(column=2, row=3)
    Checkbutton(frm, variable=IntVar()).grid(column=3, row=3)
    Checkbutton(frm, variable=0,state="disabled").grid(column=4, row=3)
    Checkbutton(frm, variable=IntVar()).grid(column=5, row=3)

    Label(frm, text="Walkie-3").grid(column=0, row=4)
    Checkbutton(frm, variable=IntVar()).grid(column=2, row=4)
    Checkbutton(frm, variable=IntVar(),state="disabled").grid(column=3, row=4)
    Checkbutton(frm, variable=IntVar(),state="disabled").grid(column=4, row=4)
    Checkbutton(frm, variable=IntVar(),state="disabled").grid(column=5, row=4)

    

    Button(frm, text="Refresh", command=lambda:updateDevices(frm)).grid(column=0, row=6, columnspan=2)
    Button(frm, text="Quit", command=root.destroy).grid(column=6, row=6, columnspan=2)

def main():
    setupNetwork()
    root = Tk()
    root.title("Comunication Control")
    root.minsize(400,200)
    
    
    tab_control = Notebook(root)

    tab1 = Frame(tab_control)
    tab2 = Frame(tab_control)

    tab_control.add(tab1, text='Broadcast Channel')
    tab_control.add(tab2, text='1 to 1')

    bradcastWindow(tab1, root)
    privateWindow(tab2, root)
    
    tab_control.pack(expand=1, fill='both')
    root.mainloop()

main()
