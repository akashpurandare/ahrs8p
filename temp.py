import ahrs8p
import asvmq

pub = asvmq.Publisher(topic_name="imu_raw", object_type=str)
ahrs = ahrs8p.Imu("/dev/tty.usbserial-A5055UXR")
ahrs.connect()
while (True):
    string = ahrs.read()
    pub.publish(string)
