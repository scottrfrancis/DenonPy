#!/usr/bin/python3

import DenonProtocol
import DenonSerial

import argparse
import logging
import RPi.GPIO as GPIO
import time


# Read in command-line parameters
parser = argparse.ArgumentParser()

# serial port args
parser.add_argument("-p", "--port", action="store", required=True, dest="port", default="/dev/ttyUSB0", help="Serial Port Device")
parser.add_argument("-t", "--timeout", action="store", required=True, dest="timeout", default="0.5", help="Timeout to wait for events")
# parser.add_argument("-q", "--query", action="store", dest="query", default="['Mute','Power','Video','Volume','Input']", help="Inital queries to kick things off")
parser.add_argument("-g", "--gpio", action="store", required=True, dest="pinNumber", help="GPIO Pin Number in BCM numbering")

args = parser.parse_args()
pinNumber = int(args.pinNumber)
port = args.port
timeout = float(args.timeout)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

logger.info("triggering on GPIO" + str(pinNumber))
logger.info("Denon on port " + str(port))

# setup serial & protocol
connection = DenonSerial.DenonSerial(port)
protocol = DenonProtocol.DenonProtocol()

# setup gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



def turn_on(channel):
    logger.info("Turning AVR ON")
    commandDict =   {
                        "Power": "ON"
                        # ,"Input": "TVCBL"
                    }
    connection.send( protocol.makeCommands(commandDict) )

def turn_off(channel):
    logger.info("Turning AVR OFF")
    commandDict =   {
                        "Power": "STANDBY"
                        # ,"Input": "TVCBL"
                    }
    connection.send( protocol.makeCommands(commandDict) )


def edge_handler(channel):
    logger.info("got edge on GPIO" + str(channel) + " state is " + str(GPIO.input(channel)))
    time.sleep(0.1)
    logger.info("after a second read, state is " + str(GPIO.input(channel)))
    if GPIO.input(channel):
        turn_on(channel)
    else:
        turn_off(channel)

# trigger on BOTH edges and use logic sense to dispatch ON/OFF
GPIO.add_event_detect(pinNumber, GPIO.BOTH, callback=edge_handler, bouncetime=1000)

def do_something():
    if not connection.isOpen():
        connection.open()

    # listen for status events
    events = connection.listen()
    if protocol.parseEvents(events):
        print( "\n\nEvents: " + str(events) + "\n\n" )

def run():
    while True:
        time.sleep(0.9*timeout)         # crude approach to timing adjustment
        do_something()

if __name__ == "__main__":
    run()
