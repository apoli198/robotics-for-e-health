#!/usr/bin/env python
import sys
import rospy
from project.srv import *

class AudioPlayerClient:

    def play(self, msg):
        rospy.wait_for_service("audio_play")
        try:
            apl = rospy.ServiceProxy('audio_play', AudioPlayer)
            respl = apl(msg)
            return respl.ack
        except rospy.ServiceException as e:
            print("AudioPlayer client exception %s" % e)

def usage():
    return "%s [file_path]" % sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        msg = sys.argv[1]
    else:
        print(usage())
        sys.exit(1)
    
    print("Requesting speech of %s" % msg)
    print("Received %s" % AudioPlayerClient().play(msg))