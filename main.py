import time
import json
import asyncio
from microdot import Microdot, send_file, websocket
import systemfunctions


sendstate = dict()

sendstate['ldrive'] = 0
sendstate['rdrive'] = 0

pstate = dict()

pstate['joy1x'] = 0
pstate['joy1y'] = 0
pstate['joy2x'] = 0
pstate['joy2y'] = 0
pstate['updated'] = time.time()

astate = dict()


app = Microdot()

@app.route('/', methods=['GET'])
async def index(request):
    return send_file('assets/index.html')

@app.route('/joy.js', methods=['GET'])
async def joy(request):
    return send_file('assets/joy.js')

# @app.route('/shutdown', methods=['GET'])
# async def shutdown(request):
#     request.app.shutdown()
#     return 'shutting down'

@app.route('/data')
@websocket.with_websocket
async def data(request, ws):
    global pstate
    while True:
        message = await ws.receive()
        # print("ws: "+message)
        try:
            message = json.loads(message)
            if 'joy1x' in message.keys():
                pstate['updated'] = time.time()
                pstate['joy1x'] = message['joy1x']
            if 'joy1y' in message.keys():
                pstate['updated'] = time.time()
                pstate['joy1y'] = message['joy1y']
            if 'joy2x' in message.keys():
                pstate['updated'] = time.time()
                pstate['joy2x'] = message['joy2x']
            if 'joy2y' in message.keys():
                pstate['updated'] = time.time()
                pstate['joy2y'] = message['joy2y']

        except ValueError:
            print("malformed json")
        await ws.send("rcvd")


async def loop():
    global astate
    done = False
    while not done:
        await asyncio.sleep(0.05)
        sendstate['ldrive'] = int(max(-100, min(100, int(pstate['joy1y']))))
        sendstate['rdrive'] = int(max(-100, min(100, int(pstate['joy2y']))))
        read = systemfunctions.rw_anet(sendstate, 0.15)
        if not read == -1:
            astate = read
            # if astate['readerror'] > 1:
            #     print(astate)
            # print(astate)
            



async def webserver():
    await app.start_server(debug=True,host='0.0.0.0', port=80)


async def tasks():
    await asyncio.gather(webserver(), loop())


if __name__ == "__main__":
    print("starting")
    # systemfunctions.update()
    systemfunctions.setup_anet_connection()
    asyncio.run(tasks())