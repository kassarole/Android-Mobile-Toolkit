#amt.py
"""
Code to interact with an android device using ADB
Written by Kevin Rode
Last Updated Sep 27 2019
"""
import adbutils
import os
import re
import requests
from lxml import html
def adb_start():
    if "platform-tools" in os.environ['PATH']:
        print("ADB found in PATH")
    else:
        os.environ['PATH'] += ';'+os.getcwd()+'\\platform-tools'


def adb_connect():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    print(adb.device_list())
    d = adb.device()
    return d


def twrp_download(d):
    cpu = d.shell('cat /proc/cpuinfo | grep Hardware')
    cpu = cpu.replace(" ","")
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


def main():
    adb_start()
    device = adb_connect()
    twrp_download(device)


main()
