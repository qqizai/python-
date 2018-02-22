import scrapy
import re

class Job(scrapy.Spider):
    name = '51job'
    allowed_domains = ['jobs.51job.com']
    start_urls = ['http://search.51job.com/list/180200,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self,response):
        for i in response.xpath('//div[@class="el"]/p/span/a/@href'):
            #print(i.extract())
            request = scrapy.Request(i.extract(),callback=self.parse_info)
            yield request
    
    def parse_info(self,response):
        # print('这是开始')
        # print(response.xpath('//div[@class="cn"]/h1/text()').extract())
        # print(response.xpath('//div[@class="cn"]/span/text()').extract())
        # print(response.xpath('//div[@class="cn"]/strong/text()').extract())
        # print(response.xpath('//div[@class="cn"]/p[1]/text()').extract())
        # print(response.xpath('//div[@class="cn"]/p[2]/text()').extract())
        print(response.xpath('//div[starts-with(@class,"bmsg")]/p/text()').extract())
    
    def filter(self,item):
        map(lambda x:str(x).strip(),ls)
        filter(lambda x:x,ls)


