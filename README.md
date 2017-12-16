DenonPy
=======

Serial control of Denon Receiver using Python

Objective
---------

Create scripts to control and record status of a Denon AVR 2308ci receiver. (Denon Command Protocol)[https://usa.denon.com/us/product/HomeTheater/receivers/AVR2308CI?docname=AVR-2308CISerialProtocol_Ver540.pdf\]

Environment
-----------

Denon AVR2308CI Raspberry Pi 2 (PL2303 USB Serial Adapter)[https://www.amazon.com/gp/product/B0758B6MK6/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1\]

Design
------

*Daemon* One daemon to read the serial port from the AVR, parsing status codes and updating

*/var/denon.json* parsing the text Denon status into a more human readable json format

*denon-control* command to take a control argument in a similar format to the status JSON above and command the AVR
