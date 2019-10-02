import adbutils
from helpers import root
import os
import sys


def recovery_boot():
    adb = "platform-tools\\adb.exe"
    adbcheck = os.popen(adb+" devices").read()
    if "recovery" in adbcheck:
        pass
    else:
        device = root.adb_connect()
        root.twrp_download(device)
        root.push_files(device)
        root.reboot_bootloader()
        adb = "platform-tools\\adb.exe"
        fastboot = "platform-tools\\fastboot.exe"
        files = os.listdir(os.curdir)
        for file in files:
            if "twrp" in file:
                twrp = file
            os.system(fastboot + " boot "+twrp)
            input("Press Enter when TWRP has booted")


def list_apps():
    adb = "platform-tools\\adb.exe"
    apps = os.popen(adb+" shell (ls /data/data)").read()
    app_array = apps.split("\n")
    for i in app_array:
        print(i)


def download_app(o=None):
    app = input("Please enter the name of the app you would like to download: ")
    adb = "platform-tools\\adb.exe"
    os.system(adb+" shell (cp -R /data/data/"+app+" /sdcard/"+app+")")
    if o == None:
        output = input("Please enter the output directory for the app files. Leave blank to download to current directory: ")
        if output != None:
            os.makedirs(output)
            os.system(adb+" pull /sdcard/"+app+" "+output)
        else:
            os.system(adb+" pull /sdcard/"+app)
    else:
        os.makedirs(o)
        os.system(adb+" pull /sdcard/"+app+" "+o)


def app_extract(output=None):
    recovery_boot()
    list_apps()
    download_app(output)


def extract_menu():
    while True:
        print("How would you like to extract data")
        print("[1] App extraction\n[2] Whole Phone Extraction (via Android Backup)(COMING SOON)\n[3] Whole Phone Extraction (via adb shell)(COMING SOON)\n[99] Main Menu")
        choice = input()
        if int(choice) == 1:
            app_extract()
        elif int(choice) == 2:
            print()
        elif int(choice) == 3:
            print()
        elif int(choice) == 99:
            break
