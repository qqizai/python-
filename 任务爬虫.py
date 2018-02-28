#coding:utf-8

import requests
import re
import json
from lxml import etree
import urlparse
import sys
import time
from selenium import webdriver


class T3spider(object):

    def __init__(self,start_url=None,path=None,headless=True):
        self.web = webdriver.Firefox()
        if start_url:
            self.start_url = start_url
        else:
            self.start_url = 'https://www.endclothing.com/us/neighborhood-drizzler-jacket-181spnh-jkm01-grn.html'
        self.head = {
        'authority':'www.endclothing.com',
        'method':'GET',
        'path':urlparse.urlsplit(self.start_url).path,
        'scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        
    }

    def get_urls(self,htmls):
        html = etree.HTML(htmls)
        href = html.xpath('//a[@class="c-pagination__next"]/@href')
        if href:
            print href[0]
            self.start_url = href[0]
        else:
            self.start_url = ''
        urls = html.xpath('//div[@class="product-item-info"]/a/@href')
        return urls
        
    
    def get_imgs(self,imgjson):
        ls = []
        img = json.loads(imgjson)
        for i in img.keys():
            for j in img[i].keys():
                for k in img[i][j].keys():
                    if k == 'data':
                        ls.extend(img[i][j][k])
        return ls

    
    def get_desc(self,descjson):
        ls = []
        desc = json.loads(descjson)
        ds = ["name","description",["offers","priceCurrency"],["offers","price"]]
        for i in ds:
            if type(i) == list:
                ls.append(desc[i[0]][i[1]])
            else:
                ls.append(desc[i])
        return ls

    def get_data(self,htmls):
        data = []
        html = etree.HTML(htmls)
        imgs = html.xpath('//script[contains(text(),"[data-gallery-role=gallery-placeholder]")]')
        if imgs:
            img_text = imgs[0].text.strip()
            data.append(self.get_imgs(img_text))
        product_data = html.xpath('//script[@type="application/ld+json"]')
        if product_data:
            product_text = product_data[0].text.strip()
            data.extend(self.get_desc(product_text))
        title = html.xpath('//meta[@name="WT.z_pcolour"]')
        if title:
            data.append(title[0].attrib['content'])
        return data
        

    def get_content(self,url):
        self.head['path'] = urlparse.urlsplit(url).path
        req = requests.get(url,headers=self.head)
        ps = len(req.content)
        print u'获取的网页长度为：{}'.format(ps)
        if ps<10000:
            print u'获取出错，需要更换cookie'
        #print req.content
        return self.get_data(req.content)

    def cookieiter(self,url):
        self.web.get(url)
        
        ls = {}
        lp = []
        for i in self.web.get_cookies():
            for j in i.keys():
               ls[j] = i[j]
        for i in ls.keys():
            lp.append([i,ls[i]])
        print lp
        print map(lambda x:':'.join(x),lp)
        self.head['cookie'] = ls


def main():
    try:
        
        spider = T3spider('https://www.endclothing.com/row/brands/nike')
        times = 0
        while spider.start_url:
            spider.cookieiter(spider.start_url)
            req = requests.get(spider.start_url,headers=spider.head)
            #print req.headers
            #print req.content
            #print req.request.headers
            urls = spider.get_urls(req.content)
            print u'网址数量为：'.format(len(urls))
            for i in urls:
                times +=1
                if times%2 == 0:
                    spider.cookieiter(spider.start_url)
                print u'正在获取数据，网址为：{}'.format(i)
                print u'取得的数据长度为：{}'.format(len(spider.get_content(i)))
    except Exception as e:
        print e
    finally:
        spider.web.quit()
            
        
def maan():
    spider = T3spider('https://www.endclothing.com/row/brands/nike')
    times = 0
    while spider.start_url:
        spider.cookieiter(spider.start_url)
        req = requests.get(spider.start_url,headers=spider.head)
            #print req.headers
            #print req.content
            #print req.request.headers
        urls = spider.get_urls(req.content)
        print u'网址数量为：'.format(len(urls))
        for i in urls:
            times +=1
            if times%2 == 0:
                spider.cookieiter(spider.start_url)
            print u'正在获取数据，网址为：{}'.format(i)
            print u'取得的数据长度为：{}'.format(len(spider.get_content(i)))
            


if __name__ == '__main__':
    maan()
        
