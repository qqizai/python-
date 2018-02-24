#coding:gbk

import pythoncom
import pyHook
import os
from pygame import mixer
import mp3play
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-S',help='''添加一个文件夹路径，里面包含声效wav文件和音乐MP3文件，声效文件名的格式为
    J-abc.wav   前面的J指定的是绑定的按键，如果有多个文件绑定同一个按键，则最后一个有效,音乐文件无格式要求''')
args = parser.parse_args()

class KeyEvent(object):

    def __init__(self):
        self.man = pyHook.HookManager()
        mixer.init()
        self.bgm = []
        self._num = 0
        self._keys = {}
        if args.S:
            self.append(args.S)
        else:
            self._init_()

    
    def _init_(self):
        for i in os.listdir('.'):
            if i.endswith('mp3'):
                self.bgm.append(i)
            elif i.endswith('wav'):
                self._keys[i[0]] = i
    
    def append(self,path):
        if os.path.exists(args.S):
            os.chdir(args.S)
            self._init_()


    def switch(self,key,name,music_name):
        if not os.path.exists(music_name):
            return None
        if key == name:
            mixer.music.load(music_name)
            mixer.music.play()

    def get(self,key):
        if not self.bgm:
            return None
        if key == 'Right':
            self._num += 1
            if self._num > len(self.bgm) -1:
                self._num = 0
            self.bm = mp3play.load(self.bgm[self._num])
            self.bm.play()
        elif key == 'Left':
            self._num -= 1
            if self._num <0:
                self._num = len(self.bgm) -1
            self.bm = mp3play.load(self.bgm[self._num])
            self.bm.play()
        elif key == 'Space':
            if hasattr(self,'bm'):
                if self.bm.isplaying():
                    self.bm.stop()
                else:
                    self.bm.play()
            else:
                return None
    def on_key(self,event):
        print event
        print event.Key
        if self._keys.has_key(event.Key):
            #self.switch(event.Key,'J','jian.wav')
            self.switch(event.Key,event.Key,self._keys[event.Key])
        self.get(event.Key)
        

    def run(self):
        Events = pyHook.HookManager()
        self.man.KeyDown = self.on_key
        self.man.HookKeyboard()
        pythoncom.PumpMessages()



if __name__ == '__main__':

    body = KeyEvent()
    body.run()
