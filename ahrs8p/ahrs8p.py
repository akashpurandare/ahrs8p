#!/usr/bin/env python

#Import any external libraries here
import serial
import pika
import asvprotobuf.sensor_pb2
import time
import sys
import asvmq

class IMUSerial(object):
    def __init__(self, port="/dev/ttyUSB0", topic_name="/imu_raw", queue_size=1000):
        self.port = serial.Serial(port, baudrate=115200)
        self.publisher = asvmq.Publisher(topic_name, asvprotobuf.sensor_pb2.Raw, hostname="localhost", port=4369)

    def query_data(self):
        self.port.write("quaternion di. accelp di. gyrop di. temperature di.\r\n")


        lines = []
        for i in range(100):
            line = self.port.readline()
            if "OK" in line:

                msg = asvprotobuf.sensor_pb2.Raw()
                t=time.time()
                msg.header.stamp.seconds = int(t)
                msg.header.stamp.nanos=(t%1)*(10**9)
                msg.header.frame_id = "base_link"
                msg.data = "".join(lines)
                return msg
            lines.append(line)
        return asvprotobuf.sensor_pb2.Raw()

    def publish(self):
        while True:
            self.publisher.publish(self.query_data())


if __name__=="__main__":
    port = sys.argv[1]
    ser = IMUSerial(port=port)
    print(ser.query_data())