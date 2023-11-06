import xmltodict
import dotmap

with open('/home/dj/PycharmProjects/WLAN/ListDB-01.kismet.netxml', 'r') as file:
    raw_data = file.read()

xmla = xmltodict.parse(raw_data)
dotmap_data = dotmap.DotMap(xmla)

wireless_networks = len(xmla["detection-run"]["wireless-network"])
networks = dotmap_data["detection-run"]["wireless-network"]

network_info = ['ESSID', 'BSSID', 'Enc', 'Cipher', 'Auth', '2.4GHz or 5GHz', 'Channel', 'PWR', 'Beacons']

dict = {
    1: ["SSID", "essid"],
    2: ["BSSID"],
    3: ["SSID", "encryption"],
    4: ["SSID", "encryption"],
    5: ["encoding"],
    6: ["freqmhz"],
    7: ["channel"],
    8: ["snr-info", "last_signal_dbm"],
    9: ["SSID", "beaconrate"]
}
RESULT = []
for i in range(wireless_networks): #1
    if networks[i]['@type'] == 'probe':
        continue
    results2 = {
        'ESSID': 'Your ESSID Value',
        'BSSID': 'Your BSSID Value',
        'Enc': 'Your Encryption Type',
        'Cipher': 'Your Cipher Type',
        'Auth': 'Your Authentication Type',
        '2.4GHz or 5GHz': 'Your Frequency',
        'Channel': 'Your Channel Number',
        'PWR': 'Your Power Value',
        'Beacons': 'Your Beacons Value'
    }
    x=0
    for each in dict.values():

        current_level = networks[i]
        for index in each:#indices
            try:
                current_level = current_level[index]
            except IndexError:
                print("Index out of range")
                break

        try:
            current_level = current_level.get('#text')
        except:
            pass
        if x==2 or x==3: #Skip the encryption
            x+=1
            continue

        if isinstance(current_level, list):
            results2[network_info[x]] = current_level
            x+=1

        else:
            results2[network_info[x]] = current_level
            x+=1
    DATA = {i:results2}
    RESULT.append(DATA)

print(RESULT)


