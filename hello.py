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
import re

'''
Error 10: Unable to parse integer fro telemetry
'''

import socket

TCP_IP = '80.178.203.191'
TCP_PORT = 61015
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


def getUnit(line):
    line = line.replace("\n", "")
    line = line.split(",")
    return line[-1]


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


def parseCSVfile(fileName, paramNames):
    params = {}
    f = open(fileName, "r")
    j = 0
    for line in f:
        if j == 2:
            params["sat_time"] = line.split(",")[-1].replace("\n", "")

        for i in range(len(paramNames)):
            if line.startswith(paramNames[i]):
                paramVal = getParam(line)
                if is_number(paramVal):
                    paramVal = float(paramVal)
                params[paramNames[i]] = paramVal
        j += 1
    return params


def createLogsDict(eventLogDirectory, erroLogDirectory):
    logsDict = log_parser.ParseAllLogFilesInDirectory(
        eventLogDirectory, log_parser.EventLogParser)
    errorlogsDict = log_parser.ParseAllLogFilesInDirectory(
        erroLogDirectory, log_parser.ErrorLogParser)
    return logsDict + errorlogsDict


def getParamsFromCSV(fileName):
    f = open(fileName, "r")

    params = []
    for line in f:
        match = re.search("^(.+?),", line)
        if match != None:
            param = match.group(1)

        if param != 'Packet ID' and param != 'Packet Ground Date Time' and param != 'Packet Sat Date Time' and param != 'Packet Total Raw Data' and param != 'Parameter Name':
            params.append(param)

    return params


def getUnitsFromCSV(fileName, paramNames):
    units = {}
    f = open(fileName, "r")
    for line in f:
        for i in range(len(paramNames)):
            if line.startswith(paramNames[i]):
                units[paramNames[i]] = getUnit(line)
    return units


def getNewestFileInDir(directory):
    list_of_files = glob.glob(directory + "/*")
    return max(list_of_files, key=os.path.getctime)


def minMaxFromType(t):
    return {
        'uint16': {"min": 0, "max": 65535},
        'int16': {"min": -32768, "max": 32767},
        'uint32': {"min": 0, "max": 4294967295},
        'byte': {"min": -128, "max": 127},
        'dateTime': {"min": 0, "max": 0},
        'string': {"min": 0, "max": 0}
    }[t]


def getCSVPacketId(path):
    f = open(path, "r")
    return f.readline().split(",")[1]


def findTelemetryInMIB(serviceType, serviceSubType):
    f = open("MIB.xml", "r")

    soup = BeautifulSoup(f.read(), "html.parser")

    sts = soup.find("gscmib").find("telemetry").find_all(
        "servicetype")

    for st in sts:
        if st['value'] == serviceType:
            for sst in st.find_all("servicesubtype"):
                if sst['value'] == serviceSubType:
                    return sst

    return None


def getTelemetryOptions(serviceType, serviceSubType):
    telemetry = findTelemetryInMIB(serviceType, serviceSubType)
    options = {}

    for param in telemetry.find_all("parameter"):
        # minAndMax = minMaxFromType(param["type"])
        try:
            options[param["name"]] = {
                # "min": minAndMax["min"],
                # "max": minAndMax["max"],
                "rangeStart": int(param["rangestart"]),
                "rangeEnd": int(param["rangeend"])
            }
        except:
            options[param["name"]] = ""

    f.close()
    return options


def getSubDirs(dirPath):
    return next(os.walk(dirPath))[1]


def parseDumpDirNames(dirs, path):
    dumpNames = {}

    for d in dirs:
        # Parse service type, subtype and telemetry name from directory name
        parsedName = re.search("ST-(\d*)\ SST-(\d*)\ (.*)$", d)

        st = parsedName[1]
        sst = parsedName[2]
        name = parsedName[3]

        dumpNames[st + "-" + sst] = {
            "name": name,
            "path": path + d
        }

    return dumpNames


app = Flask(__name__)

commandsWeb = "commands.html"
index = "index.html"
feedWeb = "feed.html"
logsWeb = "logs.html"
playground = "playground.html"
beaconWeb = "beacon.html"
dumpWeb = "dump.html"

dumpDirNames = parseDumpDirNames(getSubDirs("DumpDemo"), "DumpDemo/")


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


@app.route('/logs', methods=['GET', 'POST'])
def logs():
    logsDict = createLogsDict("Event logs", "Error logs")
    if request.method == "POST":
        return json.dumps(createLogsDict("Event logs", "Error logs"))
    return render_template(logsWeb, logParams=logsDict)


@app.route('/beacon', methods=['GET', 'POST'])
def beacon():
    latestFile = getNewestFileInDir("BeaconDemo")
    params = getParamsFromCSV(latestFile)
    data = parseCSVfile(latestFile, params)
    if request.method == "POST":
        return data

    paramOptions = getTelemetryOptions('3', '25')
    beaconUnits = getUnitsFromCSV(latestFile, params)
    beaconUnits["sat_time"] = "date"

    return render_template(beaconWeb, beacon=data, units=beaconUnits, options=paramOptions)


@app.route('/play')
def palyground():
    return render_template(playground)


@app.route('/dump', methods=['GET', 'POST'])
def dump():
    st = request.args.get('st')
    sst = request.args.get('sst')

    key = str(st) + "-" + str(sst)
    f = getNewestFileInDir(dumpDirNames[key]["path"])
    params = getParamsFromCSV(f)
    data = parseCSVfile(f, params)

    if request.method == "POST":
        return data

    options = getTelemetryOptions(str(st), str(sst))
    units = getUnitsFromCSV(f, params)

    return render_template(dumpWeb, data=data, units=units, options=options, telemName=dumpDirNames[key]["name"], telemType={"st": st, "sst": sst})


@app.route('/getDumpNames')
def getDumpNames():
    dumpTypes = {}
    for key in dumpDirNames:
        split = key.split("-")
        dumpTypes[dumpDirNames[key]["name"]] = {
            "st": split[0],
            "sst": split[1]
        }
    return dumpTypes


app.run(debug=True)
