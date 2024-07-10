from tkinter import *
from tkinter.ttk import *
import re
import os
import time
import threading
import coms


arpFile = "arp.txt"
#arpFile = "/proc/net/arp"
devNameFile = "devices.txt"
debug = False

devices = dict()
mutes = dict()
defeans = dict()
privateCom = dict()
privateMute = dict()

def setupNetwork():
    os.system("sudo systemctl start NetworkManager")
    time.sleep(3)
    os.system("sudo nmcli device wifi hotspot ssid 'raspWIFI' password 'raspwifi'")

def muteDevices():
    for val in mutes:
        if mutes[val] == 0:
            os.system(f"sudo iptables -D INPUT -i wlan0 -s {val} -p tcp --dport 6420 -j DROP")
        elif mutes[val] == 1:
            os.system(f"sudo iptables -A INPUT -i wlan0 -s {val} -p tcp --dport 6420 -j DROP")
    
def printBroadList(frm):
    count = 2

    for dev in devices:
        mutes[dev] = IntVar()
        defeans[dev] = IntVar()
        Label(frm, text=devices[dev]).grid(column=0, row=count, columnspan=2)
        Checkbutton(frm, variable=mutes[dev], command=lambda:muteDevices()).grid(column=2, row=count)
        Checkbutton(frm, variable=defeans[dev]).grid(column=3, row=count)
        count += 1
    
    return count

def printPrivList(frm):
    row = 2
    col = 2

    for dev in devices:
        Label(frm, text=devices[dev]).grid(column=col, row=1)
        col += 1

    col = 2
    for dev in devices:
        Label(frm, text=devices[dev]).grid(column=0, row=row, columnspan=2)
        privateCom[dev] = dict()
        
        for tag in devices:
            privateCom[dev][tag] = IntVar()
            Checkbutton(frm, variable=privateCom[dev][tag]).grid(column=col, row=row)
            col += 1

        col = 2
        row += 1
    
    return row

def updateDevices(frm, mode):
    devIP = dict()
    f = open(arpFile, "r")

    f.readline()
    for line in f:
        ip = re.search("(\\b25[0-5]|\\b2[0-4][0-9]|\\b[01]?[0-9][0-9]?)(\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}", line)
        mac = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
        devIP[mac[0]] = ip[0]
    f.close()

    if debug: print(devIP)

    f = open(devNameFile, "r")
    for line in f:
        mac = re.search("([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", line)
        if devIP.get(mac[0]):
            name = re.search("\t(.+)$", line)
            devices[devIP[mac[0]]] = name[0][1:]
    f.close()

    if debug: print(devices)

    for mac in devIP:
        if not devices.get(devIP[mac]):
            devices[devIP[mac]] = "Unknown"
    devIP.clear()

    print(devices)

    if mode == "BROAD":
        return printBroadList(frm)
    elif mode == "PRIV":
        return printPrivList(frm)
    
    return 2
    

def bradcastWindow(tab1, root):
    frm = Frame(tab1, padding=20)
    frm.grid(column=0,row=0)
    
    Label(frm, text="Mute").grid(column=2, row=1)
    Label(frm, text="Defean").grid(column=3, row=1)

    lastRow = updateDevices(frm, "BROAD")

    Button(frm, text="Refresh", command=lambda:updateDevices(frm, "BROAD")).grid(column=0, row=lastRow+1, columnspan=2)
    Button(frm, text="Quit", command=root.destroy).grid(column=6, row=lastRow+1, columnspan=2)

def privateWindow(tab2, root):
    frm = Frame(tab2, padding=20)
    frm.grid(column=0,row=0)
    
    lastRow = updateDevices(frm, "PRIV")

    Button(frm, text="Refresh", command=lambda:updateDevices(frm, "PRIV")).grid(column=0, row=lastRow, columnspan=2)
    Button(frm, text="Quit", command=root.destroy).grid(column=6, row=lastRow, columnspan=2)

if __name__ == "__main__":
    setupNetwork()
    server_handler = threading.Thread(target=coms.start_server, args=(coms.HOST, coms.PORT))

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

    server_handler.start()
    root.mainloop()


