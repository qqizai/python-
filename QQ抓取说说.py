#/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import threading
import time
from Queue import Queue
from qzone import Req
from qzone import Shujuku
from qzone import Web
from qzone import G_tk
import chardet
#还差些功能，一个是分布式，一个是Cookie失效的问题，这是没考虑进去的
#在试运行阶段，网址有一次出现了异常，uin不是QQ号而是一串符号
#还有队列异常，理论上来说应该是爬完有回复的朋友，然后爬朋友的朋友，但是发现好像不是这样的
#队列重复的问题，已经做了判断，应该不会出现了，未测试

class Jk(object):

    def __init__(self,user,pw):
        self.user = user
        self.pw = pw
        self.qq = set()
        self.qq.add(self.user)
        self.url = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={qq}&inCharset=utf-8&outCharset=utf-8&hostUin=1175031933&notice=0&sort=0&pos={num}&num=20&cgi_host=http%3A%2F%2Ftaotao.qq.com%2Fcgi-bin%2Femotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={tk}'
        self.que = Queue()
        self.que.put(self.user)
        self.wait = threading.Condition()
        #这里差一个序列化对象，这个队列里的东西不能没有

    def root(self):
        se = Web(self.user,self.pw)
        cookie = se.login()
        G = G_tk()
        tk = G.g_tk(cookie)
        print tk
        return tk,cookie

    def sk(self):
        print self.url.format(qq=self.user,tk=self.root())
        data = Req.requ(self.url.format(qq=self.user,tk=self.root()))
        print da
        if data['msglist']:
            for i in data['msglist']:
                print chardet.detect(i['content'])
                Shujuku.get(content=i['content'],name=data['logininfo']['name'],qq=data['logininfo']['uin'],createdate=i['createTime'])
                if i.has_key('commentlist'):
                    self.qq.add(i['commentlist']['uin'])
                    try:
                        self.que.put(self.qq.pop())
                    except KeyError as e:
                        print '完成'
                    

    def st(self,tk_num,cookie):
        while not self.que.empty():
            number = 0
            print self.que.qsize()
            print len(list(self.qq))
            qq_number = self.que.get()
            #if qq_number in self.qq:
                #continue
            while True:
                request = Req(cookie)
                data = request.requ(self.url.format(qq=qq_number,tk=tk_num,num=number))
                #print data.url
                if data.has_key('msglist'):
                    if data['msglist']:
                        for i in data['msglist']:
                            #data['total']这个是说说的总数量
                            conn = Shujuku()
                            conn.get(content=i['content'],name=data['usrinfo']['name'],qq=data['usrinfo']['uin'],createdate=i['createTime'])
                            if i.has_key('commentlist'):
                                for j in i['commentlist']:
                                    #self.qq.add(j['uin'])
                                    if j['uin'] not in self.qq:
                                        self.qq.add(j['uin'])
                                        self.que.put(j['uin'])
                        number += 20
                    else:
                        #number = 0
                        break
                else:
                    #number =0
                    break
            
        print u'已经没有可以爬取的了'

    def make(self):
        print'start'
        tk,cookie = self.root()
        p = threading.Thread(target=self.st,args=(tk,cookie))
        p.start()
        time.sleep(10)
        #for i in range(10):
            #s = threading.Thread(target=self.st,args=(tk,cookie))
            #s.start()
        p.join()
        #s.join()


qq = Jk(user,password)
qq.make()

#这里如果用if__name__ == "__main__"竟然不运行，好奇怪啊
