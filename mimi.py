# coding:utf-8

import sqlite3
import requests
import json
import os


class Mimi(object):

    def __init__(self):
        self.url = '''http://napi.uc.cn/3/classes/topic/lists/%E7%A7%98%E5%AF%86?_app_id=hottopic&_size=10&_fetch=1&_fetch_incrs=1&_max_pos={}&_fetch_total
        =1&_select=like_start%2Cdislike_start%2Ctitle%2Ctag%2Cmedia_data%2Clist_info%2Ccontent%2Cavatar%2Cuser_name%2Cis_hot%2Chot_comment%2Ccomment_total%2Coriginal%2Ctv_duration'''

        self.number = 1475820900000
        if os.path.exists('d:\\mimi.db'):
            self.db = sqlite3.Connection('d:\\mimi.db')
        else:
            self.db = sqlite3.Connection('d:\\mimi.db')
            self.db.execute('create table mimi(id integer primary key not null,name text not null,content text not null,date datetime not null);')
            self.db.commit()
            self.db.close()

    def get(self,url):
        req = requests.get(url)
        print req.url
        return req.content

    def save(self):
        #content = self.get(self.url.format(self.number))
        while self.number:
            content = self.get(self.url.format(self.number))
            if len(content)<=36:
                self.number = 0
            data = json.loads(content)
            for i in data['data']:
                #print i
                if len(i['content']) <1:
                    continue
                self.save_shuju(i['content'],i['user_name'],i['_created_at'])
            #print self.number
            self.number = data['data'][-1]['_pos']
            
    def save_shuju(self,*data):
        conn = sqlite3.Connection('d:\\mimi.db')
        cursor = conn.cursor()
        try:
            cursor.execute(u'insert into mimi(name,content,date)values("{0[1]}","{0[0]}","{0[2]}");'.format(data))
            conn.commit()
        except Exception as e:
            print '错误',e
            return
        finally:
            conn.close()
        

if __name__ == '__main__':
    sq = Mimi()
    sq.save()

    
