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
        if(1/READ_FREQUENCY-time.time()+t>0):
            time.sleep(1/READ_FREQUENCY-time.time()+t)

    asvmq.Subscriber(topic_name="imu_raw", object_type=asvprotobuf.sensor_pb2.Serial, callback=callback)

except KeyboardInterrupt:
    asvmq.log_debug("Closing AHRS Parser at %s" % datetime.datetime.now().strftime("%c"))
    print("\nClosing AHRS Parser at %s" % datetime.datetime.now().strftime("%c"))
