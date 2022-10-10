"""
VS121 Commands:
    REBOOT_DEVICE
        Parameter: Unused
        Value: Unused
        Example:
            "command": "REBOOT_DEVICE",
            "parameter": "",
            "value": ""
             ***Reboot device
    CONFIRMED_MODE
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "CONFIRMED_MODE",
            "parameter": "",
            "value": "ENABLE"
            ****Enable confirmed mode lorawan
    SET_CHANNEL_MASK
        Parameter: Unused
        Value: Threshold value in db
        Example:
            "command": "SET_THRESHOLD_ALARM",
            "parameter": "",
            "value": "65"
             ***Set threshold alarm to 65db
    ADR
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "ADR",
            "parameter": "",
            "value": "ENABLE"
             ***Enable ADR
    APLICATION_PORT
        Parameter: Unused
        Value: integer aplication port value    
        Example:
            "command": "APLICATION_PORT",
            "parameter": "",
            "value": "84"
             ***Aplication port to 85
    WIFI
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "WIFI",
            "parameter": "",
            "value": "ENABLE"
             ***Enable WIFI
    REGION_PEOPLE_COUNTING
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "REGION_PEOPLE_COUNTING",
            "parameter": "",
            "value": "ENABLE"
             ***Enable people counting
    REGION_PEOPLE_COUNTING_REPORT_REGULARLY
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "REGION_PEOPLE_COUNTING_REPORT_REGULARLY",
            "parameter": "",
            "value": "ENABLE"
             ***Enable people counting report regularly
    REGION_PEOPLE_COUNTING_REPORT_BY_RESULT
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "REGION_PEOPLE_COUNTING_REPORT_BY_RESULT",
            "parameter": "",
            "value": "ENABLE"
             ***Enable poeple counting report by result
    REPORT_BY_RESULT_MODE
        Parameter: Unused
        Value: 
            ZERO_NON_ZERO
            ONCE_RESULT_CHANGE
        Example:
            "command": "REPORT_BY_RESULT_MODE",
            "parameter": "",
            "value": "ONCE_RESULT_CHANGE"
             ***Result if a result change
    LINE_CROSSING_COUNTING
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "LINE_CROSSING_COUNTING",
            "parameter": "",
            "value": "ENABLE"
             ***Enable crossing counter
""" 

from enum import Enum

########################################
######## DEFINITIONS
########################################

DEVICE_MODEL_VS121 = 'VS121'

# Global
class global_par(Enum): 
    CHANNEL = 'ff'
    DISABLE = '00'
    ENABLE = '01'
    RESERVED = 'ff'

# Type commands
class type_commands(Enum):    
    REBOOT_DEVICE = '10'
    CONFIRMED_MODE = '04'
    SET_CHANNEL_MASK = '05'
    ADR = '40'
    APLICATION_PORT = '41'
    WIFI = '42'
    REGION_PEOPLE_COUNTING = '50'
    REGION_PEOPLE_COUNTING_REPORT_REGULARLY = '43'
    REGION_PEOPLE_COUNTING_REPORT_BY_RESULT = '44'
    REPORT_BY_RESULT_MODE = '45'
    LINE_CROSSING_COUNTING = '48'

# Reboot Reserved (REBOOT)
RESERVED_REBOOT = 'ff'

#Channel index range (SET_CHANNEL_MASK)
class channel_index(Enum):
    RANGE_1 = '01' # 0-15
    RANGE_2 = '02' # 16-31
    RANGE_3 = '03' # 32-47
    RANGE_4 = '04' # 48-63
    RANGE_5 = '05' # 64-79
    RANGE_6 = '06' # 80-95

#Report result (REPORT_BY_RESULT_MODE)
class report_result(Enum):
    ZERO_NON_ZERO = '00' # 0-15
    ONCE_RESULT_CHANGE = '01' # 16-31

########################################
######## Utilities ########
########################################

# Integer to hex and revert
def int2Hex_invert(value):
    if(value > 65535 or value < 1):
        raise NameError("no valid value")
        return
    
    hex = format(value, '04x')
    invert_hex = hex[2] + hex[3] + hex[0] + hex[1]
    
    return invert_hex

#print(int2Hex_invert(200))

