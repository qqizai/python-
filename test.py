# -*- coding:utf-8

import os
import subprocess
import web
import time
import requests
from web.wsgiserver import CherryPyWSGIServer



def img_to_string(img,clear=True,plus=""):
	subprocess.check_output('tesseract '+img+''+img,shell=True)
	with open(path+'.txt') as f:
		txt = f.read().strip()
	if clear:
		os.remove(img+'.txt')
	return txt

urls = ('/api','Ajax')

class Ajax(object):

    def POST(self):
        web.header('Content-Security-Policy','upgrade-insecure-requests',unique=True)
        data = web.input()
        print data
        req = requests.get(data)
        with open('st.img','wb') as f:
            f.write(req.content)
        value = img_to_string('st.img')
        return value


if __name__ == '__main__':
    #CherryPyWSGIServer.ssl_certificate = 'server.crt'
    #CherryPyWSGIServer.ssl_private_key = 'server.key'
    app = web.application(urls,globals())
    app.run()
