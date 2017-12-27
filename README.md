DenonPy
=======

Serial control of Denon Receiver using Python

Objective
---------

Create scripts to control and record status of a Denon AVR 2308ci receiver. [Denon Command Protocol](https://usa.denon.com/us/product/HomeTheater/receivers/AVR2308CI?docname=AVR-2308CISerialProtocol_Ver540.pdf\)

See [the blog](https://scottrfrancis.wordpress.com/2017/12/10/adding-alexa-to-an-old-av-receiver/) about this project.

Environment
-----------

Denon AVR2308CI Raspberry Pi 2 [PL2303 USB Serial Adapter](https://www.amazon.com/gp/product/B0758B6MK6/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1\)

Design
------

*Daemon*

One daemon to read the serial port from the AVR, parsing status codes and updating

*/var/denon.json*

parsing the text Denon status into a more human readable json format

*denon-control*

command to take a control argument in a similar format to the status JSON above and command the AVR

Setup
-----

*pyserial*

`pip install pyserial`

Usage
-----

pass parameters you want queried at regular intervals in the `-whitelist` parameter as an array of strings. These settings will be queried every `-update` seconds (*NB* accepts floats). At the end of the update cycle, the complete settings will be dumped as JSON. To suppress output parameters, add them to the `-blacklist` array.

*example*

```
denon-control.py -whitelist ['Power','Mute','Video']  -update 2 -port /dev/ttyUSB0
```
