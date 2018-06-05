
import flask
from flask import Flask,jsonify,request,render_template,redirect
from flask import session,url_for,escape,Response

import sqlalchemy
import flask_cors

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# engine = create_engine('mysql+pymysql://root:root@xxx.xxx.xxx.xxx/test?charset=utf8')



class MakeSqlServer(object):

    def __init__(self,WebServer):
        self.web = WebServer
        self._sql_init(db='mysql')

    def _sql_init(self,**kw):
        _config = {'mysql':self._mysql_init,'sqlite':self._sqlite_init}
        if 'db' in kw and kw['db'] in _config:
            _config[kw['db']]()

    def _mysql_init(self,**kw):
        _config = {'Host':'','User':'root','Pwd':'root','Db':'test','Charset':'utf8'}
        _config.update(kw)
        engine = create_engine('mysql+pymysql://{User}:{Pwd}@{Host}/{Db}?charset={Charset}'.format(**_config),echo=True)
        self.conn = engine.connect()
        self.metadata = MetaData(engine)
    
    def _sqlite_init(self,**kw):
        _config = {'Host':''}
        _config.update(kw)
        engine = create_engine('sqlite:///:memory:')#,echo=True
        self.conn = engine.connect()
        self.metadata = MetaData()

    def createTable(self,tableName,*args,**kw):
        #_config = {"tablename":tableName,}
        ls = [Column('id',Integer,primary_key=True,autoincrement = True)]
        for i in args:
            # if i in kw:
            #     ls.append(Column(i,String(kw[i])))
            # else:
            #     ls.append(Column(i,String(100)))
            ls.append(Column(i,String(100)))
        table_ls = Table(tableName,self.metadata,*ls)
        return table_ls
    
    def handle_reqeust(self):
        req_data = request.json or request.form or request.data
        table = self.createTable(request.path[1:],*list(req_data.keys()),**request.args)
        # print(dir(request))
        print(request.args)
        try:
            table.create()
            return 'true'
        except sqlalchemy.exc.InternalError as e:
            print(e)
            return str(e)
        except sqlalchemy.exc.InvalidRequestError as e:
            print(e)
            return (str(e))


class WebServer(object):

    def __init__(self,**kw):
        self._config = {'host':'0.0.0.0','port':8080}
        self.app = Flask(__name__)
    
    def append_route(self,routes,**kw):
        for route_item in routes:
            self.app.add_url_rule(route_item['path'],route_item['func'].__name__,route_item['func'],methods= route_item['method'] if 'method' in route_item else ['GET'])

        
    def runing(self,*args,**kw):
        self._config.update(kw)
        self.app.run(**self._config)


if __name__ == '__main__':
    server = WebServer()
    Handle = MakeSqlServer(server)
    route_rule = [{
        'path':'/','func':lambda:'hello'
    },{
        'path':'/authcheck','func':Handle.handle_reqeust,'method':['GET','POST']
    }]
    server.append_route(route_rule)
    server.runing()
    
