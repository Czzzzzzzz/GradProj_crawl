#coding:utf-8

import scrapy
import logging
import re
import itertools
import urllib

from scrapy.crawler import CrawlerProcess
from crawler.items import CrawlerItem

logger = logging.getLogger('myLogger')

class BaiduTiebaSpider(scrapy.Spider):
    
    name = 'baidupics'    
    #start_urls = [r'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1483168304047_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%A5%B3%E7%94%9F%E4%BA%BA%E8%84%B8']
    image_names = {}
    
    keyWord = ''    
    
    str_table = {
        '_z2C$q': ':',
        '_z&e3B': '.',
        'AzdH3F': '/',
    }
    
    char_table = {
        'w': 'a',
        'k': 'b',
        'v': 'c',
        '1': 'd',
        'j': 'e',
        'u': 'f',
        '2': 'g',
        'i': 'h',
        't': 'i',
        '3': 'j',
        'h': 'k',
        's': 'l',
        '4': 'm',
        'g': 'n',
        '5': 'o',
        'r': 'p',
        'q': 'q',
        '6': 'r',
        'f': 's',
        'p': 't',
        '7': 'u',
        'e': 'v',
        'o': 'w',
        '8': '1',
        'd': '2',
        'n': '3',
        '9': '4',
        'c': '5',
        'm': '6',
        '0': '7',
        'b': '8',
        'l': '9',
        'a': '0'
    }    
    
    char_table = {ord(key): ord(value) for key, value in char_table.items()}    
    
    def __init__(self, keyWord=None, *args, **kwargs):
        super(BaiduTiebaSpider, self).__init__(*args, **kwargs)
        self.keyWord = keyWord.decode('gb2312').encode('utf-8')
    
    #decode the url of images
    def decode(self,url):
        # replace strings first
        for key, value in self.str_table.items():
            url = url.replace(key, value)
        # replace the remaining chars
        return url.translate(self.char_table)    
        
    def codeKeyWords(self, word):
        word = urllib.quote(word)
        return word
    
    # build urls
    def buildUrls(self, word):
        url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
        word = self.codeKeyWords(word)
        
        pn_num = 400
        pn = []
        for i in range(pn_num):
            pn.append(i * 60)
        
        urls = (url.format(word=word, pn=x) for x in pn)
        return urls
    
    # obtain url of picture by decoding json data
    def resolveImgUrl(self, html):
        re_url = re.compile(r'"objURL":"(.*?)"')
        imgUrls = [self.decode(x) for x in re_url.findall(html)]
        return imgUrls

    def start_requests(self):
#        logger.info(self.keyWord)
        urls = self.buildUrls(self.keyWord)
        for url in urls:
            print url
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        item = CrawlerItem()
        #extract objurl from response text by using regular expression
        item['image_urls'] = self.resolveImgUrl(response.text)
        yield item

    