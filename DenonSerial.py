import serial



class DenonSerial:

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

    def open(self):
        self.ser.open()

    def isOpen(self):
        return self.ser.isOpen()

    def send(self, commands):
        self.ser.write("\r".join(commands) + '\r')

    def listen(self, timeout):
        self.ser.timeout = float(timeout)
        return self.ser.read(100*135).strip().split('\r')    # 100 events of max size
