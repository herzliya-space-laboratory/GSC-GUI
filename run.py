import sys
import signal
from flask import Flask, render_template, request, redirect
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
#import webbrowser
from datetime import datetime
import threading
from os.path import isfile, join

'''
Error 10: Unable to parse integer fro telemetry
'''

import socket
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

with open('config.json', 'r') as file:
    config = file.read().replace('\n', '')
config = json.loads(config)

TCP_IP = config["baseIP"]
TCP_PORT = config["basePort"]
BUFFER_SIZE = config["bufferSize"]


handshake = "{'Type': 'GUI'}"

s = None

endNodes = []
commandIds = []
isGSCconnected = False


def connectToGSC():
    global s
    global isGSCconnected
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(200)
    s.connect((TCP_IP, TCP_PORT))
    s.send(handshake.encode())
    print("Connected")
    isGSCconnected = True


try:
    connectToGSC()
except:
    print("GSC not connected")

f = open(config["mibPath"], "r")

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

app = Flask(__name__)

commandsWeb = "commands.html"
index = "index.html"
feedWeb = "feed.html"
logsWeb = "logs.html"
playground = "playground.html"
beaconWeb = "beacon.html"
dumpWeb = "dump.html"
graphPage = "paramGraph.html"
graphForm = "graphForm.html"
commandAcksWeb = "commandAcks.html"
loginWeb = "login.html"

def IPAddrValidate():
    ip = request.remote_addr
    if(ip[0:3] == "172" or ip == "127.0.0.1"):
        print(ip + " is Allowed to connect")
        return True
    print(ip + " is not allowed to connect")
    return False


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


def findAll(itemList, item):
    return [i for i, x in enumerate(itemList) if x == item]


def getParam(line):
    '''Take last number from line'''
    line = line.replace("\n", "")
    line = line.split(",")
    param = line[2]
    if is_date(param):
        return param
    else:
        param = param.replace(" ", "")
        return param
    return None


def getUnit(line):
    line = line.replace("\n", "")
    line = line.split(",")
    return line[-1]


def sortByTime(data, paramName, isReverse):
    sortedArray = sorted(
        data,
        key=lambda x: datetime.strptime(x[paramName], '%d/%m/%Y %H:%M:%S'), reverse=isReverse)

    return sortedArray


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
    if fileName == None:
        return {}

    params = {}
    f = open(fileName, "r")
    for line in f:
        if line.startswith("Packet Ground Date Time"):
            params["ground_time"] = line.split(",")[-1].replace("\n", "")
        elif line.startswith("Packet Sat Date Time"):
            params["sat_time"] = line.split(",")[-1].replace("\n", "")

        for i in range(len(paramNames)):
            if line.startswith(paramNames[i]):
                paramVal = getParam(line)
                if is_number(paramVal):
                    paramVal = float(paramVal)
                params[paramNames[i]] = paramVal
    return params


def createLogsDict(eventLogDirectory, erroLogDirectory):
    logsDict = log_parser.ParseAllLogFilesInDirectory(
        eventLogDirectory, log_parser.EventLogParser)
    errorlogsDict = log_parser.ParseAllLogFilesInDirectory(
        erroLogDirectory, log_parser.ErrorLogParser)
    return logsDict + errorlogsDict


def getParamsFromCSV(fileName):
    if fileName == None:
        return []

    f = open(fileName, "r")

    params = []
    for line in f:
        match = re.search("^(.+?),", line)
        if match != None:
            param = match.group(1)

        if param != 'Packet ID' and param != 'Packet Ground Date Time' and param != 'Packet Sat Date Time' and param != 'Packet Total Raw Data' and param != 'Parameter Name':
            params.append(param)

    return params


def parseCSVfileForGraph(fileName, parameterName):
    if fileName == None:
        return None

    f = open(fileName, "r")

    j = 0
    for line in f:
        if j == 2 and parameterName == "Packet Sat Date Time":
            return line.split(",")[-1].replace("\n", "")

        if line.startswith(parameterName):
            return getParamForGraph(line)

        j += 1

    return None


def getParamForGraph(line):
    '''Take last number from line'''
    line = line.replace("\n", "")
    line = line.split(",")
    param = line[2]
    param = param.replace(" ", "")
    return param


