#!/usr/bin/python3

import DenonProtocol
import DenonSerial
import DenonTelnet
from GreengrassAwareConnection import *

import argparse
from datetime import datetime
import json
import logging
import time

# remote debug harness -- unco
# import ptvsd
# import socket
# this_ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
# ptvsd.enable_attach(address=(this_ip,3000), redirect_output=True)
# ptvsd.wait_for_attach()
# end debug harness


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

# serial port args
parser.add_argument("-p", "--port", action="store", required=False, dest="port", help="Serial Port Device")
parser.add_argument("-t", "--timeout", action="store", required=False, dest="timeout", default="0.5", help="Timeout to wait for events")

# telnet args
parser.add_argument("-d", "--targetDevice", action="store", required=False, dest="target", help="Target name/IP of AVR")

parser.add_argument("-q", "--query", action="store", dest="query", default="['Mute','Power','Video','Volume']", help="Inital queries to kick things off")


args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
thingName = args.thingName
clientId = args.thingName

port = args.port

target = args.target

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
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# setup serial & protocol
if port is not None:
    connection = DenonSerial.DenonSerial(port)
elif target is not None:
    connection = DenonTelnet.DenonTelnet(target)
protocol = DenonProtocol.DenonProtocol()

iotConnection = GreengrassAwareConnection(host, rootCAPath, certificatePath, privateKeyPath, thingName ) #, deltas)


def do_something():
    if not connection.isOpen():
        connection.open()

    # listen for status events
    events = connection.listen()
    if protocol.parseEvents(events):
        logger.info( "\n\nEvents: " + str(events) + "\n\n" )
        state = protocol.getState()
        logger.info( str(datetime.now()) + " - " + json.dumps(state) )
        try:
            # deviceShadowHandler.shadowUpdate(Shadow.makeStatePayload("reported", state), customShadowCallback_Update, 5)
            iotConnection.publishMessageOnTopic(json.dumps(state), "denon" ) #, qos=1):(Shadow.makeStatePayload("reported", state), customShadowCallback_Update, 5)
        except Exception as e:
            print(e)


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
