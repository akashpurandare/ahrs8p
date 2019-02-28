import ahrs8p
import asvmq
import asvprotobuf
import time
import datetime

try:
    READ_FREQUENCY = 20

    port_name = ahrs8p.get_ahrs()
    if(port_name==''):
        asvmq.log_fatal("IMU Module not found.")
        raise ModuleNotFoundError("IMU Module not found.")
    pub = asvmq.Publisher(topic_name="imu_raw", object_type=asvprotobuf.sensor_pb2.Serial)
    ahrs = ahrs8p.Imu(port_name)
    ahrs.connect()
    while True:
        t = time.time()
        msg = asvprotobuf.sensor_pb2.Serial()
        msg.header.stamp.seconds = int(t)
        msg.header.stamp.nanos = int((t-int(t))*10**9)
        msg.header.frame_id = "imu"
        msg.data = ahrs.read()
        pub.publish(msg)

except KeyboardInterrupt:
    ahrs.disconnect()
    asvmq.log_debug("Closing AHRS Port at %s" % datetime.datetime.now().strftime("%c"))
    print("\nClosing AHRS Port at %s" % datetime.datetime.now().strftime("%c"))
