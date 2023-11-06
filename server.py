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

from main import Listener, Stop_Listener, Listener2

import threading
app = Sanic(__name__)
HOST = "localhost"
PORT = 8000


app = Sanic('app')
app.static('/static', './static')

connected_clients = set()


from WEBSOCKETS import network_feed_handler, device_feed_handler


# Socket for Network Scan
@app.websocket('/network-feed')
async def network_feed(request: Request, ws: Websocket):
    while True:
        await network_feed_handler(request,ws)

@app.websocket('/device-feed')
async def device_feed(request: Request, ws: Websocket):
    while True:
        print('working???')
        await device_feed_handler(request,ws)

#Start/Stop Scanner
@app.route('/', methods=['GET', 'POST'])
async def Start_Scanner(request):
    Mode = None
    action = request.form.get('action')
    try:
        print("MODE IS ACTIVE")
        Mode = request.form.get('Mode')
        BSSID = request.form.get('BSSID')
    except:
        print('failed to get Mode')
    if request.method == 'POST':
        if action == "Start":
            stop_event = asyncio.Event()

            if Mode == "Devices":

                print(f'BSSID: {BSSID}')
                asyncio.create_task(Listener2(stop_event, 'wlan0mon',BSSID))
            else:
                asyncio.create_task(Listener(stop_event, 'wlan0mon'))



            #asyncio.create_task(Listener2(stop_event, 'wlan0mon',))

        elif action == "stop":
            asyncio.create_task(Stop_Listener()) #This creates a new task in the same thread
        elif action == "stop2":
            asyncio.create_task('pass') #This creates a new task in the same thread
    return await response.file('index.html')


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)

