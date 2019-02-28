import serial
import asvprotobuf
import math
import numpy as np
from serial.tools.list_ports import comports
import datetime

def get_ahrs():
    VID = 1027
    PID = 24577
    for port in comports():
        if port.vid == VID and port.pid == PID:
            return port.device
    return ''

def parse(data):
    print(datetime.datetime.fromtimestamp(data.header.stamp.seconds+data.header.stamp.nanos*10**(-9)))
    mystring = [i.split() for i in data.data.split("\n")]
    msg = asvprotobuf.sensor_pb2.Imu()
    msg.header.stamp.seconds = data.header.stamp.seconds
    msg.header.stamp.nanos = data.header.stamp.nanos
    msg.header.frame_id = data.header.frame_id
    msg.orientation.roll = float(mystring[1][2])
    msg.orientation.pitch = float(mystring[2][2])
    msg.orientation.yaw = float(mystring[3][2])
    msg.acceleration.x = float(mystring[4][3])
    msg.acceleration.y = float(mystring[5][1])
    msg.acceleration.z = float(mystring[6][1])
    msg.angular_velocity.x = float(mystring[7][3])
    msg.angular_velocity.y = float(mystring[8][1])
    msg.angular_velocity.z = float(mystring[9][1])
    z_error = [msg.orientation.yaw, msg.orientation.pitch, msg.orientation.roll]
    expected_z = 9.81*math.cos(z_error[1])*math.cos(z_error[2])
    expected_x = 9.81*math.sin(z_error[1])
    expected_y = 9.81*math.sin(z_error[2])
    if(np.sign(expected_z)!=np.sign(msg.acceleration.z)):
        expected_z *= -1
    if(np.sign(expected_x)!=np.sign(msg.acceleration.x)):
        expected_x *= -1
    if(np.sign(expected_y)!=np.sign(msg.acceleration.y)):
        expected_y *= -1
    msg.acceleration.z = float("%f" % (msg.acceleration.z-expected_z))
    msg.acceleration.x = float("%f" % (msg.acceleration.x-expected_x))
    msg.acceleration.y = float("%f" % (msg.acceleration.y-expected_y))
    msg.temperature = float(mystring[-1][2])
    return msg

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
            if(len(line)!=0):
                result.append(line)

    def disconnect(self):
        self._port.close()
