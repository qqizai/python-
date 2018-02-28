from scrapy.command import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import Crawler

class Command(ScrapyCommand):

    requires_project = True

    def syntax(self):
        return '[options]'
    
    def short_desc(self):
        return 'Runs all of spiders'
    
    def run(self,args,otps):
        setting = get_project_settings()

        for spider_name in self.crawler.spiders.list():
            craw = Crawler(settings)
            craw.configure()
            spider = craw.spiders.create(spideer_name)
            craw.crawl(spider)
            craw.start()
        self.craw.start()