import os
import re
import tempfile
import xml.etree.cElementTree as ET
from Events import event
import Axis

class Pc(event.TouchEvent):

    def __init__(self):
        self.services = []
        self._get_androidID()
        self._tempfile = tempfile.gettempdir()
        self._tree = None
    
    def _get_androidID(self):
        data = self.run('devices')
        reg = r'\d{1}.{7}'
        self.services + re.findall(reg,data)
    
    def _element(self,attrib,name,update:bool=False):
        '''返回单个坐标'''
        if update:
            self._tree = self.getTree()
            treeiter = self._tree.iter(tag='node')
        elif self._tree:
            treeiter = self._tree.iter(tag='node')
        else:
            self._tree = self.getTree()
            treeiter = self._tree.iter(tag='node')
        for elem in treeiter:
            if elem.attrib[attrib] == name or name in elem.attrib[attrib]:
                bounds = elem.attrib['bounds']
                coord = re.findall(r'\d+',bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) /2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) /2.0 + int(coord[1])
                return (Xpoint,Ypoint)

    def _elements(self,attrib,name,update:bool=False):
        '''返回多个坐标列表'''
        ls = []
        if update:
            self._tree = self.getTree()
            treeiter = self._tree.iter(tag='node')
        elif self._tree:
            treeiter = self._tree.iter(tag='node')
        else:
            self._tree = self.getTree()
            treeiter = self._tree.iter(tag='node')
        for elem in treeiter:
            if elem.attrib[attrib] == name or name in elem.attrib[attrib]:
                bounds = elem.attrib['bounds']
                coord = re.findall(r'\d+',bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) /2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) /2.0 + int(coord[1])
                ls.append((Xpoint,Ypoint))
        return ls

    def findElementByName(self,name,update=False):
        '''使用属性为text来查找name的元素'''
        return self._element('text',name,update)
    
    # def findElement(self,name,attr:str="content-desc",update:bool=False):
    #     '''使用属性来查找元素'''
    #     if self._tree and update:
    #         treeiter = self._tree.iter(tag='node')
    #     else:
    #         self._tree = self.getTree()
    #         treeiter = self._tree.iter(tag='node')
    #     for elem in treeiter:
    #         if elem.attrib[attr] == name or name in elem.attrib[attr]:
    #             bounds = elem.attrib['bounds']
    #             coord = re.findall(r'\d+',bounds)
    #             Xpoint = (int(coord[2]) - int(coord[0])) /2.0 + int(coord[0])
    #             Ypoint = (int(coord[3]) - int(coord[1])) /2.0 + int(coord[1])
    #             return (Xpoint,Ypoint)
    
    def findElement(self,name,attr:str="content-desc",update:bool=False):
        return self._element(attr,name,update)

    def get(self):
        pass
    
    def getlist(self):
        info = self.run('devices')
        return info
    
    def run(self,command):
        ins = os.popen('adb {}'.format(command))
        return ins.read()
    
    def getTree(self):
        '''获取元素树'''
        self.run('shell uiautomator dump /data/local/tmp/uidump.xml')
        self.run('pull /data/local/tmp/uidump.xml {}'.format(self._tempfile))
        return ET.ElementTree(file=self._tempfile+'\\uidump.xml')
    
    def getScreen(self):
        self.run('shell screencap -p | sed "s/\r$//" >screen.png')


def main():
    android = Pc()
    xy = android.findElement('领取红包',attr='text',update=True)
    android.click(xy)
    xy = android.findElement('android.widget.Button',update=True,attr="class")
    android.click(xy)
    #android.up_slide()
    #android.down_slide()
    #android.left_slide()
    #android.right_slide()
    # xy = android.findElementByName('发送加密消息',update=True)
    # android.click(xy)
    # android.input_text('test')
    # xy = android.findElementByName('发送')
    # android.click(xy)
    android.run('pull /data/local/tmp/uidump.xml c:\\Users\\Administrator\\Desktop')
    

if __name__ == '__main__':
    main()