def getParameterFromDirectory(directoryName, parameterName):
    paramFromDirectory = {}
    names = os.listdir(directoryName)

    for name in names:
        fileName = directoryName + "/" + name
        satTime = parseCSVfileForGraph(fileName, "Packet Sat Date Time")
        paramFromDirectory[satTime] = parseCSVfileForGraph(
            fileName, parameterName)

    return paramFromDirectory


def getUnitsFromCSV(fileName, paramNames):
    if fileName == None:
        return {}

    units = {}
    f = open(fileName, "r")
    for line in f:
        for i in range(len(paramNames)):
            if line.startswith(paramNames[i]):
                units[paramNames[i]] = getUnit(line)
    return units


def getNewestFileInDir(directory):
    if len(os.listdir(directory)) > 0:
        list_of_files = glob.glob(directory + "/*")
        return max(list_of_files, key=os.path.getctime)
    return None


def findTelemetryInMIB(serviceType, serviceSubType):
    f = open(config["mibPath"], "r")

    soup = BeautifulSoup(f.read(), "html.parser")

    sts = soup.find("gscmib").find("telemetry").find_all(
        "servicetype")

    for st in sts:
        if st['value'] == serviceType:
            for sst in st.find_all("servicesubtype"):
                if sst['value'] == serviceSubType:
                    return sst

    return None


def getParameterSubSystems(serviceType, serviceSubType):
    telemetry = findTelemetryInMIB(serviceType, serviceSubType)
    paramSubSystem = {}
    paramSubSystem["Date"] = ["sat_time", "ground_time"]

    for param in telemetry.find_all("parameter"):
        try:
            subsystem = param["description"].split(",")[0]
            if not subsystem in paramSubSystem:
                paramSubSystem[subsystem] = []
            paramSubSystem[subsystem].append(param["name"].lower())
        except:
            pass

    return paramSubSystem


def getParameterReadableNames(serviceType, serviceSubType):
    telemetry = findTelemetryInMIB(serviceType, serviceSubType)
    paramNames = {}

    for param in telemetry.find_all("parameter"):
        try:
            readableName = param["description"].split(",")[1]
            paramNames[param["name"].lower()] = readableName
        except:
            pass

    return paramNames


def getTelemetryOptions(serviceType, serviceSubType):
    telemetry = findTelemetryInMIB(serviceType, serviceSubType)
    options = {}

    for param in telemetry.find_all("parameter"):
        # minAndMax = minMaxFromType(param["type"])
        try:
            options[param["name"].lower()] = {
                # "min": minAndMax["min"],
                # "max": minAndMax["max"],
                "rangeStart": int(param["rangestart"]),
                "rangeEnd": int(param["rangeend"])
            }
        except:
            options[param["name"].lower()] = ""

    f.close()
    return options


def getSubDirs(dirPath):
    return next(os.walk(dirPath))[1]


def parseDumpDirNames(dirs, path):
    dumpNames = {}

    for d in dirs:
        # Parse service type, subtype and telemetry name from directory name
        try:
            parsedName = re.search("ST-(\d*)\ SST-(\d*)\ (.*)$", d)
            st = parsedName[1]
            sst = parsedName[2]
            name = parsedName[3]

            dumpNames[st + "-" + sst] = {
                "name": name,
                "path": path + d
            }
        except:
            pass

    return dumpNames


def sendPacket(params):
    packets = ast.literal_eval(params)
    time.sleep(0.25)
    for packet in packets:
        print("Sending to GSC: ", packet)
        print("Sending this packet to ", TCP_IP, " Port: ", TCP_PORT)
        sentBytes = s.send(str(packet).encode())
        print("Number of bytes sent: ", sentBytes)
        # print("Server respond: ", s.recv(1024))
        time.sleep(0.1)


@app.route('/commands', methods=['GET', 'POST'])
def commands():
    global s

    params = ""

    if request.args.get("packet") == None:
        print("Got NoneType")
    else:
        if IPAddrValidate():
            print("Sending to GSC")
            params = html.unescape(request.args.get("packet"))
            try:
                sendPacket(params)
            except:
                print("Trying to reconnect to base")
                connectToGSC()
                sendPacket(params)
        else:
            return "{}", 401

    return render_template(commandsWeb, commandNames=commandNames, commandNumbers=commandNumbers, paramNames=paramNames, paramTypes=paramTypes, paramUnits=paramUnits)


