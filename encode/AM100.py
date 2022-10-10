"""
AM100 Commands:
    SET_REPORTING_INTERVAL
        Parameter: Unused
        Value: 1200 (Seconds)
        Example:
            "command": "SET_REPORTING_INTERVAL",
            "parameter": "",
            "value": "1200"
            ****Set reporting interval to 20min
    SET_CHANNEL_MASK
        Parameter: Range channels mask
            RANGE_1 - 0-15
            RANGE_2 - 16-31
            RANGE_3 - 32-47
            RANGE_4 - 48-63
            RANGE_5 - 64-79
            RANGE_6 - 80-95
        Value: indicate disable or enable via every bit (2 Bytes String Hex Value)
            0000 -> disable all channels of RANGE_X
        Example:
            "command": "SET_CHANNEL_MASK",
            "parameter": "RANGE_1",
            "value": "FF00"
             ***Disable channel 8-15
    REBOOT_DEVICE
        Parameter: Unused
        Value: Unused
        Example:
            "command": "REBOOT_DEVICE",
            "parameter": "",
            "value": ""
             ***Reboot device
    EN_DIS_SENSOR
        Parameter: Select sensor
            Temperature
            Humidity
            PIR
            Light
            CO2
            TVOC
            Bar_pressure
        Value: 
            ENABLE
            DISABLE
        Example:
            "command": "EN_DIS_SENSOR",
            "parameter": "Humidity",
            "value": "DISABLE"
             ***Disable humidity sensor       
    CALIBRATION_CO2
        Parameter: Select calibration
            FACTORY_CALIBRATION
            MANUAL_CALIBRATION
        Value: Unused
        Example:
            "command": "CALIBRATION_CO2",
            "parameter": "FACTORY_CALIBRATION",
            "value": ""
             ***Calibrate with factory mode  
    SCREEN_DISPLAY
        Parameter: Select display status
            DISABLE_DISPLAY
            ENABLE_DISPLAY
        Value: Unused
        Example:
            "command": "SCREEN_DISPLAY",
            "parameter": "ENABLE_DISPLAY",
            "value": ""
             ***Screen display enable
""" 

from enum import Enum

########################################
######## DEFINITIONS
########################################

DEVICE_MODEL_AM100 = 'AM100'

# Global
class global_par(Enum): 
    CHANNEL = 'ff'
    DISABLE = '00'
    ENABLE = '01'
    RESERVED = 'ff'

# Type commands
class type_commands(Enum):    
    """
    @type_commands
    """    
    SET_REPORTING_INTERVAL = '03'
    SET_CHANNEL_MASK = '05'
    REBOOT_DEVICE = '10'
    EN_DIS_SENSOR = '18'
    CALIBRATION_CO2 = '1a'
    SCREEN_DISPLAY = '2d'

#Channel index range (SET_CHANNEL_MASK)
class channel_index(Enum):
    RANGE_1 = '01' # 0-15
    RANGE_2 = '02' # 16-31
    RANGE_3 = '03' # 32-47
    RANGE_4 = '04' # 48-63
    RANGE_5 = '05' # 64-79
    RANGE_6 = '06' # 80-95

# Reboot Reserved (REBOOT)
RESERVED_REBOOT = 'ff'

# Enable/disable sensor (EN_DIS_SENSOR)
class sensors(Enum):
    Temperature = '01'
    Humidity = '02'
    PIR = '03'
    Light = '04'
    CO2 = '05'
    TVOC = '06'
    Bar_pressure = '07'

# CO2 Calibration feature (CALIBRATION_CO2)
class value_co2_calibration(Enum):
    FACTORY_CALIBRATION = '00'
    MANUAL_CALIBRATION = '03'

# Screen Display (SCREEN_DISPLAY)
class value_screen_display(Enum):
    DISABLE_DISPLAY = '00'
    ENABLE_DISPLAY = '01'

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

def func_reboot():
    payload = global_par.CHANNEL.value + str(type_commands.REBOOT_DEVICE.value) + str(RESERVED_REBOOT)
    return payload

def en_dis_sensor(parameter,value):
    # Sensor
    if(parameter == sensors.Temperature.name):
        parameter = sensors.Temperature.value 
    elif (parameter == sensors.Humidity.name):
        parameter = sensors.Humidity.value 
    elif (parameter == sensors.PIR.name):
        parameter = sensors.PIR.value 
    elif (parameter == sensors.Light.name):
        parameter = sensors.Light.value  
    elif (parameter == sensors.CO2.name):
        parameter = sensors.CO2.value 
    elif (parameter == sensors.TVOC.name):
        parameter = sensors.TVOC.value 
    elif (parameter == sensors.Bar_pressure.name):
        parameter = sensors.Bar_pressure.value 
    else:
        raise NameError("no valid sensor")
        
    # Value
    if(value == global_par.ENABLE.name):
        value = global_par.ENABLE.value
    elif (value == global_par.DISABLE.name):
        value = global_par.DISABLE.value
    else:
        raise NameError("no valid value")
    
    # Make payload
    payload = global_par.CHANNEL.value + str(type_commands.EN_DIS_SENSOR.value) + str(parameter) + str(value)
    return payload

def func_calibration_co2(value):
    # Value
    if(value == value_co2_calibration.FACTORY_CALIBRATION.name):
        value = value_co2_calibration.FACTORY_CALIBRATION.value
    elif (value == value_co2_calibration.MANUAL_CALIBRATION.name):
        value = value_co2_calibration.MANUAL_CALIBRATION.value
    else:
        raise NameError("no valid value")
    
    payload = global_par.CHANNEL.value + str(type_commands.CALIBRATION_CO2.value) + str(value)
    return payload

def func_screen_display(value):
    # Value
    if(value == value_screen_display.ENABLE_DISPLAY.name):
        value = value_screen_display.ENABLE_DISPLAY.value
    elif (value == value_screen_display.DISABLE_DISPLAY.name):
        value = value_screen_display.DISABLE_DISPLAY.value
    else:
        raise NameError("no valid value")
    
    payload = global_par.CHANNEL.value + str(type_commands.SCREEN_DISPLAY.value) + str(value)
    return payload

########################################
######## ENCODE
########################################

def encode_AM100(command='',parameter='',value=''):
    if (command == type_commands.SET_REPORTING_INTERVAL.name):
        return func_set_reporting_interval(value)
    
    elif (command == type_commands.SET_CHANNEL_MASK.name):
        return func_set_channel_mask(parameter,value)
    
    elif (command == type_commands.REBOOT_DEVICE.name):
        
        return func_reboot()
    
    elif (command == type_commands.EN_DIS_SENSOR.name):
        return en_dis_sensor(parameter,value)
    
    elif (command == type_commands.CALIBRATION_CO2.name):
        return func_calibration_co2(value)
    
    elif (command == type_commands.SCREEN_DISPLAY.name):
        return func_screen_display(value)
    
    else:
        raise NameError("No valid commmand")

# Add to handle the model and the encode function
AM100_DEVICE_HANDLE = [DEVICE_MODEL_AM100,encode_AM100]