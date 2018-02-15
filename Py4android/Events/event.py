import os
import re

class TouchEvent(object):

    def __init__(self,*args,**kw):
        pass
    
    def _run(self,command):
        '''用来执行命令'''
        return os.popen('adb {}'.format(command)).read()
    
    def getdisplay(self):
        '''获取显示分辨率值'''
        return re.findall(r'\d+',self._run('shell wm size'))

    def click(self,coordinate:tuple,times=1,callback:"function"=None):
        '''点击，默认点击一次'''
        if coordinate:
            for i in range(int(times)):
                self._run('shell input tap {} {}'.format(*coordinate))
            if callback:
                callback()
    
    def up_slide(self,x:int or float=None,y:int or float=None):
        '''上滑滑动时间不能太小，不然时间不够滑动的，就变成点击了'''
        if not (x or y):
            x,y = list(map(lambda x:int(x)/2.0,self.getdisplay()))
        self._run('shell input swipe {} {} {} {} 200'.format(*(x,y),*(x,y/2.0)))
    
    def down_slide(self,x:int or float=None,y:int or float=None):
        '''下滑'''
        if not (x or y):
            x,y = list(map(lambda x:int(x)/2.0,self.getdisplay()))
        self._run('shell input swipe {} {} {} {} 200'.format(*(x,y),*(x,y*2.0)))
    
    def left_slide(self,x:int or float=None,y:int or float=None):
        '''左滑动'''
        if not (x or y):
            x,y = list(map(lambda x:int(x)/2.0,self.getdisplay()))
        self._run('shell input swipe {} {} {} {} 200'.format(*(x,y),*(x/2.0,y)))
    
    def right_slide(self,x:int or float=None,y:int or float=None):
        '''右滑动'''
        if not (x or y):
            x,y = list(map(lambda x:int(x)/2.0,self.getdisplay()))
        self._run('shell input swipe {} {} {} {} 200'.format(*(x,y),*(x*2.0,y)))
    
    def home(self):
        '''Home键'''
        self._run('shell input keyevent 3')
    
    def back(self):
        '''返回键'''
        self._run('shell input keyevent 4')
    
    def menu(self):
        '''菜单键'''
        self._run('shell input keyevent 1')
    
    def delete(self,times:int=1):
        for i in range(times):

            self._run('shell input keyevent 67')
    
    def input_text(self,text:str):
        self._run('shell input text "{}"'.format(text))