#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     07/02/2019
# Copyright:   (c) Administrator 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import BulletWords as bw
from multiprocessing import Queue
import cv2

class www:
    def __init__(self):
        self.c = cv2.VideoCapture(0)

    def read(self):
        ret, frame = self.c.read()
        return ret, frame

    def show(self, frame):
        cv2.imshow('Bullet Video', frame)
        cv2.waitKey(1)

def main():
    words = Queue()
    w = bw.gen_text("ha")
    words.put(w)
    camera = www()
    ss = bw.BulletWords(camera, words)
    ss.start()
    while(True):
        w = input()
        if(w == 'q'):
            break
        words.put(bw.gen_text(w))

if __name__ == '__main__':
    main()
