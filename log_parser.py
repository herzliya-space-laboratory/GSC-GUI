import os
import json

with open('config.json', 'r') as file:
    config = file.read().replace('\n', '')
config = json.loads(config)

# =============================================================================
# First Part: Normal log parser
# Recieves log number, and check the relevant subsystem by a defined offset
# The delta remained is the log by the sybsystem
# =============================================================================
def EventLogParser(input_number):
    log_eps = [
        'EPS_ENTER_FULL_MODE',
        'EPS_ENTER_CRUISE_MODE',
        'EPS_ENTER_SAFE_MODE',
        'EPS_ENTER_CRITICAL_MODE',
        'EPS_SOFT_RESET',
        'EPS_HARD_RESET']
    log_payload = [
        'PAYLOAD_TOOK_IMAGE',
        'PAYLOAD_TRANSFERRED_IMAGE',
        'PAYLOAD_COMPRESSED_IMAGE',
        'PAYLOAD_ERASED_IMAGE',
        'PAYLOAD_TURNED_GECKO_ON',
        'PAYLOAD_TURNED_GECKO_OFF']
    log_transponder = [
        'TRANSPONDER_ACTIVATION',
        'TRANSPONDER_DEACTIVATION',
        'TRXVU_SOFT_RESET',
        'TRXVU_HARD_ESET',
        'ANTS_A_HARD_RESET',
        'ANTS_B_HARD_RESET',
        'ANTS_DEPLOY']
    log_systems = [
        'SYSTEM_TRXVU',
        'SYSTEM_EPS',
        'SYSTEM_PAYLOAD',
        'SYSTEM_PAYLOAD_AUTO_HANDLING',
        'SYSTEM_OBC',
        'SYSTEM_ADCS',
        'SYSTEM_ANTS',
        'SYSTEM_CUF']
    log_adcs = [
        'LOG_ADCS_SUCCESS',
        'LOG_ADCS_FAIL',
        'LOG_ADCS_ADCS_INIT_ERR',
        'LOG_ADCS_QUEUE_CREATE_ERR',
        'LOG_ADCS_SEMAPHORE_CREATE_ERR',
        'LOG_ADCS_BOOT_ERROR',
        'LOG_ADCS_CHANNEL_OFF',
        'LOG_ADCS_CMD_ERR',
        'LOG_ADCS_CMD_RECEIVED',
        'LOG_ADCS_UPDATED_VECTOR',
        'LOG_ADCS_WRONG_SUB_TYPE',
        'LOG_ADCS_WRONG_TYPE',
        'LOG_ADCS_FS_INIT_ERR',
        'LOG_ADCS_FS_WRITE_ERR',
        'LOG_ADCS_FS_READ_ERR',
        'LOG_ADCS_FRAM_WRITE_ERR',
        'LOG_ADCS_FRAM_READ_ERR',
        'LOG_ADCS_INPUT_PARAM_ERR',
        'LOG_ADCS_NULL_DATA',
        'LOG_ADCS_TLM_SAVE_ERR',
        'LOG_ADCS_TLM_ERR',
        'LOG_ADCS_QUEUE_ERR',
        'LOG_ADCS_MALLOC_ERR',
        'LOG_ADCS_I2C_READ_ERR',
        'LOG_ADCS_I2C_WRITE_ERR',
        'LOG_ADCS_GENERIC_I2C_ACK',
        'LOG_ADCS_HARD_RESET',
        'LOG_ADCS_SOFT_RESET']
    log_cuf = [
        'CUF_EXECUTE_unauthenticated',
        'CUF_INTEGRATED_unauthenticated',
        'CUF_RESET_SUCCESSFULL',
        'CUF_RESET_THRESHOLD_MET',
        'CUF_REMOVED',
        'CUF_EXECUTED',
        'CUF_INTEGRATED',
        'CUF_DISABLED',
        'CUF_ENABLED']

    offset_number = 500

    EPS_LOG_OFFSET = offset_number * 0
    PAYLOAD_LOG_OFFSET = offset_number * 1
    TRANSPONDER_LOG_OFFSET = offset_number * 2
    RESETS_LOG_OFFSET = offset_number * 3
    ADCS_LOG_OFFSET = offset_number * 4
    CUF_LOG_OFFSET = offset_number * 5

    if (EPS_LOG_OFFSET <= input_number < PAYLOAD_LOG_OFFSET):
        system_name = 'EPS'
        system_log = input_number - EPS_LOG_OFFSET
        log = log_eps[system_log]
    elif (PAYLOAD_LOG_OFFSET <= input_number < TRANSPONDER_LOG_OFFSET):
        system_name = 'Payload'
        system_log = input_number - PAYLOAD_LOG_OFFSET
        log = log_payload[system_log]
    elif (TRANSPONDER_LOG_OFFSET <= input_number < RESETS_LOG_OFFSET):
        system_name = 'Transponder'
        system_log = input_number - TRANSPONDER_LOG_OFFSET
        log = log_transponder[system_log]
    elif (RESETS_LOG_OFFSET <= input_number < ADCS_LOG_OFFSET):
        system_name = 'System Resets'
        system_log = input_number - RESETS_LOG_OFFSET
        log = log_systems[system_log]
    elif (ADCS_LOG_OFFSET <= input_number < CUF_LOG_OFFSET):
        system_name = 'ADCS'
        system_log = input_number - ADCS_LOG_OFFSET
        log = log_adcs[system_log]
    elif (CUF_LOG_OFFSET <= input_number < (CUF_LOG_OFFSET + len(log_cuf))):
        system_name = 'CUF'
        system_log = input_number - CUF_LOG_OFFSET
        log = log_cuf[system_log]
    else:
        system_name = 'Error'
        log = 'System not found'

    return [system_name, log]


