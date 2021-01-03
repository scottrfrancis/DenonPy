import telnetlib
import time


class DenonTelnet:
    RECORD_SEPARATOR = '\r'

    def __init__(self, host):
        self.host = host
        self.tn = telnetlib.Telnet()
        self.readbuffer = ''

    def open(self):
        try:
            self.tn.open(self.host)
        except Exception as e:
            pass

    def isOpen(self):
        return self.tn.get_socket() is not None

    def send(self, commands):
        self.tn.write(bytearray(self.RECORD_SEPARATOR.join(commands) + self.RECORD_SEPARATOR, 'ascii'))

    def listen(self):
        events = []
        try:
            self.readbuffer += self.tn.read_very_eager().decode('ascii')
            e = self.readbuffer.strip().split(self.RECORD_SEPARATOR)

            if self.readbuffer[-1] == self.RECORD_SEPARATOR:
                events = e
                self.readbuffer = ''
            else:
                # emit the records that are complete
                events = e[:-1]
                self.readbuffer = e[-1]  # retain the partial ones
        except Exception as e:
            # print("Exception while reading from Telnet")
            pass

        return events

# test stub
if __name__ == "__main__":
    dt = DenonTelnet('192.168.4.35')

    if not dt.isOpen():
        dt.open()

    dt.send(["PW?", "SI?", "MU?", "MV?"])
    while True:
        [ print(e) for e in dt.listen() ]
        time.sleep(1)

