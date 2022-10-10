"""
EM310 Commands:
    SET_REPORTING_INTERVAL
        Parameter: Unused
        Value: 1200 (Seconds)
        Example:
            "command": "SET_REPORTING_INTERVAL",
            "parameter": "",
            "value": "1200"
            ****Set reporting interval to 20min
""" 

from enum import Enum

########################################
######## DEFINITIONS
########################################

DEVICE_MODEL_EM310 = 'EM310'

# Global
class global_par(Enum): 
    CHANNEL = 'ff'
    DISABLE = '00'
    ENABLE = '01'
    RESERVED = 'ff'

# Type commands
class type_commands(Enum):    
    SET_REPORTING_INTERVAL = '03'

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

########################################
######## ENCODE
########################################

def encode_EM310(command='',parameter='',value=''):
    if (command == type_commands.SET_REPORTING_INTERVAL.name):
        return func_set_reporting_interval(value)
    
    else:
        raise NameError("No valid commmand")
    
# Add to handle the model and the encode function
EM310_DEVICE_HANDLE = [DEVICE_MODEL_EM310,encode_EM310]