# =============================================================================
# Second Part: Error log parser
# Recieves log number, and check the relevant subsystem by a defined offset
# The delta remained is the log by the sybsystem
# =============================================================================
def ErrorLogParser(input_number):
    log_systems_for_offset = [
        'SYSTEM_TRXVU',
        'SYSTEM_EPS',
        'SYSTEM_PAYLOAD',
        'SYSTEM_PAYLOAD_AUTO_HANDLING',
        'SYSTEM_OBC',
        'SYSTEM_ADCS',
        'SYSTEM_ANTS',
        'SYSTEM_CUF']

    offset_number = 500

    log_errors_CUF = [
        'CUF_GENERATE_SSH_FAIL',
        'CUF_AUTHENTICATE_FAIL',
        'CUF_SAVE_PERMINANTE_FAIL',
        'CUF_LOAD_PERMINANTE_FAIL',
        'CUF_UPDATE_PERMINANTE_FAIL',
        'CUF_EXECUTE_FAIL',
        'CUF_INTEGRATED_FAIL',
        'CUF_ENABLE_FAIL',
        'CUF_DISABLE_FAIL'
    ]
    log_errors_OBC = [
        'LOG_ERR_FRAM_WRITE',
        'LOG_ERR_FRAM_READ',
        'LOG_ERR_GET_TIME',
        'LOG_ERR_SET_TIME',
        'LOG_ERR_DELETE_TM',
        'LOG_ERR_DELETE_FILES',
        'LOG_ERR_RESET_FRAM_MAIN',
        'LOG_ERR_FRAM_GLOBAL_PARAM',
        'LOG_ERR_SAMAPHORE_GLOBAL_PARAM',
        'LOG_ERR_SAVE_HK',
        'LOG_ERR_SEMAPHORE_SD',
        'LOG_ERR_SEMAPHORE_CMD',
        'LOG_ERR_READ_SD_TLM'
    ]
    log_errors_COMM = [
        'LOG_ERR_FRAM_WRITE_',
        'LOG_ERR_FRAM_READ_',
        'LOG_ERR_GET_TIME_',
        'LOG_ERR_SET_TIME_',
        'LOG_ERR_DELETE_TM_',
        'LOG_ERR_DELETE_FILES_',
        'LOG_ERR_COMM_SET_BIT_RATE',
        'LOG_ERR_COMM_IDLE',
        'LOG_ERR_COMM_INIT_TRXVU',
        'LOG_ERR_COMM_SEMAPHORE_TRANSMITTING',
        'LOG_ERR_COMM_DUMP_QUEUE',
        'LOG_ERR_COMM_TRANSPONDER_QUEUE',
        'LOG_ERR_COMM_BEACON_TASK',
        'LOG_ERR_COMM_COUNT_FRAME',
        'LOG_ERR_COMM_READ_TRXVU_STATE',
        'LOG_ERR_COMM_SEND_FRAME',
        'LOG_ERR_COMM_RECIVE_FRAME',
        'LOG_ERR_COMM_GET_TLM',
        'LOG_ERR_COMM_TRANSPONDER_GET_TIME',
        'LOG_ERR_COMM_TRANSPONDER_FRAM_READ',
        'LOG_ERR_COMM_TRANSPONDER_FRAM_WRITE',
        'LOG_ERR_COMM_FRAM_READ_BITRATE',
        'LOG_ERR_COMM_FRAM_READ_BEACON',
        'LOG_ERR_COMM_FRAM_RESET_VALUE',
        'LOG_ERR_I2C_TRANSPONDER',
        'LOG_ERR_I2C_TRANSPONDER_RSSI',
        'LOG_ERR_COMM_DELAYED_COMMAND_GET_TIME',
        'LOG_ERR_COMM_DELAYED_COMMAND_FRAM_WRITE',
        'LOG_ERR_COMM_DELAYED_COMMAND_FRAM_READ',
        'LOG_ERR_COMM_DUMP_ENTER_FS',
        'LOG_ERR_COMM_DUMP_READ_FS'
    ]
    log_errors_ANTS = [
        'LOG_ERR_FRAM_WRITE__',
        'LOG_ERR_FRAM_READ__',
        'LOG_ERR_GET_TIME__',
        'LOG_ERR_SET_TIME__',
        'LOG_ERR_DELETE_TM__',
        'LOG_ERR_DELETE_FILES__',
        'LOG_ERR_INIT_ANTS',
        'LOG_ERR_ARM_ANTS_A',
        'LOG_ERR_ARM_ANTS_B',
        'LOG_ERR_DEPLOY_ANTS',
        'LOG_ERR_READ_FRAM_ANTS',
        'LOG_ERR_WRITE_FRAM_ANTS',
        'LOG_ERR_GET_TIME_ANTS',
        'LOG_ERR_RESET_FRAM_ANTS',
        'LOG_ERR_ANTS_GET_TLM_A',
        'LOG_ERR_ANTS_GET_TLM_B',
    ]
    log_errors_EPS = [
        'LOG_ERR_FRAM_WRITE___',
        'LOG_ERR_FRAM_READ___',
        'LOG_ERR_GET_TIME___',
        'LOG_ERR_SET_TIME___',
        'LOG_ERR_DELETE_TM___',
        'LOG_ERR_DELETE_FILES___',
        'LOG_ERR_EPS_GRD_WDT',
        'LOG_ERR_EPS_FRAM_OVERRIDE_VALUE',
        'LOG_ERR_EPS_UPDATE_POWER_LINES',
        'LOG_ERR_EPS_WRITE_STATE',
        'LOG_ERR_EPS_RESET_FRAM',
        'LOG_ERR_EPS_READ_VOLTAGE_TABLE',
        'LOG_ERR_EPS_GET_TLM',
        'LOG_ERR_EPS_FRAM_ALPHA',
        'LOG_ERR_EPS_SP_WAKE',
        'LOG_ERR_EPS_SP_SLEEP',
        'LOG_ERR_EPS_SP_COLLECT_TEMP',
        'LOG_ERR_EPS_VOLTAGE'
    ]
    log_errors_PAYLOAD = [
        'DataBaseSuccess',
        'DataBaseNullPointer',
        'DataBaseNotInSD',
        'DataBaseRawDoesNotExist',
        'DataBasealreadyInSD',
        'DataBaseIllegalId',
        'DataBaseIdNotFound',
        'DataBaseFull',
        'DataBaseJpegFail',
        'DataBaseAlreadyMarked',
        'DataBaseTimeError',
        'DataBaseFramFail',
        'DataBaseFileSystemError',
        'DataBaseFail',
        'DataBaseAdcsError_gettingAngleRates',
        'DataBaseAdcsError_gettingEstimatedAngles',
        'DataBaseAdcsError_gettingCssVector',
        'GECKO_Take_Success',
        'GECKO_Take_Error_TurnOffSensor',
        'GECKO_Take_Error_Set_ADC_Gain',
        'GECKO_Take_Error_Set_PGA_Gain',
        'GECKO_Take_Error_setExposure',
        'GECKO_Take_Error_setFrameAmount',
        'GECKO_Take_Error_setFrameRate',
        'GECKO_Take_Error_turnOnSensor',
        'GECKO_Take_sensorTurnOnTimeout',
        'GECKO_Take_trainingTimeout',
        'GECKO_Take_trainingError',
        'GECKO_Take_Error_notInitialiseFlash',
        'GECKO_Take_Error_setImageID',
        'GECKO_Take_Error_disableTestPattern',
        'GECKO_Take_Error_startSampling',
        'GECKO_Take_samplingTimeout',
        'GECKO_Take_Error_clearSampleFlag',
        'GECKO_Take_Error_turnOfSensor',
        'GECKO_Read_Success',
        'GECKO_Read_Error_InitialiseFlash',
        'GECKO_Read_Error_SetImageID',
        'GECKO_Read_Error_StartReadout',
        'GECKO_Read_readTimeout',
        'GECKO_Read_wordCountMismatch',
        'GECKO_Read_pageCountMismatch',
        'GECKO_Read_readDoneFlagNotSet',
        'GECKO_Read_Error_ClearReadDoneFlag',
        'GECKO_Read_CouldNotReadStopFlag',
        'GECKO_Read_StoppedAsPerRequest',
        'GECKO_Erase_Success',
        'GECKO_Erase_Error_SetImageID',
        'GECKO_Erase_StartErase',
        'GECKO_Erase_Timeout',
        'GECKO_Erase_Error_ClearEraseDoneFlag',
        'Butcher_Success',
        'Butcher_Null_Pointer',
        'Butcher_Parameter_Value',
        'Butcher_Out_of_Bounds',
        'Butcher_Undefined_Error',
        'JpegCompression_Success',
        'JpegCompression_Failure',
        'JpegCompression_qualityFactor_outOfRange',
    ]

    log_errors_CUF_num = [
        165,
        166,
        167,
        168,
        169,
        170,
        171,
        172,
        173
    ]
    log_errors_OBC_num = [
        0,
        1,
        2,
        3,
        4,
        5,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
    ]
    log_errors_COMM_num = [
        0,
        1,
        2,
        3,
        4,
        5,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        50,
        51,
        52,
        53,
        54,
    ]
    log_errors_ANTS_num = [
        0,
        1,
        2,
        3,
        4,
        5,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
    ]
    log_errors_EPS_num = [
        0,
        1,
        2,
        3,
        4,
        5,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
    ]
    log_errors_PAYLOAD_num = range(0, 59)

    if (offset_number*0 <= input_number < offset_number):
        system_name = 'TRXVU'
        system_log = input_number - offset_number*0
        log = log_errors_COMM[log_errors_COMM_num.index(system_log)]

    elif (offset_number*1 <= input_number < offset_number*2):
        system_name = 'EPS'
        system_log = input_number - offset_number
        log = log_errors_EPS[log_errors_EPS_num.index(system_log)]

    elif (offset_number*2 <= input_number < offset_number*3):
        system_name = 'Payload'
        system_log = input_number - offset_number*2
        log = log_errors_PAYLOAD[log_errors_PAYLOAD_num.index(system_log)]

    elif (offset_number*3 <= input_number < offset_number*4):
        system_name = 'Payload Automatic Image Handler'
        system_log = input_number - offset_number*3
        log = log_errors_PAYLOAD[log_errors_PAYLOAD_num.index(system_log)]

    elif (offset_number*4 <= input_number < offset_number*5):
        system_name = 'OBC'
        system_log = input_number - offset_number*4
        log = log_errors_OBC[log_errors_OBC_num.index(system_log)]

    elif (offset_number*5 <= input_number < offset_number*6):
        # Well  you see ADCS decided to use the event log as their error log...
        #system_name = 'ADCS'
        #system_log = input_number - offset_number*6
        #log = log_errors_ADCS[log_errors_ADCS_num.index(system_log)]
        system_name = None
        log = None

    elif (offset_number*6 <= input_number < offset_number*7):
        system_name = 'ANTS'
        system_log = input_number - offset_number*7
        log = log_errors_ANTS[log_errors_ANTS_num.index(system_log)]

    elif (offset_number*7 <= input_number < offset_number*8):
        system_name = 'CUF'
        system_log = input_number - offset_number*8
        log = log_errors_CUF[log_errors_CUF_num.index(system_log)]

    else:
        system_name = None
        log = None

    return [system_name, log]


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
         pass #print("-E-\t Error ("") at file: "+path)
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
    second = date[17:19]

    return str(day)+'/'+str(month)+'/'+str(year)+' '+str(hour)+':'+str(minute)+':'+str(second)


def GetSatTime(file_name):
    index = file_name.find('SATTIME-') + len('SATTIME-')
    end_index = index + len("2019-10-29@19-01-20")

    return ConvertDateFromFileNameFormatToNormal(file_name[index:end_index])


def GetGroundTime(file_name):
    index = file_name.find('GTIME-') + len('GTIME-')
    end_index = index + len("2019-10-29@19-01-20")

    return ConvertDateFromFileNameFormatToNormal(file_name[index:end_index])


def getColor(directory):
    if directory == config["eventLogsFolderPath"]:
        return "blue white-text"
    return "red white-text"


def ParseAllLogFilesInDirectory(directory, logFileParsingFunction):
    output = []

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            log = ParseLogFile(os.path.join(
                directory, filename), logFileParsingFunction)
            rowDict = {}
            if not log == None:
                rowDict["System"] = (log[0])
                rowDict["Log Type"] = (log[1])
                rowDict["Data"] = (log[2])
                rowDict["Sat Time"] = (GetSatTime(filename))
                rowDict["Ground Time"] = (GetGroundTime(filename))
                rowDict["Color"] = getColor(directory)
                output.append(rowDict)

    return output
