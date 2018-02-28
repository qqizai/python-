import requests
import re
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class Tspider(object):

    def __init__(self):
        self.request = requests.Session()
        self.head = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    "authority":"www.endclothing.com",
                    "method":"GET",
                    "path":'/row/neighborhood-drizzler-jacket-181spnh-jkm01-grn.html',
                    'scheme':'https',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding':'gzip, deflate, br',
                    'accept-language':'zh,zh-CN;q=0.9',
                    'cache-control':'max-age=0',
                    'dnt':'1',
                    'upgrade-insecure-requests':'1'}

    def get(self,url):
        response = self.request.get(url,headers=self.head)
        return response.content
    
    def data(self,response):
        html = etree.HTML(response)
        data = html.xpath('//div[@class="product-item-info"]/a')
        return data
    
    def test(self,response):
        with open('test.html','w+') as f:
            f.write(response)


class T2spider(object):

    def __init__(self,path=None,headless=False):
        options = webdriver.FirefoxOptions()
        if headless:
            options.set_headless()
            options.add_argument('--disable-gpu')
        self.web = webdriver.Firefox(firefox_options=options,firefox_binary=path)
    
    def get_list(self,url):
        ls = []
        self.web.get(url)
        item = WebDriverWait(self.web,20).until(lambda driver:driver.find_elements_by_xpath('//div[@class="product-item-info"]/a'))
        try:
            self.next = self.web.find_element_by_xpath('//a[@class="c-pagination__next"]').get_attribute('href')
        except Exception as e:
            self.next = None

        if item:
            return map(lambda x:x.get_attribute('href'),item)
        else:
            return None

    def get_data(self,url):
        ls = []
        self.web.get(url)
        #time.sleep(20)
        #获取标题
        span = WebDriverWait(self.web,20).until(lambda driver:driver.find_element_by_xpath('//span[@class="base"]'))
        try:
            imgs = WebDriverWait(self.web,20).until(lambda driver:driver.find_elements_by_xpath('//div[@class="fotorama__thumb fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img"]/img'))
        except Exception as e:
            imgs = None
        
        #获取到所有的图片链接
        if imgs:
            ls.append(map(lambda x:x.get_attribute('src'),imgs))

        #span = self.web.find_element_by_xpath('//span[@class="base"]')
        ls.append(span.text)
        #获取价格
        price = self.web.find_element_by_xpath('//span[@class="price"]')
        ls.append(price.text)
        #获取标题之下的副标题和简介
        desc = self.web.find_elements_by_xpath('//div[@class="value"]')
        ls.extend(map(lambda x:x.text,desc))

        return ls


if __name__ == '__main__':
    spider = T2spider()
    #item = spider.get_list('https://www.endclothing.com/row/clothing')

    
    
    def run(spider,start_url):
        item = spider.get_list(start_url)
        if item:
            for i in item:
                response = spider.get_data(i)
                #print response
                print len(response)
        if spider.next:
            print '下一页是：{}'.format(spider.next)
            run(spider,spider.next)

    run(spider,'https://www.endclothing.com/row/clothing')


