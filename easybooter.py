#usage: python3 easybooter.py

import sys
import os
import re,subprocess,random

colors = ["\033[1;32;40m","\033[1;30;40m","\033[1;31;40m","\033[1;33;40m","\033[1;34;40m","\033[1;35;40m","\033[1;36;40m","\033[1;37;40m"]
colors2 = ["\033[1;32;40m","\033[1;30;40m","\033[1;31;40m","\033[1;33;40m","\033[1;34;40m","\033[1;35;40m","\033[1;36;40m","\033[1;37;40m"]

def intro():
    print(random.choice(colors))
    print(" *--------------------------------------------------------------------------------------*")
    print(" | _______ _______ _______ __   __      ______   _____   _____  _______ _______  ______ |")
    print(" | |______ |_____| |______   \_/        |_____] |     | |     |    |    |______ |_____/ |")
    print(" | |______ |     | ______|    |         |_____] |_____| |_____|    |    |______ |    \_ |")
    print(" *--------------------------------------------------------------------------------------*")
    print(random.choice(colors2))
    print("     https://github.com/Virgula0/OsxEasyBooter      Create Bootable Usb for Osx  ")
    print("\033[0m")
    

def process(read , input_iso):
    mount_point = os.popen("diskutil info \""+read+"\" |grep \"Part of Whole\" |awk -F \":\" '{print $2}' |tr -d ' '").read()
    if mount_point:
        print("\033[1;32;48m[*] Found mount point for this device /dev/"+mount_point+"Proceeding...")
        os.popen("rm ./temporary_of_easy_booter.img &> /dev/null")
        os.popen("rm ./temporary_of_easy_booter.img.dmg &> /dev/null")
        convert_result = os.popen("hdiutil convert -format UDRW -o ./temporary_of_easy_booter.img "+input_iso+" |grep created |awk -F \":\" '{print $2}' |sed '/^$/d'").read()
        convert_result = convert_result.lstrip()
        print ("\033[0m[INFO] Temporary image file created at "+convert_result)
        print("\033[0m[INFO] Unmounting disk...")
        unmount_disk = os.popen("diskutil unmountDisk /dev/"+mount_point).read()
        print ("\033[94m[INFO] "+unmount_disk)
        print("\033[1;32;48m[*] Making bootable USB, please wait...")
        try:
            copy_files = subprocess.check_output(["sudo","dd", "if="+convert_result.rstrip("\n\r"),"of=/dev/r"+mount_point.rstrip("\n\r"),"bs=1m"]).decode(errors='ignore')
            #copy_files = os.popen("sudo dd if="+convert_result+" of=/dev/r"+mount_point+" bs=1m").read().decode(errors='ignore') This one is not supported by diskutil
        except subprocess.CalledProcessError as e:
            print("\033[1;31;48m[!] An error occurred: "+e.Message())       
        print("\033[0m[INFO] Ejecting disk...")
        eject_disk = os.popen("diskutil eject /dev/"+mount_point).read()
        print("\033[0m[INFO] Deleting temporary image...")
        os.popen("rm ./temporary_of_easy_booter.img &> /dev/null")
        os.popen("rm ./temporary_of_easy_booter.img.dmg &> /dev/null")
        print("\033[1;32;48m[*] Done.")
    else:
        print("\033[1;31;48m[!] Unexpected error, no mount point found for "+read)
        sys.exit(1)                        
    

def proceed(input_device , input_iso):
    answer = input("\033[1;33;40m[?] Are you sure you want proceed? All datas on USB will be erased(y/n) =>\033[0m")
    if answer == "yes" or answer == "y" or answer == "Y":
        process(input_device, input_iso)
    else:
        print ("\033[93mBye, See you!")
        sys.exit(1)

def main():
    check = os.getuid()
    os.system("clear")
    intro()
    if check != 0:
        print("\033[1;31;48m[!] This script must run as root!")
        sys.exit(1)
    clear = os.popen("clear")
    #devices = os.popen("ioreg -p IOUSB -w0 | sed 's/[^o]*o //; s/@.*$//' | grep -v '^Root.*'|grep -iv facetime |grep -iv apple |grep -iv iousb |sed '/Hub/d' |grep -iv controller |grep -iv mouse |sed '/^$/d' |tr -d '0-9'").read()
    devices = os.popen("ls -l /Volumes |grep -iv \"macintosh\" |awk -F \":\" '{print $2}'|tr -d '0-9'").read()
    devices_formatted = os.linesep.join([s for s in devices.splitlines() if s])
    if devices_formatted == "":
        print("\033[1;31;48m[!] No external devices found... if not, please open an issue on github project")
        sys.exit(1)
    else:
        print("\n\033[1;32;48m[INFO] External devices found: \033[0m\n"+devices_formatted+"\n")
        input_device = input("\033[1;33;40m[?] Which device you want to make bootable?\033[0m ")
    while input_device not in devices_formatted:
        print ("\033[1;31;48m[!] Device not found try again")
        input_device = input("\033[1;33;40m[?] Which device you want to make bootable?\033[0m ")
        if input_device in devices_formatted:
            break
    input_iso = input("\033[1;33;40m[?] Insert path of your iso or drag and drop it here =>\033[0m ")
    input_iso = input_iso.replace("\\","")
    while input_iso == "" or input_iso == " " or not os.path.isfile(input_iso):
        if input_iso == "" or input_iso == " ":
            print ("\033[1;31;48m[!] Insert your iso location")
        elif not os.path.isfile(input_iso):
            print ("\033[1;31;48m[!] File not found")
        else:
            print("\033[1;32;48m[*] Done")
            break
        input_iso = input("\033[1;33;40m[?] Insert path of your iso or drag and drop it here =>\033[0m ")
    input_iso = input_iso.replace("\\","")
    if input_iso.endswith(".iso"):
        proceed(input_device , input_iso)
    else:
        print("\033[1;31;48m[!] Extension not valid! Must be an iso!")        
    sys.exit(1)

os.system("mode con cols=50")
main()
print("\033[0m")