@app.route('/logs', methods=['GET', 'POST'])
def logs():
    logCount = request.args.get('sliceNum')

    logsDict = sortByTime(createLogsDict(
        config["eventLogsFolderPath"], config["errorLogsFolderPath"]), "Sat Time", False)

    if request.method == "POST":
        if logCount == "" or logCount == None:
            logCount = '1'

        elif int(logCount) > len(logsDict):
            logCount = len(logsDict)

        return json.dumps(logsDict[len(logsDict) - int(logCount):])

    return render_template(logsWeb, logParams=logsDict[len(logsDict) - 1:])


@app.route('/')
@app.route('/beacon', methods=['GET', 'POST'])
def beacon():
    latestFile = getNewestFileInDir(config["beaconFolderPath"])
    params = getParamsFromCSV(latestFile)
    data = parseCSVfile(latestFile, params)
    if request.method == "POST":
        return data

    paramOptions = getTelemetryOptions('3', '25')
    dispOrder = getParameterSubSystems('3', '25')
    readableNames = getParameterReadableNames('3', '25')
    readableNames["sat_time"] = "Satellite Time"
    readableNames["ground_time"] = "Ground Time"
    beaconUnits = getUnitsFromCSV(latestFile, params)
    beaconUnits["sat_time"] = "date"
    beaconUnits["ground_time"] = "date"

    return render_template(beaconWeb, beacon=data, units=beaconUnits, options=paramOptions, dispOrder=dispOrder, readableNames=readableNames)


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
    units["sat_time"] = "date"
    units["ground_time"] = "date"

    return render_template(dumpWeb, data=data, units=units, options=options, telemName=dumpDirNames[key]["name"], telemType={"st": st, "sst": sst})


@app.route('/paramGraph')
def parameterGraph():
    dumpNames = getDumpNames()
    st = request.args.get("st")
    sst = request.args.get("sst")
    parameterName = request.args.get('paramName')
    key = str(st) + "-" + str(sst)
    isLineGraph = request.args.get("isLineGraph")

    try:
        options = getTelemetryOptions(str(st), str(sst))[parameterName]

    except:
        options = {"rangeStart": "", "rangeEnd": ""}

    paramValues = getParameterFromDirectory(
        dumpDirNames[key]["path"], parameterName)

    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    startDate = datetime.strptime(startDate, '%d/%m/%Y %H:%M')

    try:
        endDate = datetime.strptime(endDate, '%d/%m/%Y %H:%M')
    except:
        endDate = datetime.today()

    forDeletion = []
    for keyDate in paramValues:
        date = datetime.strptime(keyDate, '%d/%m/%Y %H:%M:%S')
        if not(startDate <= date <= endDate):
            forDeletion.append(keyDate)
    for keyDate in forDeletion:
        del paramValues[keyDate]

    f = getNewestFileInDir(dumpDirNames[key]["path"])
    params = getParamsFromCSV(f)
    units = getUnitsFromCSV(f, params)
    unit = units[parameterName]

    return render_template(graphPage, paramData=paramValues, paramOptions=options, paramName=parameterName, paramUnit=unit, isLineGraph=isLineGraph)


@app.route('/getDumpNames')
def getDumpNames():
    dumpTypes = {}
    for key in dumpDirNames:
        if len(os.listdir(dumpDirNames[key]["path"])) != 0:
            split = key.split("-")
            dumpTypes[dumpDirNames[key]["name"]] = {
                "st": split[0],
                "sst": split[1]
            }
    return dumpTypes

@app.route('/login')
def loginPage():
    return render_template(loginWeb)

@app.route('/graphForm')
def graph():
    return render_template(graphForm)


@app.route('/getTelemParams')
def getTelemParams():
    st = request.args.get("st")
    sst = request.args.get("sst")

    key = str(st) + "-" + str(sst)
    f = getNewestFileInDir(dumpDirNames[key]["path"])
    params = getParamsFromCSV(f)
    return {"params": params}