########################################
######## COMMANDS FUNCTIONS ########
########################################

def func_reboot():
    payload = global_par.CHANNEL.value + str(type_commands.REBOOT_DEVICE.value) + str(RESERVED_REBOOT)
    return payload

def func_confirmed_mode(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.CONFIRMED_MODE.value) + str(value)
    return payload

def func_set_channel_mask(parameter,value):
    """
    Function for 
    
    parameter: @type_commands
    value: string hex value (2 bytes)
    return: String hex payload
    """ 
    # Parameter
    if(parameter == channel_index.RANGE_1.name):
        parameter = channel_index.RANGE_1.value             
    elif (parameter == channel_index.RANGE_2.name):
        parameter = channel_index.RANGE_2.value 
    elif (parameter == channel_index.RANGE_3.name):
        parameter = channel_index.RANGE_3.value 
    elif (parameter == channel_index.RANGE_4.name):
        parameter = channel_index.RANGE_4.value  
    elif (parameter == channel_index.RANGE_5.name):
        parameter = channel_index.RANGE_5.value 
    elif (parameter == channel_index.RANGE_6.name):
        parameter = channel_index.RANGE_6.value 
    else:
        raise NameError("no valid parameter")
    
    # Value
    if((int(value, 16) > 65535) or (int(value, 16) < 0)):
        raise NameError("no valid parameter")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.SET_CHANNEL_MASK.value) + str(parameter) + str(value)
    return payload

def func_adr(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.ADR.value) + str(value)
    return payload

def func_application_port(value):
    
    # Value
    if(int(value) > 255 or int(value) < 1):
        raise NameError("no valid value")
        return
    
    hex_value = format(int(value), '02x')
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.APLICATION_PORT.value) + str(hex_value)
    return payload

def func_wifi(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.WIFI.value) + str(value)
    return payload

def func_region_people_counting(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.REGION_PEOPLE_COUNTING.value) + str(value)
    return payload

def func_region_people_counting_report_regularity(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.REGION_PEOPLE_COUNTING_REPORT_REGULARLY.value) + str(value)
    return payload

def func_region_people_counting_report_by_result(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.REGION_PEOPLE_COUNTING_REPORT_BY_RESULT.value) + str(value)
    return payload

def func_report_by_result_mode(value):
    
    # Value
    if(value == report_result.ZERO_NON_ZERO.name):
        value = report_result.ZERO_NON_ZERO.value
    elif (value == report_result.ONCE_RESULT_CHANGE.name):
        value = report_result.ONCE_RESULT_CHANGE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.REPORT_BY_RESULT_MODE.value) + str(value)
    return payload

def func_line_crossing_counting(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.LINE_CROSSING_COUNTING.value) + str(value)
    return payload

########################################
######## ENCODE
########################################

def encode_VS121(command='',parameter='',value=''):
    if (command == type_commands.REBOOT_DEVICE.name):
        return func_reboot()
    
    elif (command == type_commands.CONFIRMED_MODE.name):
        return func_confirmed_mode(value)
    
    elif (command == type_commands.SET_CHANNEL_MASK.name):
        return func_set_channel_mask(parameter,value)
    
    elif (command == type_commands.ADR.name):
        return func_adr(value)
    
    elif (command == type_commands.APLICATION_PORT.name):
        return func_application_port(value)

    elif (command == type_commands.WIFI.name):
        return func_wifi(value)

    elif (command == type_commands.REGION_PEOPLE_COUNTING.name):
        return func_region_people_counting(value)

    elif (command == type_commands.REGION_PEOPLE_COUNTING_REPORT_REGULARLY.name):
        return func_region_people_counting_report_regularity(value)

    elif (command == type_commands.REGION_PEOPLE_COUNTING_REPORT_BY_RESULT.name):
        return func_region_people_counting_report_by_result(value)

    elif (command == type_commands.REPORT_BY_RESULT_MODE.name):
        return func_report_by_result_mode(value)

    elif (command == type_commands.LINE_CROSSING_COUNTING.name):
        return func_line_crossing_counting(value)
    
    else:
        raise NameError("No valid commmand")
    
# Add to handle the model and the encode function
VS121_DEVICE_HANDLE = [DEVICE_MODEL_VS121,encode_VS121]