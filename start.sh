# stop script on error
set -e

printf "\nRunning DenonSerial to Shadow"
# python3 denon-control.py -e a38islc3h7i87s-ats.iot.us-west-2.amazonaws.com -r certs/root-ca-cert.pem -c certs/23c079a990.cert.pem -k certs/23c079a990.private.key -n "Denon" -p /dev/ttyUSB0 -t 0.5
python3 denon-control.py -e a38islc3h7i87s-ats.iot.us-west-2.amazonaws.com -r certs/root-ca-cert.pem -c certs/23c079a990.cert.pem -k certs/23c079a990.private.key -n "Denon" -h "192.168.4.35" -t 0.5