@app.route('/getAcks')
def getAcks():
    global numOfAcks
    newNumOfAcks = len(os.listdir(dumpDirNames["13-90"]["path"]))
    if newNumOfAcks > numOfAcks:
        f = getNewestFileInDir(dumpDirNames["13-90"]["path"])
        params = getParamsFromCSV(f)
        data = parseCSVfile(f, params)
        numOfAcks = newNumOfAcks
        return json.dumps(data)
    return "null"


@app.route("/v2")
def GUIv2():
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@app.route("/getEndNodes")
def getEndNode():
    global endNodes
    return {"endNodes": endNodes}
    # return {"endNodes": [{"Name": "blabla", "Id": "3"}, {"Name": "System.Object", "Id": "2"}, {"Name": "Sscdc", "Id": "4"}]}


@app.route('/acks', methods=['GET', 'POST'])
def commandAcks():
    global commandIds
    ackDirPath = dumpDirNames["13-90"]["path"]
    ackFilesPaths = [join(ackDirPath, f) for f in os.listdir(ackDirPath)]
    params = getParamsFromCSV(ackFilesPaths[0])
    acks = []

    for comm in commandIds:
        acks.append(comm)
        acks[-1]["Sat Time"] = "-"
        acks[-1]["GroundTime"] = "-"
        acks[-1]["AckType"] = "-"
        acks[-1]["ErrorType"] = "-"
        acks[-1]["Color"] = "grey white-text"

    for path in ackFilesPaths:
        parsedAck = parseCSVfile(path, params)
        index = -1
        for i in range(len(acks)):
            if acks[i]["Id"] == parsedAck["commandid"]:
                index = i
                break

        if index != -1:
            acks[index]["Sat Time"] = parsedAck["sat_time"]
            acks[index]["GroundTime"] = parsedAck["ground_time"]
            acks[index]["AckType"] = parsedAck["acktype"]
            acks[index]["ErrorType"] = parsedAck["errortype"]
            if parsedAck["errortype"] != 0:
                acks[index]["Color"] = "red white-text"
            else:
                acks[index]["Color"] = "blue white-text"
    acks = sortByTime(acks, "TimeSent", True)
    if request.method == "POST":
        return {"Content": acks}
    return render_template(commandAcksWeb, acksList={"Content": acks})


dumpDirNames = parseDumpDirNames(getSubDirs(
    config["telemetryFolderPath"]), config["telemetryFolderPath"])
numOfAcks = len(os.listdir(dumpDirNames["13-90"]["path"]))


def socketInputLoop():
    gscBuffer = ""
    global s
    global isGSCconnected
    while True:
        if not isGSCconnected:
            try:
                connectToGSC()
            except:
                pass
            time.sleep(1.0)
        else:
            try:
                s.settimeout(3.0)
                while True:
                    try:
                        res = s.recv(1024)
                        gscBuffer += res.decode("ascii")
                    except socket.timeout:
                        break
            except socket.error:
                isGSCconnected = False
                continue

            if gscBuffer != "":
                packets = splitJSON(gscBuffer)
                dealWithGSCres(packets)
                gscBuffer = ""


def dealWithGSCres(res):
    global endNodes
    global commandIds
    global isGSCconnected

    for packet in res:
        packet = json.loads(packet)
        print("Got from GSC: " + str(packet))
        if packet["Type"] == "SystemAck":
            print("Got ack")
            commandIds.append({
                "Id": packet["Content"],
                "TimeSent": datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            })
        elif packet["Type"] == "EndNodes":
            print("Endnode change")
            endNodes = packet["Content"]
        elif packet["Type"] == "Disconnection":
            print("GSC disconnected")
            isGSCconnected = False


def splitJSON(msg):
    msg = msg.split("}{")
    if len(msg) > 1:
        msg[0] += "}"
        for i in range(1, len(msg) - 1):
            msg[i] = "{" + msg[i] + "}"
        msg[-1] = "{" + msg[-1]
    return msg


socketLoopThread = threading.Thread(target=socketInputLoop)
socketLoopThread.daemon = True
socketLoopThread.start()


def signal_handler(sig, frame):
    global s
    s.send('{"Type": "Disconnection"}'.encode())
    s.close()
    print("Bye!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

app.run(debug=config["debugMode"], host='0.0.0.0')

# I'm Alon Grossman and I have scribbled on the GSC-GUI code

# webbrowser.open('http://127.0.0.1:5000/')
