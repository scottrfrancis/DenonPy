#!/usr/bin/python

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import DenonProtocol
import DenonSerial
import Shadow

import argparse
from datetime import datetime
import json
import logging
import time



# Read in command-line parameters
parser = argparse.ArgumentParser()
# IOT args
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-n", "--thingName", action="store", dest="thingName", default="Bot", help="Targeted thing name")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="SeriAlexa", help="Targeted client id")

# serial port args
parser.add_argument("-p", "--port", action="store", required=True, dest="port", default="/dev/ttyUSB0", help="Serial Port Device")
parser.add_argument("-t", "--timeout", action="store", required=True, dest="timeout", default="0.5", help="Timeout to wait for events")
parser.add_argument("-q", "--query", action="store", dest="query", default="['Mute','Power','Video','Volume','Input']", help="Inital queries to kick things off")


args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
thingName = args.thingName
clientId = args.clientId

port = args.port
timeout = float(args.timeout)
query = eval(args.query)


if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# setup serial & protocol
connection = DenonSerial.DenonSerial(port)
protocol = DenonProtocol.DenonProtocol()

# Custom Shadow callback
def customShadowCallback_Update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("payload: " + json.dumps(payloadDict)) #["state"]["desired"]["property"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

# def customShadowCallback_Delete(payload, responseStatus, token):
#     if responseStatus == "timeout":
#         print("Delete request " + token + " time out!")
#     if responseStatus == "accepted":
#         print("~~~~~~~~~~~~~~~~~~~~~~~")
#         print("Delete request with token: " + token + " accepted!")
#         print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
#     if responseStatus == "rejected":
#         print("Delete request " + token + " rejected!")

class shadowCallbackContainer:
    def __init__(self, deviceShadowInstance):
        self.deviceShadowInstance = deviceShadowInstance

    # Custom Shadow callback
    def customShadowCallback_Delta(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        print("Received a delta message:")
        payloadDict = json.loads(payload)
        deltaMessage = json.dumps(payloadDict["state"])
        print(deltaMessage + "\n")

        commands = protocol.makeCommands(payloadDict["state"])
        connection.send(commands)


        # print("Request to update the reported state...")
        # newPayload = '{"state":{"reported":' + deltaMessage + '}}'
        # self.deviceShadowInstance.shadowUpdate(newPayload, None, 5)
        # print("Sent.")


# Init AWSIoTMQTTShadowClient
myAWSIoTMQTTShadowClient = None
if useWebsocket:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId, useWebsocket=True)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTShadowClient configuration
myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
myAWSIoTMQTTShadowClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

# Delete shadow JSON doc
# deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

shadowCallbackContainer_Bot = shadowCallbackContainer(deviceShadowHandler)


# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(shadowCallbackContainer_Bot.customShadowCallback_Delta)




def do_something():
    if not connection.isOpen():
        connection.open()

    # listen for status events
    events = connection.listen()
    if protocol.parseEvents(events):
        # print "\n\nEvents: " + str(events) + "\n\n"
        state = protocol.getState()
        # print str(datetime.now()) + " - " + json.dumps(state)
        deviceShadowHandler.shadowUpdate(Shadow.makeStatePayload(state), customShadowCallback_Update, 5)



def run():
    if not connection.isOpen():
        connection.open()

    # query status ONCE to start
    connection.send(protocol.makeQuery(query))

    while True:
        time.sleep(0.9*timeout)         # crude approach to timing adjustment
        do_something()

if __name__ == "__main__":

    # do_something(connection, protocol)
    run()
