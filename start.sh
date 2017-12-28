# stop script on error
set -e

# Check to see if root CA file exists, download if not
# if [ ! -f ./root-CA.crt ]; then
#   printf "\nDownloading AWS IoT Root CA certificate from Symantec...\n"
#   curl https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem > root-CA.crt
# fi
#
# # install AWS Device SDK for Python if not already installed
# if [ ! -d ./aws-iot-device-sdk-python ]; then
#   printf "\nInstalling AWS SDK...\n"
#   git clone https://github.com/aws/aws-iot-device-sdk-python.git
#   pushd aws-iot-device-sdk-python
#   python setup.py install
#   popd
# fi

# run pub/sub sample app using certificates downloaded in package
# printf "\nRunning pub/sub sample application...\n"
# python aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py -e a38islc3h7i87s.iot.us-east-1.amazonaws.com -r root-CA.crt -c SeriAlexa-0001.cert.pem -k SeriAlexa-0001.private.key -t "$aws/things/SeriAlexa-0001/foo" -m publish

# printf "\nRunning shadow sample application...\n"
# python basicShadowUpdater.py -e a38islc3h7i87s.iot.us-east-1.amazonaws.com -r certs/root-CA.crt -c certs/SeriAlexa-0001.cert.pem -k certs/SeriAlexa-0001.private.key -n "SeriAlexa-0001"

printf "\nRunning DenonSerial to Shadow"
python denon-control.py -e a38islc3h7i87s.iot.us-east-1.amazonaws.com -r certs/root-CA.crt -c certs/SeriAlexa-0001.cert.pem -k certs/SeriAlexa-0001.private.key -n "SeriAlexa-0001" -p /dev/ttyUSB0 -t 2.0
