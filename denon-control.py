#!/usr/bin/python

import DenonProtocol
import DenonSerial
import Shadow

import argparse
from datetime import datetime
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
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicShadowUpdater", help="Targeted client id")

# serial port args
parser.add_argument("-p", "--port", action="store", required=True, dest="port", default="/dev/ttyUSB0", help="Serial Port Device")
parser.add_argument("-t", "--timeout", action="store", required=True, dest="timeout", default="0.5", help="Timeout to wait for events")
parser.add_argument("-q", "--query", action="store", dest="query", default="['Mute','Power','Video','Volume']", help="Inital queries to kick things off")


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


def do_something(connection, protocol):
    if not connection.isOpen():
        connection.open()

    # listen for status events
    events = connection.listen(1.0*timeout)

    if protocol.parseEvents(events):
        print str(datetime.now()) + " - " + Shadow.makeStatePayload("reported", protocol.getState())


def run(connection, protocol):
    if not connection.isOpen():
        connection.open()

    # query status ONCE to start
    connection.send(protocol.makeQuery(query))

    while True:
        # time.sleep(0.2*timeout)
        do_something(connection, protocol)

if __name__ == "__main__":
    connection = DenonSerial.DenonSerial(port)
    protocol = DenonProtocol.DenonProtocol()

    # do_something(connection, protocol)
    run(connection, protocol)
