'''
This module is used to interact with AHRS8P provided
by Sparton Nav Ex. This module uses the Northtek commands
over serial port at 115200 BAUD rate to access Database
Variables that store sensory data.
This package also uses Pyserial's autodetect libraries to
automatically detect Serial libraries.
'''
import serial
from serial.tools.list_ports import comports
import asvprotobuf.sensor_pb2
import numpy as np

GRAVITY = 9.80665
WRITE_LINE = "roll di. pitch di. yaw di. accelp di. gyrop di. temperature di.\r\n"
VID = 1027
PID = 24577

def get_ahrs():
    '''This function uses Pyserial library to detect which port AHRS is on'''
    for port in comports():
        if port.vid == VID and port.pid == PID:
            return port.device
    return ''

def parse(data):
    '''This function converts a single IMU output to an ASVProtobuf message'''
    #GPS is North-East-Up while IMU is North-West-Up
    mystring = [i.split() for i in data.data.split("\n")]
    msg = asvprotobuf.sensor_pb2.Imu()
    msg.header.stamp = data.header.stamp
    msg.header.frame_id = data.header.frame_id
    msg.orientation.roll = np.radians(float(mystring[1][2]))
    msg.orientation.pitch = np.radians(float(mystring[2][2]))
    msg.orientation.yaw = np.radians(float(mystring[3][2]))
    msg.angular_velocity.roll = float(mystring[7][3])
    msg.angular_velocity.pitch = float(mystring[8][1])
    msg.angular_velocity.yaw = float(mystring[9][1])
    #Transform acceleration to world frame
    ax = float(mystring[4][3])/100
    ay = float(mystring[5][1])/100
    az = float(mystring[6][1])/100
    z_error = [msg.orientation.yaw, msg.orientation.pitch, msg.orientation.roll]
    expected_z = GRAVITY*np.cos(z_error[1])*np.cos(z_error[2])
    expected_x = GRAVITY*np.sin(z_error[1])
    expected_y = GRAVITY*np.sin(z_error[2])
    if np.sign(expected_z) != np.sign(az):
        expected_z *= -1
    if np.sign(expected_x) != np.sign(ax):
        expected_x *= -1
    if np.sign(expected_y) != np.sign(ay):
        expected_y *= -1
    msg.acceleration.z = round(0.98*az-expected_z, 6)
    ax = round(0.98*ax-expected_x, 6)
    ay = round(0.98*ay-expected_y, 6)
    msg.acceleration.y = ax*np.cos(z_error[0])+ay*np.sin(z_error[0])
    msg.acceleration.x =ax*np.sin(z_error[0])+ay*np.cos(z_error[0])
    #print("%.2f" % (abs(ax)-abs(msg.acceleration.x)))
    msg.temperature = float(mystring[-1][2])
    return msg

class Imu:
    '''
    This class is used to initiate a connection to the AHRS
    and handle all the low level functions.
    '''
    def __init__(self, port):
        '''Initialises the class with Autodetected Port'''
        self._port_name = port
        self._port = None

    def connect(self):
        '''This method opens port to AHRS over serial'''
        self._port = serial.Serial(self._port_name, baudrate=115200, timeout=4)
        return self._port.is_open

    def read(self):
        '''This is used to Read and Write database variables to the AHRS'''
        if (not self._port or not self._port.is_open):
            self.connect()
        self._port.write(WRITE_LINE.encode())
        result = []
        while True:
            line = self._port.readline().decode()
            #if not line.endswith("\r\n"):
            #    asvmq.log_fatal("IMU Could not be read. Reconnecting to module now...")
            line = line.strip()
            if line.startswith("OK"):
                return "\n".join(result)
            if line:
                result.append(line)

    def disconnect(self):
        '''This is used to disconnect and close the serial connections to the AHRS'''
        self._port.close()

    def __del__(self):
        '''Used to safely disconnect and close serial port before garbage collection'''
        self.disconnect()
