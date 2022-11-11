import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class SuperSpider(CrawlSpider):
    name = 'extractor'
    allowed_domains = ['google.com']
    start_urls = ['https://www.google.com/search?q=dentist+seattle']
    #base_url = 'https://en.wikipedia.org'
 
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True), #follow = False - to go only for 1st level
    )

    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }

    def parse_item(self, response):
       #print(response.url)
        domain = (response.url).split("/")[2]
        if domain != (self.start_urls[0]).split("/")[2]:
            print(domain)
        # for link in self.link_extractor.extract_links(response):
        #     print(link)
        #     yield Request(link.url, callback=self.parse)