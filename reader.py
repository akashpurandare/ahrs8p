import ahrs8p
import asvmq
import asvprotobuf
import time

pub = asvmq.Publisher(topic_name="imu_raw", object_type=asvprotobuf.sensor_pb2.Serial)
ahrs = ahrs8p.Imu("/dev/tty.usbserial-A5055UXR")
ahrs.connect()
while (True):
    msg = asvprotobuf.sensor_pb2.Serial()
    t = time.time()
    msg.header.stamp.seconds = int(t)
    msg.header.stamp.nanos = int((t-int(t))*10**9)
    msg.header.frame_id = "imu"
    msg.data = ahrs.read()
    print(msg)
    pub.publish(msg)
