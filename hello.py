from flask import Flask, render_template, request
import os
from bs4 import BeautifulSoup
import json
import html
import ast
from dateutil.parser import parse
import time
import glob
import log_parser

'''
Error 10: Unable to parse integer fro telemetry
'''

import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

is_tcp_connected = False

handshake = "{'Type': 'GUI'}"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

f = open("MIB.xml", "r")

soup = BeautifulSoup(f.read(), "html.parser")
commandNames = []
commandNumbers = []
paramNames = []
paramTypes = []
paramUnits = []

commands = soup.find("gscmib").find("telecommands")

for serType in commands.find_all("servicetype"):
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


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def getParam(line):
    '''Take last number from line'''
    line = line.replace("\n", "")
    line = line.split(",")
    for i in range(len(line)):
        param = line[-(i+1)]
        if is_date(param):
            return param
        else:
            param = param.replace(" ", "")
            if is_number(param):
                return param
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
                    if is_number(paramVal):
                        paramVal = float(paramVal)
                    if paramNames[i] in params.keys():
                        params[paramNames[i]].append([name, getParam(line)])
                    else:
                        params[paramNames[i]] = [[name, getParam(line)]]
    return params


def praseNewestCSVdir(directory, paramNames, params={}):
    '''For each file, find param name and append it to param dictionary.'''
    list_of_files = glob.glob(directory + "/*")
    latest_file = max(list_of_files, key=os.path.getctime)
    f = open(latest_file, "r")
    for line in f:
        for i in range(len(paramNames)):
            if line.startswith(paramNames[i]):
                paramVal = getParam(line)
                if is_number(paramVal):
                    paramVal = float(paramVal)
                params[paramNames[i]] = paramVal
    return params


app = Flask(__name__)

commandsWeb = "commands.html"
index = "index.html"
feedWeb = "feed.html"
logsWeb = "logs.html"
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
            time.sleep(0.25)
        for packet in packets:
            print("This is: ", packet)
            print("Sending this packet to ", TCP_IP, " Port: ", TCP_PORT)
            sentBytes = s.send(str(packet).encode())
            print("Number of bytes sent: ", sentBytes)

    return render_template(commandsWeb, commandNames=commandNames, commandNumbers=commandNumbers, paramNames=paramNames, paramTypes=paramTypes, paramUnits=paramUnits)


@app.route('/')
def home():
    return render_template(index)


@app.route('/feed', methods=['GET', 'POST'])
def feed():
    params1 = {}
    praseCSV("BeaconDemo", ["batt_curr", "3v3_curr", "vbatt",
                            "Packet Sat Date Time", "Packet Ground Date Time"], params1)
    if request.method == "POST":
        params1 = {}
        praseCSV("BeaconDemo", ["batt_curr", "3v3_curr", "vbatt",
                                "Packet Sat Date Time", "Packet Ground Date Time"], params1)
        return params1
    return render_template(feedWeb, satParams=params1)


@app.route('/logs', methods=['GET', 'POST'])
def logs():
    logsDict = log_parser.ParseAllLogFilesInDirectory(
        "Event logs", log_parser.EventLogParser)
    if request.method == "POST":
        return logsDict
    return render_template(logsWeb, logParams=logsDict)


@app.route('/play')
def palyground():
    return render_template(playground)


app.run(debug=True)
