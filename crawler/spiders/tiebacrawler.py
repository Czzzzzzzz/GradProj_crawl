import scrapy

from crawler.items import CrawlerItem

class BaiduTiebaSpider(scrapy.Spider):
    
    name = 'baidutieba'    
    start_urls = ['http://tieba.baidu.com/p/2235516502?see_lz=1&pn=%d' % i for i in range(1, 2)]
    image_names = {}
    
    def parse(self, response):
        item = CrawlerItem()
        item['image_urls'] = response.xpath("//img[@class='BDE_Image']/@src").extract()
        for index, value in enumerate(item['image_urls']):
            number = self.start_urls.index(response.url) * len(item['image_urls']) + index
            self.image_names[value] = '%04d.jpg' % number
        yield item
    
    