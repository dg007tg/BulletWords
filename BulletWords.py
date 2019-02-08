'''
This file define an object to add dan mu to a video stream.
To use this:
1. A stream obejct is needed. The object should have following methods:
    I. read(): return value (ret, frame)
        frame: a frame extrated from video stream
        ret: a boolean to mark whether a frame is successfully read
    II. show():display a frame.
2. A Queue is also needed to pass on texts.
        A text is a dictionary with following elements:
            content: text content in utf-8 bytes
            font, size,
            color: (R,G,B)
            position:(x, y) of left-top origin
        Use gen_text() to get a legal text.
3. Initialize stream and queue and pass them to constructor of BulletWords.
    Then start() of BulletWords object.

4. Additionally, use:
    set_defaut_font()
    set_defaut_size()
    set_defaut_color()
    to modify default settings.

5. use positional value to set frame rate in constructor of BulletWords
    or call set_frame_rate() method.
'''
from multiprocessing import Queue
from queue import Empty
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import threading
import random
import cv2

__DefautFont = "C:\Windows\Fonts\simsun.ttc"
__DefaultColor = (255,197,255)
__DefaultSize = 40

class BulletWords(threading.Thread):
    '''
    Two parameters are needed by constructor.
    @param: video: typically this is similar to a cv2 object.
        It should have read() method to get a frame and show()
        method to display a frame.
    @param: wordQueue: This is a queue to contain dan mu. Each
        element is a dictionary with respect to a piece of dan mu.
        The dic contain contents and some configuration such as
        font, size, speed, etc.
    '''
    def __init__(self, video, wordQueue, frameRate = 25):
        #@param frameRate:frameRate frames will be displayed every second
        super().__init__()
        self.stream = video
        self.height = 0
        self.width = 0
        self.frameRate = frameRate
        self.words = wordQueue
        self.flying = []

    def run(self):
        self.__fire()

    def __fire(self):
        #start displaying the stream and add dan mu on it.
        ret, frame = self.stream.read()
        if(ret):
            self.width, self.height = frame.shape[0:2]
        while(ret):
            for text in self.flying:
                dur = text['duration']
                step = int(self.width / (dur * self.frameRate))
                loc = text['position']
                loc[0] = loc[0] - step
                w, h = text['shape']
                if((loc[0] + w) < 0):
                    self.flying.remove(text)
                else:
                    text['position'] = loc
                    frame = self.__draw_text(frame, text)
                    self.stream.show(frame)

            try:
                text = self.words.get(False)
            except Empty:
                pass
            else:
                pos = text['position']
                if(pos[0] == 0 and pos[1] == 0):
                    pos[0] = self.width
                    pos[1] = random.randint(0, self.height - 150)
                    text['position'] = pos
                frame = self.__draw_text(frame, text)
                self.stream.show(frame)
                self.flying.append(text)

            self.stream.show(frame)
            ret, frame = self.stream.read()

    def __draw_text(self, frame, text):
        #put text onto a frame
        #@param text:a dictionary contains configuration and contents
        #   color should be RGB 3-elements tuple and position should be
        #   2-elements tuple or list
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        font = ImageFont.truetype(text['font'], text['size'])
        draw = ImageDraw.Draw(image)
        draw.text(text['position'], text['content'].decode(), font = font, fill = text['color'])
        if(text['shape'] == None):
            text['shape'] = draw.textsize(text['content'].decode(), font)
        ret_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        return ret_image

    def set_frame_rate(self, rate):
        self.frameRate = rate

def gen_text(content, font = __DefautFont, size = __DefaultSize, color = __DefaultColor,\
        position = [0,0], duration = 3):
    #position:[x, y]
    text = {}
    if not content:
        raise NoContentException
    text['content'] = bytes(content,encoding = "utf-8")
    text['font'] = font
    text['size'] = size
    text['color'] = color
    text['position'] = position
    text['duration'] = duration
    text['shape'] = None
    return text

def set_defaut_font(font):
    global __DefautFont
    __DefautFont = font
    return True

def set_defaut_size(size):
    global __DefaultSize
    __DefaultSize = size
    return True

def set_defaut_color(color):
    global __DefaultColor
    __DefaultColor = color
    return True

class NoContentException(Exception):
    def __init__(self):
        print("Content is needed.")