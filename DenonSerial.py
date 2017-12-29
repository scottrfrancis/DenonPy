import serial



class DenonSerial:
    RECORD_SEPARATOR = '\r'

    def __init__(self, device):
        self.device = device
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port=self.device,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            ,timeout=0.1
            ,write_timeout=0.1
        )

        self.readbuffer = ''


    def open(self):
        self.ser.open()

    def isOpen(self):
        return self.ser.isOpen()

    def send(self, commands):
        self.ser.write(self.RECORD_SEPARATOR.join(commands) + self.RECORD_SEPARATOR)

    def listen(self):
        events = []
        n = self.ser.inWaiting()
        if n > 0:
            self.readbuffer += self.ser.read(n)
            e = self.readbuffer.strip().split(self.RECORD_SEPARATOR)

            if self.readbuffer[-1] == self.RECORD_SEPARATOR:
                events = e
                self.readbuffer = ''
            else:
                events = e[:-1]         # emit the records that are complete
                self.readbuffer = e[-1] # retain the partial ones

        return events
