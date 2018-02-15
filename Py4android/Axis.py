from Events import event
import os


class Point(event.TouchEvent):

    def __init__(self,x:int,y:int):
        self._axis = (x,y)
