import asvmq
import asvprotobuf
import ahrs8p
import time

pub = asvmq.Publisher(topic_name="imu_data", object_type=asvprotobuf.sensor_pb2.Imu)

def callback(data, args):
    t = time.time()
    msg = ahrs8p.parse(data)
    pub.publish(msg)
    print(1/(time.time()-t))

asvmq.Subscriber(topic_name="imu_raw", object_type=asvprotobuf.sensor_pb2.Serial, callback=callback)
