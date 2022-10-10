import os
import boto3
import codecs
import json
from encode.AM100 import AM100_DEVICE_HANDLE
from encode.VS121 import VS121_DEVICE_HANDLE
from encode.WS302 import WS302_DEVICE_HANDLE
from encode.WS301 import WS301_DEVICE_HANDLE
from encode.EM310 import EM310_DEVICE_HANDLE

# List of models and encode handlers
listModels = [
    AM100_DEVICE_HANDLE,
    VS121_DEVICE_HANDLE,
    WS302_DEVICE_HANDLE,
    WS301_DEVICE_HANDLE,
    EM310_DEVICE_HANDLE
]

def lambda_handler(event, context):
    
    payload=''

    # Get data
    #string_data=event
    id_group = string_data["encodeDownlink"]["id_group"]
    id_device = string_data["encodeDownlink"]["id_device"]
    device_model = string_data["encodeDownlink"]["device_model"]
    port = string_data["encodeDownlink"]["port"]
    command = string_data["encodeDownlink"]["command"]
    parameter = string_data["encodeDownlink"]["parameter"]
    value = string_data["encodeDownlink"]["value"]

    # Search model and execute the encode
    for deviceHandler in listModels:
        model = deviceHandler[0]
        encode_function = deviceHandler[1]
        # Make payload to send
        if device_model == deviceHandler[0]:
            payload = encode_function(command=command,parameter=parameter,value=value)

    # Check payload
    if(payload==''):
        raise NameError("No valid model device")

    print(payload)

    # hex string to base64
    payload64 = str(codecs.encode(codecs.decode(payload, 'hex'), 'base64').decode()).replace("\n", "");  
    print(payload64)

    # Send Data
    # Is a single device.
    if (id_group == ""):
        # Send to device
        response = iotwireless.send_data_to_wireless_device(
            Id=id_device,
            TransmitMode=1,
            PayloadData=payload64,
            WirelessMetadata={
                'LoRaWAN': {
                    'FPort': port
                }
            }
        )
        print(response)

   
    else:
        # Is a group
        response = iotwireless.send_data_to_multicast_group(
            Id=id_group,
            PayloadData=payload64,
            WirelessMetadata={
                'LoRaWAN': {
                    'FPort': port
                }
            }
        )
        print(response)

    #End
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
