import os
import subprocess
import signal

import asyncio


def Pre_sets(Device):
    os.system(f'sudo airmon-ng start {Device}')#sudo iwconfig {Device} power on &&



async def Listener(stop_event, Mon_Device):
    print('Listener started')

    process = await asyncio.create_subprocess_shell(
        f'sudo airodump-ng {Mon_Device} --band abg --write-interval 1 --write ListDB --output-format netxml'
    )
    print(process.pid)

async def Listener2(stop_event, Mon_Device, Focused_Network):
    print('Listener started2')

    process = await asyncio.create_subprocess_shell(
        f'sudo airodump-ng {Mon_Device} --bssid {Focused_Network} --write-interval 1 --write DEVICESDB --output-format netxml'
    )
    print(process.pid)


async def Stop_Listener():
    FileName_Networks='ListDB-01.kismet.netxml'
    FileName_Devices='DEVICESDB-01.kismet.netxml'
    print('Listener Stopped')
    output = subprocess.check_output(['ps', 'aux'], text=True)

    # Split the output into lines
    lines = output.split('\n')

    # Iterate through the lines and check for the desired process
    for line in lines:
        if 'S+' in line and '/bin/sh -c sudo airodump-ng wlan0mon' in line:
            pass #Wrong PID

        elif 'S+' in line and 'sudo airodump-ng wlan0mon' in line:
            print("Process is running:", line)
            PID = line.split()[1]
            print(PID)
            os.kill(int(PID), signal.SIGTERM)

        else:
            pass
    try:
        os.system(f'sudo rm {FileName_Networks}')
    except:
        pass
    try:
        os.system(f'sudo rm {FileName_Devices}')
    except:
        pass

data = [{0: {'ESSID': 'Verizon_6ZP4G4', 'BSSID': '78:67:0E:4C:4D:A9', 'Enc': 'Your Encryption Type', 'Cipher': 'Your Cipher Type', 'Auth': 'CCK', '2.4GHz or 5GHz': '2412 3', 'Channel': '1', 'PWR': '-52', 'Beacons': '10'}}, {1: {'ESSID': 'Uki_AP_2G', 'BSSID': '04:92:26:60:C7:30', 'Enc': 'Your Encryption Type', 'Cipher': 'Your Cipher Type', 'Auth': 'CCK', '2.4GHz or 5GHz': '2412 3', 'Channel': '1', 'PWR': '-17', 'Beacons': '10'}}, {2: {'ESSID': 'JUPITER', 'BSSID': 'A4:CF:D2:02:F0:F8', 'Enc': 'Your Encryption Type', 'Cipher': 'Your Cipher Type', 'Auth': 'CCK', '2.4GHz or 5GHz': '2412 2', 'Channel': '1', 'PWR': '-56', 'Beacons': '10'}}, {3: {'ESSID': 'MyAltice aac4ed', 'BSSID': '0C:B9:37:AA:C4:F0', 'Enc': 'Your Encryption Type', 'Cipher': 'Your Cipher Type', 'Auth': 'CCK', '2.4GHz or 5GHz': '2412 2', 'Channel': '1', 'PWR': '-79', 'Beacons': '10'}}]



network_info = ['ESSID', 'BSSID', 'Enc', 'Cipher', 'Auth', '2.4GHz or 5GHz', 'Channel', 'PWR', 'Beacons']

