import asvmq
import asvprotobuf
import ahrs8p
import time
import datetime

try:
    READ_FREQUENCY = 20

    pub = asvmq.Publisher(topic_name="imu_data", object_type=asvprotobuf.sensor_pb2.Imu)

    def callback(data, args):
        t = time.time()
        msg = ahrs8p.parse(data)
        pub.publish(msg)

    asvmq.Subscriber(topic_name="imu_raw", object_type=asvprotobuf.sensor_pb2.Serial, callback=callback)
    asvmq.spin()

except KeyboardInterrupt:
    asvmq.log_debug("Closing AHRS Parser at %s" % datetime.datetime.now().strftime("%c"))
