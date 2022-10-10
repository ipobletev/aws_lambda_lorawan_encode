"""
WS302 Commands:
    SET_REPORTING_INTERVAL
        Parameter: Unused
        Value: 1200 (Seconds)
        Example:
            "command": "SET_REPORTING_INTERVAL",
            "parameter": "",
            "value": "1200"
            ****Set reporting interval to 20min
    SET_THRESHOLD_ALARM
        Parameter: Unused
        Value: Threshold value in db
        Example:
            "command": "SET_THRESHOLD_ALARM",
            "parameter": "",
            "value": "65"
             ***Set threshold alarm to 65db
    LED_INDICATOR
        Parameter: Unused
        Value: 
            DISABLE
            ENABLE
        Example:
            "command": "LED_INDICATOR",
            "parameter": "",
            "value": "ENABLE"
             ***Enable led indicator
    SET_WEIGHTING_MODE
        Parameter:
            A_WEIGHTING
            C_WEIGHTING
        Value:
            DISABLE_TIME_WEIGHT
            ENABLE_FAST_TIME_WEIGHT
        Example:
            "command": "SET_WEIGHTING_MODE",
            "parameter": "A_WEIGHTING",
            "value": "ENABLE_FAST_TIME_WEIGHT"
             ***Enable fast time weighting in A weighting
    REBOOT_DEVICE
        Parameter: Unused
        Value: Unused
        Example:
            "command": "REBOOT_DEVICE",
            "parameter": "",
            "value": ""
             ***Reboot device
""" 

from enum import Enum

########################################
######## DEFINITIONS
########################################

DEVICE_MODEL_WS302 = 'WS302'

# Global
class global_par(Enum): 
    CHANNEL = 'ff'
    DISABLE = '00'
    ENABLE = '01'
    RESERVED = 'ff'
    
# Type commands
class type_commands(Enum):    
    SET_REPORTING_INTERVAL = '03'
    SET_THRESHOLD_ALARM = '06'
    LED_INDICATOR = '2f'
    SET_WEIGHTING_MODE = '5d'
    REBOOT_DEVICE = '10'

# Set weighting mode
class setweightingmode_param(Enum):    
    A_WEIGHTING = '01'
    C_WEIGHTING = '02'
class setweightingmode_value(Enum):  
    DISABLE_TIME_WEIGHT = '00'
    ENABLE_FAST_TIME_WEIGHT = '01'

# Reboot Reserved (REBOOT)
RESERVED_REBOOT = 'ff'

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

def func_set_reporting_interval(value):
    
    # Hex convert
    str_hex = int2Hex_invert(int(value))
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.SET_REPORTING_INTERVAL.value) + str_hex
    return payload

    """
    Function for 
    
    value: integer decibel value (db) (2 bytes)
    return: String hex payload
    """ 
def func_set_threshold_alarm(value):
    
    # Hex convert
    str_hex = int2Hex_invert(int(value)*10)

    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.SET_THRESHOLD_ALARM.value) + "0a0000" + str_hex
    return payload

def func_led_indicar(value):
    
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.LED_INDICATOR.value) + str(value)
    return payload

def func_set_weighting_mode(parameter,value):
    
    # Parameter
    if(parameter == setweightingmode_param.A_WEIGHTING.name):
        parameter = setweightingmode_param.A_WEIGHTING.value
    elif (parameter == setweightingmode_param.C_WEIGHTING.name):
        parameter = setweightingmode_param.C_WEIGHTING.value
    else:
        raise NameError("no valid parameter")
    
    # Value
    if(value == setweightingmode_value.DISABLE_TIME_WEIGHT.name):
        value = setweightingmode_value.DISABLE_TIME_WEIGHT.value
    elif (value == setweightingmode_value.ENABLE_FAST_TIME_WEIGHT.name):
        value = setweightingmode_value.ENABLE_FAST_TIME_WEIGHT.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.SET_WEIGHTING_MODE.value) + str(parameter) + str(value)
    return payload

def func_reboot():
    payload = global_par.CHANNEL.value + str(type_commands.REBOOT_DEVICE.value) + str(RESERVED_REBOOT)
    return payload

########################################
######## ENCODE
########################################

def encode_WS302(command='',parameter='',value=''):
    if (command == type_commands.SET_REPORTING_INTERVAL.name):
        return func_set_reporting_interval(value)
    
    elif (command == type_commands.SET_THRESHOLD_ALARM.name):
        return func_set_threshold_alarm(value)
    
    elif (command == type_commands.LED_INDICATOR.name):
        return func_led_indicar(value)
    
    elif (command == type_commands.SET_WEIGHTING_MODE.name):
        return func_set_weighting_mode(parameter,value)
    
    elif (command == type_commands.REBOOT_DEVICE.name):
        return func_reboot()
    
    else:
        raise NameError("No valid commmand")

# Add to handle the model and the encode function
WS302_DEVICE_HANDLE = [DEVICE_MODEL_WS302,encode_WS302]





    
    
    
    
