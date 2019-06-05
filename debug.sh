# stop script on error
set -e

printf "\nRunning DenonSerial to Shadow"
python3 denon-control.py -e akavp55t2efxk-ats.iot.us-west-2.amazonaws.com -r certs/root-CA.crt -c certs/23c079a990.cert.pem -k certs/23c079a990.private.key -n "Denon" -p /dev/ttyUSB0 -t 0.5
