import csv

network_info = ['ESSID', 'BSSID', 'Enc', 'Cipher', 'Auth', '2.4GHz or 5GHz', 'Channel', 'PWR', 'Beacons']


f = open('/home/dj/PycharmProjects/WLAN/ListDB-02.csv',encoding='UTF8')
csv_reader = csv.reader(f)

RESULT = []
for line in csv_reader:
    try:
        if line[0] == "Station MAC":
            break
        if line[0] == "BSSID":
            continue
        Vals = [13,0,5,6,7,10,3,8,9]
        x=0

        results = {
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
        for i in Vals:
            results[network_info[x]] = str(line[i]).strip()

            x+=1
        RESULT.append(results)


    except:
        pass
print(RESULT)
