import serial

class Imu:
    def __init__(self, port):
        self._port_name = port
        self._port=None

    def connect(self):
        self._port=serial.Serial(self._port_name, baudrate=115200)
        return self._port.is_open

    def read(self):
        if (not self._port or not self._port.is_open):
            self.connect()
        self._port.write("roll di. pitch di. yaw di. accelp di. gyrop di. temperature di.\r\n".encode())
        result = []
        while(True):
            line=self._port.readline().decode().strip()
            if(line.startswith("OK")):
                return "\n".join(result)
            result.append(line)
