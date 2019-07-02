DenonPy
=======

Serial control of Denon Receiver using Python. Implements an AWS IoT Thing that updates the device shadow and takes updates from Delta messages. **Python 3**

Objective
---------

Create scripts to control and record status of a Denon AVR 2308ci receiver. [Denon Command Protocol](https://usa.denon.com/us/product/HomeTheater/receivers/AVR2308CI?docname=AVR-2308CISerialProtocol_Ver540.pdf\)

See [the blog](https://scottrfrancis.wordpress.com/2017/12/10/adding-alexa-to-an-old-av-receiver/) about this project.

Environment
-----------

Denon AVR2308CI Raspberry Pi 2 [PL2303 USB Serial Adapter](https://www.amazon.com/gp/product/B0758B6MK6/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1\)

Design
------

The concerns of dealing with the Serial port and the Denon Command Protocol are separated in to two Objects: DenonSerial.py and DenonProtocol.py.

*DenonSerial.py*
Handles all the Denon-specific serial formatting (e.g. speed, format, etc.) in such a way that this Object could be replaced if the transport were different (say serial port-forwarding over IP) in the future. A nice extension would be to define an interface or mix-in for this to really facilitate proper extension, but I felt this was already overkill for the problem at hand.

In the Denon Control Protocol, "EVENTS" are emitted by the receiver when all kinds of things happen -- remote control operation as well as response to serial commands. "COMMANDS" are sent to the AVR. Thus, the two event streams (commands and events) are somewhat independent in that commands can be sent anytime and that events may be emitted in any order.

*DenonProtocol.py*
Handles the translation of the various short strings and codes of the protocol to more usuable formats (e.g. 'PW' <=> 'Power'). Provides methods to create query commands that can be used to force the emission of events with current state from the receiver. *NB*- these queries are parameter-specific.

The Protocol object maintains an internal state model of the receiver that can be retieved with the getState() method. This internal model is updated by passing an event stream to the parseEvents() method.

*denon-control.py* Orchestrates the event and command flow between the transport (DenonSerial) and protocol (DenonProtocol) objects. This module also implements the AWS IoT Thing.

_TODO_: 

[ ] while this program will connect to a greengrass server with correct endpoint and credentials, a good improvement would be to implement the Greengrass Discovery Protocol so that power outages could be better tolerated.

[ ] There also exists a race condition on bootup for this script and Greengrass itself.  If GG isn't up, this script will error out.  A better solution would be retry and/or fallback.

Setup
-----

*pyserial*

`pip3 install pyserial`

*AWSIoTPythonSDK*

`pip3 install AWSIoTPythonSDK`

Usage
-----

See start.sh for example invocation. Be sure to supply the appropriate endpoint, certificates, serial port, etc. Available options are near the top of denon-control.py. *NB*- if using Greengrass, provide the IP as endpoint and the appropriate root-ca for the GGC.
