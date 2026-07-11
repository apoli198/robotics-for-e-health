#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import rospy
from sound_recognition_client import SoundRecognitionClient
from text2speech_client import Text2SpeechClient

if __name__ == "__main__":
    obj_names = open("/home/mivia/Desktop/medrob_ws/src/project/names.txt").read().splitlines()
    obj_snds = open("/home/mivia/Desktop/medrob_ws/src/project/sounds.txt").read().splitlines()
    obj_lbls = open("/home/mivia/Desktop/medrob_ws/src/project/labels.txt").read().splitlines()
    index = 0
    err_count = 0

    t2s = Text2SpeechClient()
    sr = SoundRecognitionClient("sr_client")

    t2s.say("Ciao! Facciamo un gioco. Pronuncerò il verso di alcuni oggetti e animali, e tu dovrai ripeterli.")
    t2s.say("Avrai cinque secondi per ripetere il verso, e tre tentativi totali. Sei pronto per iniziare?")
    raw_input()
    while index < len(obj_names):
        sr.start()
        sounds = []
        rospy.loginfo("Next object is %s. Hit Enter when you're ready" % obj_names[index])
        raw_input()
        t2s.say(obj_names[index])
        t2s.say(obj_snds[index])
        sr.recognize()
        rospy.loginfo("Waiting for patient's response")
        start_time = time.time()
        rospy.sleep(5)
        rospy.sleep(3) #computing
        
        sounds = sr.get_sounds()
        rospy.loginfo("Timeout of %d seconds expired" % 5)
        rospy.loginfo("Recorded: " + str([x for x in sounds if len(x) > 0]))
        if obj_lbls[index] in sounds:
            rospy.loginfo("Sound is right")
            t2s.say("Bravo!")
            index += 1
            continue
        else:
            err_count += 1
            t2s.say("Peccato! Non era il verso giusto!")
            rospy.loginfo("Sound is wrong, total errors: %d", err_count)

            if err_count > 2:
                rospy.loginfo("Maximum allowed errors reached, exercise failed")
                t2s.say("Non sei riuscito a terminare correttamente l'esercìzio.")
                break

            t2s.say("Riproviamo!")
            continue
    
    # completed correctly
    if err_count < 3:
        rospy.loginfo("Activity completed with success")
        t2s.say("Molto bene!")