def ParseLogFileField(file_data, field_name):
    index = file_data.find(field_name)
    if index == -1:
        return None

    index += len(field_name) + len(",00-00-00-00,")
    
    end_index = file_data.find(",", index)
    if end_index == -1:
        return None

    return int(file_data[index:end_index])


def ParseLogFile(path, logFileParsingFunction):
    file_data = open(path, 'r').read()
    
    log_type = ParseLogFileField(file_data, "log num")
    if log_type == None:
        return ""

    log_data = ParseLogFileField(file_data, "info")
    if log_data == None:
        return ""

    output = None

    try:
        output = logFileParsingFunction(log_type)
        output.append(log_data)
    except:
        print("-E-\t Error ("") at file: "+path)
    else:
        if None in output:
            output = None	

    return output


def ConvertDateFromFileNameFormatToNormal(date):
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    minute = date[14:16]
    second =date[17:19]

    return str(day)+'/'+str(month)+'/'+str(year)+' '+str(hour)+':'+str(minute)+':'+str(second)


def ParseAllLogFilesInDirectory(directory, logFileParsingFunction):
    output = "System,Log Type,Data,Sat Time,Ground Time\n"
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            log = ParseLogFile(os.path.join(directory, filename), logFileParsingFunction)
            if not log == None:
                output += str(log[0]) + ',' + str(log[1]) + ',' + str(log[2]) + ',' + ConvertDateFromFileNameFormatToNormal(filename[15:34]) + ',' + ConvertDateFromFileNameFormatToNormal(filename[43:62]) + '\n'

    return output



def ParseAllLogFilesInDirectory(directory, logFileParsingFunction):
    output = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            log = ParseLogFile(os.path.join(directory, filename), logFileParsingFunction)
            rowDict = {}
            if not log == None:
                rowDict["System"] = (log[0])
                rowDict["Log Type"] = (log[1])
                rowDict["Data"] = (log[2])
                rowDict["Sat Time"] = (ConvertDateFromFileNameFormatToNormal(filename[14:33]))
                rowDict["Ground Time"] = (ConvertDateFromFileNameFormatToNormal(filename[42:61]))
                output.append(rowDict)

    return output