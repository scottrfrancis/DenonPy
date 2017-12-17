#!/usr/bin/python

import time

import DenonProtocol
import DenonSerial


config = {  'port': '/dev/ttyUSB0',
            'whitelist': ['Power'],
            'update': 0.5 }

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0][1:]] = argv[1]
        argv = argv[1:]
    return opts



def do_something(connection, protocol):
    if not connection.isOpen():
        connection.open()

    # query status
    connection.send(protocol.makeQuery(config['whitelist']))

    # TODO: send desired state command

    # listen for status
    events = connection.listen(0.8*config['update'])

    protocol.parseEvents(events)
    print protocol.getState()


def run(connection, protocol):
    while True:
        time.sleep(0.2*config['update'])
        do_something(connection, protocol)

if __name__ == "__main__":
    from sys import argv
    config.update(getopts(argv))
    config['whitelist'] = eval(config['whitelist'])
    config['update'] = float(config['update'])

    connection = DenonSerial.DenonSerial(config['port'])
    protocol = DenonProtocol.DenonProtocol()

    # do_something(connection, protocol)
    run(connection, protocol)
