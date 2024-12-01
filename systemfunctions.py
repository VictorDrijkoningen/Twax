import requests
import serial
import json
import time

LASTSENT = 0



def update(force_update = False):
    with open(".env") as f:
        env = f.read().split(",")
    with open("VERSION") as file:
        twax_version = file.read()
        githubversion = requests.get(env[0]).text
        if twax_version != githubversion or force_update:
            print(twax_version.split("-")[0]+" / "+ str(githubversion).split("-")[0])
            with open('VERSION', 'w') as f:
                f.write(githubversion)
            with open('main.py', 'w') as f:
                f.write(requests.get(env[1]).text)
            with open('AnetBoard/AnetBoard.ino', 'w') as f:
                f.write(requests.get(env[2]).text)
            with open('systemfunctions.py', 'w') as f:
                f.write(requests.get(env[3]).text)
            upload_to_anet()
        print('done updating')
    return twax_version


def upload_to_anet():
    pass


def setup_anet_connection():
    global ANETSERIAL

    with open(".env") as f:
        env = f.read().split(",")

    ANETSERIAL = serial.Serial(env[4], 115200, timeout=0.050)  # open serial port


def rw_anet(sendstate, sendtimeout):
    """update the state of the anet board and get sensor data"""
    global ANETSERIAL
    global LASTSENT
    if time.time() - LASTSENT > sendtimeout:
        ANETSERIAL.write("a".encode('ascii'))
        ANETSERIAL.write((sendstate['ldrive']+100).to_bytes(1, 'big'))
        ANETSERIAL.write("b".encode('ascii'))
        ANETSERIAL.write((sendstate['rdrive']+100).to_bytes(1, 'big'))
        ANETSERIAL.write("z".encode('ascii'))
        LASTSENT = time.time()

    datasize = 100

    if ANETSERIAL.in_waiting > datasize:
        astate_raw = str(ANETSERIAL.readline())[2:-5]
        
        try:
            out = json.loads(astate_raw)
            out['updatedtime'] = time.time()
            return out
        except ValueError as e:
            print(astate_raw)
            print("Malformed json")
            # print(e)

    return -1
