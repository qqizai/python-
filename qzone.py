# -*- coding:utf-8 -*-

import sys
import re
import json
import sqlite3
from selenium import webdriver
import requests
import os
import time
#reload(sys)
#sys.setdefaultencoding('utf8')
import MySQLdb as mysql

class G_tk(object):

    def __init__(self):
        pass

    def LongToInt(self,value):  # 由于int+int超出范围后自动转为long型，通过这个转回来  
        if isinstance(value, int):  
            return int(value)  
        else:  
            return int(value & sys.maxint)
    
    def LeftShiftInt(self,number, step):  # 由于左移可能自动转为long型，通过这个转回来  
        if isinstance((number << step), long):  
            return int((number << step) - 0x200000000L)  
        else:  
            return int(number << step)
        
    def getOldGTK(self,ArithmeticErrorskey):  
        a = 5381  
        for i in range(0, len(skey)):  
            a = a + self.LeftShiftInt(a, 5) + ord(skey[i])  
            a = self.LongToInt(a)  
        return a & 0x7fffffff
    
    def getNewGTK(self,p_skey, skey, rv2):  
        b = p_skey or skey or rv2  
        a = 5381  
        for i in range(0, len(b)):  
            a = a + self.LeftShiftInt(a, 5) + ord(b[i])  
            a = self.LongToInt(a)  
        return a & 0x7fffffff

    def g_tk(self,cookie):
        if re.search(r'p_skey=(?P<p_skey>[^;]*)',cookie):  
            p_skey = re.search(r'p_skey=(?P<p_skey>[^;]*)',cookie).group('p_skey')  
        else:  
            p_skey = None  
        if re.search(r'skey=(?P<skey>[^;]*)',cookie):  
            skey = re.search(r'skey=(?P<skey>[^;]*)',cookie).group('skey')  
        else:  
            skey = None  
        if re.search(r'rv2=(?P<rv2>[^;]*)',cookie):  
            rv2 = re.search(r'rv2=(?P<rv2>[^;]*)',cookie).group('rv2')  
        else:  
            rv2 = None
        return self.getNewGTK(p_skey,skey,rv2)
    #这个tk的计算是从网上找来的


class Web(object):

    def __init__(self,user,password):
        self.web = webdriver.Chrome()#executable_path，这个应该指定一个默认路径
        self.user = user
        self.pw = password
        self.ls = ['pgv_pvi','pgv_si','_qpsvr_localtk','pgv_pvid','pgv_info',
                   'ptui_loginuin','ptisp','RK','ptcz','pt2gguin','uin'
                   ,'skey','p_uin','p_skey','pt4_token','Loading','qzspeedup',
                   'qz_screen',self.user+'_todaycount',self.user+'_totalcount',
                   'QZ_FE_WEBP_SUPPORT']#'cpu_performance_v8'这个获取不到，只好添加上去了
        self.data = {}
        self.cookie = ''

    def login(self):
        self.web.get('http://i.qq.com/')
        self.web.switch_to_frame('login_frame')
        self.web.find_element_by_id('switcher_plogin').click()
        self.web.find_element_by_id('u').send_keys(self.user)
        self.web.find_element_by_id('p').send_keys(self.pw)
        self.web.find_element_by_id('login_button').click()
        time.sleep(15)
        data ={}
        #print self.web.get_cookies()
        for i in self.ls:
            #print self.web.get_cookies()
            #print self.web.get_cookie(i)
            #print self.web.get_cookie(i)['value']
            self.data[i] = self.web.get_cookie(i)['value']
            #print '添加了一个值'
        for i in list(self.data):
            self.cookie += i + '=' + self.data[i]+';'
        self.cookie += 'cpu_performance_v8=4;'
        self.web.quit()
        return self.cookie


class ShuJuku(object):
#sqlite3只能放一千条数据，只好换Mysql了
    def __init__(self):
        #self.conn = sqlite3.Connection('d:\\QQ.db')
        self.path = 'd:\\QQ.db'
        if not os.path.exists(self.path):
            self.conn = sqlite3.Connection('d:\\QQ.db')
            self.conn.execute('create table qzone(id integer primary key not null,name text not null,qq text not null,content text not null,createdate datetime not null);')
            self.conn.commit()
            self.conn.close()
            self.data = False
        else:
            self.on()
    
    def get(self,**data):        
        if hasattr(self,'conn') and self.data:
            #print chardet.detect(data['name'])
            self.conn.execute(u'insert into qzone(name,qq,content,createdate)values("{name}","{qq}","{content}","{createdate}");'.format(name=data['name'],qq=data['qq'],content=data['content'],createdate=data['createdate']))
            self.conn.commit()
            self.off()
        else:
            self.on()
            #print chardet.detect(data['name'])
            self.conn.execute(u'insert into qzone(name,qq,content,createdate)values("{name}","{qq}","{content}","{createdate}");'.format(name=data['name'],qq=data['qq'],content=data['content'],createdate=data['createdate']))
            self.conn.commit()
            self.off()
                            
    def off(self):
        self.conn.close()
        self.data = False

    def on(self):
        self.data = True
        self.conn = sqlite3.Connection(self.path)


class Req(object):
    def __init__(self,cookie):
        self.cookie = cookie
        self.head = {'Cookie':cookie,'User-Agent':'Mozilla/5.0 (Windows NT 7.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

    def requ(self,url):
        req = requests.get(url,headers=self.head)
        print req.url
        #print req.content
        #print req.content[:10]
        return json.loads(req.content[10:-2])
        #return req

class Shujuku(object):

    def __init__(self,localhost="localhost",user="root",password="123456"):
        self.localhost = localhost
        self.user = user
        self.password = password
        
    def get(self,**data):
        try:
            conn = mysql.connect(self.localhost,self.user,self.password,db="qzone",charset="utf8")
            cur = conn.cursor()
            cur.execute(u'insert into qzone(name,qq,content,createdate)values("{name}","{qq}","{content}","{createdate}");'.format(name=data['name'],qq=data['qq'],content=data['content'],createdate=data['createdate']))
            cur.close()
            conn.commit()
        except Exception as e:
            print e

        finally:
            conn.close()
        
        

if __name__ == '__main__':
    s = G_tk()
    print s.g_tk()
        
