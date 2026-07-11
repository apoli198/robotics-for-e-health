#!/usr/bin/env python
import rospy

from std_msgs.msg import String

class SoundRecognitionClient:
    
    def __init__(self, node_name):
        self.curr_sounds = []
        rospy.init_node(node_name, anonymous=True)
        self.pub = rospy.Publisher('soundrec_trig', String, queue_size=10)

    def start(self):
        self.curr_sounds = []
        rospy.Subscriber("soundrec", String, self.sub_clbk, queue_size=10)

    def sub_clbk(self, data):
        self.curr_sounds.append(data.data)

    def recognize(self):
        self.pub.publish("start")

    def get_sounds(self):
        return self.curr_sounds

if __name__ == "__main__": 
    src = SoundRecognitionClient()
    src.start("src_client")
    rospy.spin()