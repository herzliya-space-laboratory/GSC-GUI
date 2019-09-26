from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup
import json
import html
import ast

'''
Error 10: Unable to parse integer fro telemetry
'''

import socket

TCP_IP = '172.16.1.241'
TCP_PORT = 61015
BUFFER_SIZE = 1024

handshake = "{'Type': 'GUI'}"
is_tcp_connected = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

f = open("MIB.xml", "r")

soup = BeautifulSoup(f.read(), 'html.parser')
commandNames = []
commandNumbers = []
paramNames = []
paramTypes = []
paramUnits = []

for serType in soup.find_all("servicetype"):
    typeVal = serType.get("value")
    for subtype in serType.find_all("servicesubtype"):
        subtypeName = subtype.get("name")
        subtypeValue = int(subtype.get("value"))
        names = []
        types = []
        units = []
        for param in subtype.find_all("parameter"):
            names.append(param.get("name"))
            types.append(param.get("type"))
            units.append(param.get("unit"))
        paramNames.append(names)
        paramTypes.append(types)
        paramUnits.append(units)
        commandNames.append(subtypeName)
        commandNumbers.append(
            repr((int(typeVal), subtypeValue)).replace(" ", ""))
f.close()


def is_number(s):
    '''Finds out if string is a number'''
    try:
        float(s)
        return True
    except ValueError:
        return False


def getParam(line):
    '''Take last number from line'''
    line = line.replace(" ", "")
    line = line.split(",")
    for i in range(len(line)):
        if is_number(line[-(i+1)]):
            return line[-(i+1)]
    return None


def praseCSV(directory, paramNames, params={}):
    '''For each file, find param name and append it to param dictionary.'''
    names = os.listdir(directory)
    for name in names:
        f = open(directory + "/"+name, "r")
        for line in f:
            for i in range(len(paramNames)):
                if line.startswith(paramNames[i]):
                    paramVal = getParam(line)
                    if not is_number(paramVal):
                        print("Error 10 unable to read value from file:",
                              name, " Value: ", paramVal)
                    if paramNames[i] in params.keys():
                        params[paramNames[i]].append(
                            [name, float(getParam(line))])
                    else:
                        params[paramNames[i]] = [[name, float(getParam(line))]]
    return params


app = Flask(__name__)

commandsWeb = "commands.html"
index = "index.html"
feedWeb = "feed.html"
playground = "playground.html"


@app.route('/commands')
def commands():
    global is_tcp_connected
    global handshake
    params = ""

    if request.args.get("packet") == None:
        print("Got NoneType")
    else:
        params = html.unescape(request.args.get("packet"))
        packets = ast.literal_eval(params)
        if not is_tcp_connected:
            s.connect((TCP_IP, TCP_PORT))
            is_tcp_connected = True
            s.send(handshake.encode())
        for packet in packets:
            print("This is: ", packet)
            print("Sending this packet to ", TCP_IP, " Port: ", TCP_PORT)
            sentBytes = s.send(str(packet).encode())
            print("Number of bytes sent: ", sentBytes)

    return render_template(commandsWeb, commandNames=commandNames, commandNumbers=commandNumbers, paramNames=paramNames, paramTypes=paramTypes, paramUnits=paramUnits)


@app.route('/')
def home():
    return render_template(index)


@app.route('/feed')
def feed():
    params1 = {}
    praseCSV("telemFEED", ["Batt_Curr", "3v3_curr",
                           "Rxdoppler", "vbatt"], params1)
    return render_template(feedWeb, satParams=params1)


@app.route('/play')
def palyground():
    return render_template(playground)


app.run(debug=True)
