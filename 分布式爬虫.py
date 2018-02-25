#!/usr/bin/env python
# coding:utf-8

import requests
import redis
import json
import MySQLdb as mysql
import re
import threading
import multiprocessing
import chardet

'''新浪分布式爬虫，算是完成了吧，当然，没有添加多进程和多线程，代理也没有'''


class Sina(object):
    #_start_id = '1713926427'
    _luiID = '10000011'
    _featureID = '20000320'

    def __init__(self,start_id,host,pw,Mode,**args):
        
        #主从模式，判断入口点是否存在，如果存在则为主模式，生产，如果不存在，则为从模式，消耗
        '''
            start_id是入口用户ID，会从这里最开始爬取
            host是redis数据库的IP地址
            pw是redis数据库的密码
            mode是确定生产模式还是消费模式，默认为生产模式
            args里传入用户名，IP，密码，作为数据库信息,用来存放数据
        '''
        self._db = args
        self._Mode = Mode
        self.start_id = start_id
        #self.luiID = '10000011'       #基本不变
        #self.featureID = '20000320'     #基本不变

        self._host = host
        self._pw = pw
        
        #入口网址，先得到用户信息，获取到粉丝ID，关注ID，主页ID
        self.start_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={0}'   #传入入口ID
        
        #通过主页ID，获取用户的详细信息
                                                        #这里的lfID是indexID
        self.user_info_url = 'https://m.weibo.cn/api/container/getIndex?containerid={indexID}_-_INFO&luicode={luiID}&lfid={lfID}&featurecode={featureID}&type=uid&value={userID}'

        #通过粉丝ID,获取他的粉丝
        self.user_fance_url = 'https://m.weibo.cn/api/container/getIndex?containerid={fanceID}&luicode={luiID}&lfid={lfID}&featurecode={featureID}&page={number}'
        #https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_1713926427&luicode=10000011&lfid=1005051713926427&featurecode=20000320&page=3 粉丝url
        

        #通过关注ID,获取他的关注
        self.user_follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid={followID}&luicode={luiID}&lfid={lfID}&featurecode={featureID}&page={number}'

        conn = redis.Redis(host = self._host,password = self._pw)
        conn.lpush('waitID',self.start_id)
        #conn.close

    def requ(self,url,Referer = None):
        head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36','Host':'m.weibo.cn'}
        if Referer:
            print Referer
            head.setdefault('Referer',Referer)
        req = requests.get(url)
        #print req.status_code
        print req.url
        
        data = req.content
        req.close()
        try:
            data = json.loads(data)
            return data
        except Exception as e:
            print e
            return None

    
    def get_user_info(self,userid):
        content = self.requ(self.start_url.format(userid))         #获取用户基础信息
        #data = json.loads(content)
        if content:
            userID = content['userInfo']['id']
            fanceID = content['fans_scheme'][33:].replace('recomm','')
            
            #print fanceID
            
            followID = content['follow_scheme'][33:].replace('recomm','')
            #print followID
            indexID = content['tabsInfo']['tabs'][0]['containerid']
            
            #print u'主页ID',indexID
            
            #print content['userInfo']['fans_scheme']
            
            lfID = re.findall(r'lfid=(\d+)',content['userInfo']['fans_scheme'])[0]
            return fanceID,followID,indexID,lfID
        else:
            return None

        

    
    #解析器，用于解析数据，消费者
    def fans_generate(self):         #生成，多通道生成，如果能够以信息来生成多个爬虫
        conn = redis.Redis(host = self._host,password = self._pw)
        keynumber = conn.llen('waitID')
        while keynumber:         #这个不能永远循环下去，应该有个停止的条件
        
            userID = conn.rpop('waitID')          #获取待请求的用户ID，这个请求是用户信息请求，从这里得到粉丝ID，再得到粉丝的用户信息
            fanceID,followID,indexID,lfID = self.get_user_info(userID)
            num = 1
            while num:
                url = self.user_fance_url.format(fanceID = fanceID,luiID = self._luiID,indexID = indexID,lfID = lfID.replace(userID,''),featureID = self._featureID,number = num)
                content = self.requ(url)
                     

                print u'正在获取粉丝数据'
                if content.has_key('cards'):
                    fance_group = content['cards'][0]['card_group']
                    print u'粉丝的数量有',len(fance_group)
                else:
                    break
                #print '等待的元素还有',conn.llen('waitID')
                #print fance_group
                for i in fance_group:
                    if conn.sadd('completeID',i['user']['id']):
                        fans_user_ID = i['user']['id']
                        print fans_user_ID
                        #获得粉丝基础信息
                        
                        fanceID,followID,indexID,lfID = self.get_user_info(fans_user_ID)
                        
                        url = self.user_info_url.format(indexID = indexID,lfID = indexID,luiID = self._luiID,featureID = self._featureID,userID = fans_user_ID)
                        #获得粉丝详细信息
                        content = self.requ(url)
                        if content.has_key('cards'):
                            if content['cards']:
                                data = content['cards'][0]['card_group']
                                ls = []
                                if data:
                                    for i in data:
                                        if i['item_name'] == u'昵称':
                                            ls.append(i['item_content'])
                                        elif i['item_name'] == u'性别':
                                            ls.append(i['item_content'])
                                        elif i['item_name'] == u'所在地':
                                            ls.append(i['item_content'])
                                data = content['cards'][1]['card_group']
                                for i in data:
                                    if i['item_name'] == u'等级':
                                        ls.append(i['item_content'])
                                        
                                    elif i['item_name'] == u'阳光信用':
                                        ls.append(i['item_content'])
                                        
                                    elif i['item_name'] == u'注册时间':
                                        ls.append(i['item_content'])
                                    else:
                                        ls.append(0)
                        
                                print len(ls)
                                print ls
                                if len(ls) == 6:
                                    username = ls[0].encode('utf-8')
                                    gender = ls[1].encode('utf-8')
                                    city = ls[2].encode('utf-8')
                                    level = ls[3].encode('utf-8')
                                    sun_credit = ls[4].encode('utf-8')
                                    regtime = ls[5].encode('utf-8')

                                
                                self.conn(username = username,gender = gender,city = city,level = level,sun_credit = sun_credit,regtime = regtime,table = userID)
                                print u'正在插入数据'
                                
                    else:
                        print u'跳过了一个粉丝ID',fans_user_ID
                        continue
                num += 1

                try:
                    print u'等待的用户ID元素还有',conn.llen('waitID')
                
                except KeyboardInterrupt as e:
                    print '停止'
                    break

                except TypeError as e:
                    print '停止'
                    break
                
            try:
                print '等待的用户ID元素还有',conn.llen('waitID')
                
            except KeyboardInterrupt as e:
                print '停止'
                break
            except TypeError as e:
                print '停止'
                break
            #finally:
             #   conn.close()
                
    def follow_generate(self):      #从等待抓取ID中获取用户ID，然后获得关注人，并添加关注人的ID到抓取ID中
        conn = redis.Redis(host = self._host,password = self._pw)
        keynumber = conn.llen('waitID')
        while keynumber:
            userID = conn.rpop('waitID')
            fanceID,followID,indexID,lfID = self.get_user_info(userID)
            num = 1
            url = self.user_follow_url.format(followID = followID,luiID = self._luiID,lfID = lfID.replace(userID,''),featureID = self._featureID,number = num)
            while num:
                
                content = self.requ(url)
                if not content:
                    num = 0
                followgroup = content['cards'][0]['card_group']
                for i in followgroup:
                    if conn.sadd('completeID',i['buttons'][0]['params']['uid']):
                        conn.lpush('waitID',i['buttons'][0]['params']['uid'])
                num += 1
                print '正在添加数据到redis数据库'
                
            try:
                print '现在waidID里面的元素还有'+str(keynumber)
            except KeyboardInterrupt as e:
                print '停止'
                keynumber = 0
            #finally:
             #   conn.close()

    def conn(self,**kw):
        if self._db.has_key('user'):
            user = self._db['user']
        if self._db.has_key('ip'):
            ip = self._db['ip']
        else:
            ip = self._host
        if self._db.has_key('pw'):
            pw = self._db['pw']
        else:
            pw = self._pw
        if self._db.has_key('db'):
            db = self._db['db']
        else:
            db = 'test'
        
        conn = mysql.Connection(host = ip,user = user,passwd = pw,db = db,charset='utf8')
        cursor = conn.cursor()

        #if kw.has_key('table'):
        
        cursor.execute('create table if not exists `{table}`(id int auto_increment primary key,username text,gender text,city text,level text,sun_credit text,regtime text)'.format(table = kw['table']))
        #print '已创建一个表',kw['table']
        sql = "insert into `{table}`(username,gender,city,level,sun_credit,regtime) values ('{}','{}','{}','{}','{}','{}')".format(kw['username'],kw['gender'],kw['city'],kw['level'],kw['sun_credit'],kw['regtime'],table=kw['table'])
        print sql
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()


        
    def make(self):
        if self._Mode:
            self.follow_generate()
        else:
            self.fans_generate()
        
        


if __name__ == '__main__':
    sina = Sina('1713926427','172.16.2.47','adminroot',False,db = 'sina',user='root')
    sina.make()
    
        
        
    
