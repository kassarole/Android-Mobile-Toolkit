# amt.py
"""
Code to interact with an android device using ADB
Written by Kevin Rode
Last Updated Sep 28 2019
"""
import adbutils
import os
import sys
import re
import time
import requests
from lxml import html


def adb_start():
    if "platform-tools" in os.environ['PATH']:
        print("ADB found in PATH")
    else:
        os.environ['PATH'] += ';'+os.getcwd()+'\\platform-tools'


def adb_connect():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    d = adb.device()
    if d != None:
        print("Device connected.")
    return d


def twrp_download(d):
    found = 0
    files = os.listdir(os.curdir)
    for file in files:
        if "twrp" in file:
            found = 1
    if found != 1:
        cpu = d.shell('cat /proc/cpuinfo | grep Hardware')
        cpu = cpu.replace(" ", "")
        cpu = re.sub(r'(.+:)', '', cpu)
        r = requests.get('https://dl.twrp.me/'+cpu)
        tree = html.fromstring(r.text)
        urls = tree.xpath('//a/@href')
        downloads = []
        for i in urls:
            if "img" in i:
                downloads.append(i)
        url_to_download = "https://dl.twrp.me"+downloads[0]
        url_to_download = url_to_download.replace('.html', '')
        print("Use this link to download twrp for your connected device: "+url_to_download)
        print("Ensure that the downloaded file is moved to the same folder as the script before continuing")
        input("Press Enter to continue...")
        files = os.listdir(os.curdir)
        for file in files:
            if "twrp" in file:
                found = 1
        while found != 1:
            print("File not found. Please confirm it has been moved to the correct directory")
            input("Press Enter to continue...")
            files = os.listdir(os.curdir)
            for file in files:
                if "twrp" in file:
                    found = 1
    else:
        print("twrp already downloaded")


def push_files(d):
    initcheck_magisk = d.shell("cd /sdcard && ls | grep Magisk")
    if initcheck_magisk == None and initcheck_twrp == None:
        d.sync.push("Magisk-v19.3.zip", "/sdcard/Magisk.zip")
        check_magisk = d.shell("cd /sdcard && ls | grep Magisk")
        if check != None:
            print("File copied successfully.")
        else:
            print("Something went wrong. Please try again.")
    else:
        print("Magisk already copied")


def reboot_bootloader():
    adb = "platform-tools\\adb.exe"
    fastboot = "platform-tools\\fastboot.exe"
    os.system(adb+" reboot bootloader")
    input("Press Enter when the device has rebooted")
    os.system(fastboot+" devices")


def root_device():
    adb = "platform-tools\\adb.exe"
    fastboot = "platform-tools\\fastboot.exe"
    files = os.listdir(os.curdir)
    for file in files:
        if "twrp" in file:
            twrp = file
    os.system(fastboot + " boot "+twrp)
    input("Press Enter when TWRP has booted")
    print("Follow the onscreen directions to install Magisk (Located at the bottom of the install window)")
    print("After Magisk installs click [Reboot] then [Do Not Install]")
    input("Press Enter when the device has rebooted")


def menu():
    while True:
        print("[1] Root Device (WIP)\n[2] Extract Data (Coming Soon)\n[99] Quit")
        choice = input("Please select a number: ")
        if int(choice) == 1:
            device = adb_connect()
            twrp_download(device)
            push_files(device)
            reboot_bootloader()
            root_device()
        elif int(choice) == 2:
            print("Data extraction is coming soon.")
            time.sleep(2)
        elif int(choice) == 99:
            print("Goodbye!")
            sys.exit()


def show_help():
    print("Android Mobile Toolkit v1.1")
    print("Written by Kevin Rode (kevroded)")
    print()
    print("Run with amt.exe [options]")
    print()
    print("OPTIONS:")
    print(" --interactive   : start the utility in a mode with a menu for the user to select options on")
    print(" -i              : alias for --interactive")
    print(" --root          : root a connected Android device")
    print(" -r              : alias for --root")
    print(" --help          : print this message")
    print(" -h              : alias for --help")


def main():
    if "--interactive" in sys.argv[1:] or "-i" in sys.argv[1:]:
        adb_start()
        menu()
    elif "--root" in sys.argv[1:] or "-r" in sys.argv[1:]:
        device = adb_connect()
        twrp_download(device)
        push_files(device)
        reboot_bootloader()
        root_device()
    elif "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        show_help()
    else:
        show_help()


main()
