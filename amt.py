# amt.py
"""
Code to interact with an android device using ADB
Written by Kevin Rode
Last Updated Sep 28 2019
"""
import sys
from helpers import root
from helpers import extract


def menu():
    while True:
        print("[1] Root Device\n[2] Check root\n[3] Extract Data (WIP)\n[99] Quit")
        choice = input("Please select a number: ")
        if int(choice) == 1:
            root.root_device()
        elif int(choice) == 2:
            root.root_check()
        elif int(choice) == 3:
            extract.extract_menu()
        elif int(choice) == 99:
            print("Goodbye!")
            sys.exit()
        else:
            print("Unknown input")

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
    print(" --check-root    : checks if the device is rooted")
    print(" -Ae             : Extract data in app extract mode. Add -o to specify an output directory")
    print(" --help          : print this message")
    print(" -h              : alias for --help")


def main():
    if "--interactive" in sys.argv[1:] or "-i" in sys.argv[1:]:
        root.adb_start()
        menu()
    elif "--root" in sys.argv[1:] or "-r" in sys.argv[1:]:
        root.root_device()
    elif "--help" in sys.argv[1:] or "-h" in sys.argv[1:]:
        show_help()
    elif "--check-root" in sys.argv[1:]:
        root.root_check()
    elif "-Ae" in sys.argv[1:]:
        if "-o" in sys.argv[1:]:
            output_index = sys.argv.index("-o")
            output = sys.argv[output_index+1]
            extract.app_extract(output)
        else:
            extract.app_extract()
    else:
        show_help()


main()
