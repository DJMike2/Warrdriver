from sanic import Sanic, json, request, response
from sanic.response import text

from sanic import Request, Websocket
#import pywifi
import asyncio

import dotmap
import xml
import xmltodict
import csv
import json


async def network_feed_handler(request, ws):
   await asyncio.sleep(1)

   try:
      with open('/home/dj/PycharmProjects/WLAN/ListDB-01.kismet.netxml', 'r') as file:
         raw_data = file.read()
   except:
      return
   xmla = xmltodict.parse(raw_data)
   dotmap_data = dotmap.DotMap(xmla)

   try:
      wireless_networks = len(xmla["detection-run"]["wireless-network"])
      networks = dotmap_data["detection-run"]["wireless-network"]
   except:
      return

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
   if wireless_networks == 0:
      return
   for i in range(wireless_networks):  # 1
      if networks[i]['@type'] == 'probe':  # Include in a diff section
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
      x = 0
      for each in dict.values():

         current_level = networks[i]
         for index in each:  # indices
            try:
               current_level = current_level[index]
            except IndexError:
               print("Index out of range")
               break

         try:
            current_level = current_level.get('#text')
         except:
            pass
         if x == 2 or x == 3:  # Skip the encryption
            x += 1
            continue

         if isinstance(current_level, list):
            results2[network_info[x]] = current_level
            x += 1

         else:
            results2[network_info[x]] = current_level
            x += 1
      DATA = {i: results2}
      RESULT.append(DATA)
   # Return the data as JSON
   try:
      await ws.send(json.dumps(RESULT))
   except:
      print('failed to send data')



async def device_feed_handler(request, ws): #wireless-client | client-mac | client-manuf | channel | encoding | carrier | snr-info][last_signal_dbm]
   await asyncio.sleep(1)
   print("NEW")

   try:
      with open('/home/dj/PycharmProjects/WLAN/DEVICESDB-01.kismet.netxml', 'r') as file:
         raw_data = file.read()
   except:
      print('failed to open File')
      return
   try:
      xmla = xmltodict.parse(raw_data)
   except:
      print('failed to parse data')
   dotmap_data = dotmap.DotMap(xmla)

   try:
      wireless_clients= xmla["detection-run"]["wireless-network"]["wireless-client"]
      clients = dotmap_data["detection-run"]["wireless-network"]["wireless-client"]
   except:
      print('No clients detected')
      return

   print(clients)
   if isinstance(wireless_clients, list):
      wireless_clients = len(wireless_clients)
   else:
      wireless_clients = 1
   client_info = ['client-mac', 'client-manuf', 'channel', 'encoding', 'PWR', 'carrier']
   #wireless-client | client-mac | client-manuf | channel | encoding | carrier | snr-info][last_signal_dbm] 7/9
   dict = {
      1: ["client-mac"],
      2: ["client-manuf"],
      3: ["channel"],
      4: ["encoding"],
      5: ["snr-info", "last_signal_dbm"],
      6: ["carrier"],

   }
   RESULT = []
   print(wireless_clients)
   for i in range(wireless_clients):  # 1


      results2 = {
         'client-mac': 'Your BSSID Value',
         'client-manuf': 'Your Encryption Type',
         'channel': 'Your Cipher Type',
         'encoding': 'Your Authentication Type',
         'PWR': 'Your Frequency',
         'carrier': 'Your Channel Number'
      }
      x = 0
      for each in dict.values():
#[{0: {'client-mac': '34:20:03:79:9F:21', 'client-manuf': 'Shenzhen Feitengyun Technology Co.,LTD', 'channel': '1', 'encoding': 'CCK', 'PWR': '-47', 'carrier': 'IEEE 802.11b+'}}, {1: {'client-mac': 'C8:94:02:15:69:61', 'client-manuf': 'CHONGQING FUGUI ELECTRONICS CO.,LTD.', 'channel': '1', 'encoding': 'CCK', 'PWR': '-39', 'carrier': 'IEEE 802.11b+'}}, {2: {'client-mac': '7C:A6:B0:0A:1D:5D', 'client-manuf': 'Unknown', 'channel': '1', 'encoding': 'CCK', 'PWR': '-55', 'carrier': 'IEEE 802.11b+'}}]

         if wireless_clients == 1:
            current_level = clients
         else:
            current_level = clients[i] #REG LIST
         for index in each:  # indices
            try:
               #print(current_level)
               current_level = current_level[index]
               print(current_level)
            except IndexError:
               print("Index out of range")
               break


         try:
            current_level = current_level.get('#text')
         except:
            pass
         print(current_level) #Null???
         print(client_info[x])
         #continue

         results2[client_info[x]] = current_level
         x+=1
      DATA = {i: results2}
      RESULT.append(DATA)

   # Return the data as JSON
   print(RESULT)
   #return
   try:
      #print(RESULT)
      await ws.send(json.dumps(RESULT))
   except:
      print('failed to send data')