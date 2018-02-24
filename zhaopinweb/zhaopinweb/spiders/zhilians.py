import scrapy
import re

class Zhaopin(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%AD%A6%E6%B1%89&kw=python&sm=0&p=1']

    def parse(self,response):
        for i in response.xpath('//table[@class="newlist"]/tr/td/div/a/@href').extract():
            yeild scrapy.Request(i,callback=self.parse2)
    
    def parse2(self,response):
        pass