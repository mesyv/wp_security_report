# To run this spider:
# venv/scripts/activate 
# scrapy crawl email -o emails.csv

# IDEA: drop emails without the same domain as the website (or gmail/yahoo)

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from urllib.parse import urlparse
import pandas as pd
from email_validator import validate_email, EmailNotValidError
 
def check_email(email):
    try:
        v = validate_email(email)
        email = v["email"] 
        return True
    except EmailNotValidError as e:
        # print(str(e))
        return False

class Spider(CrawlSpider):
    name = 'email'
    path = "C:\Projekty\Coding\wp_security_report\leads\output\master_file.xlsx"
    master_file = pd.read_excel(path)
    allowed_domains = list(master_file['Domain']) 
    start_urls = list(master_file['Website'])

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=False), #follow = False - to go only for 1st level
    )

    custom_settings = {
        'DEPTH_LIMIT': 1 # Found on https://www.mikulskibartosz.name/how-to-use-scrapy-to-follow-links-on-the-scraped-pages/
    }

    def parse_item(self, response):
        print(response.url)
        #emails = re.findall(r'[\w\.-]+@[\w\.-]+', response.text) # My Regular Expresion to find emails
        emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", response.text)
        for email in emails:
            if check_email(email) == True:
                yield {
                    'Domain': urlparse(response.url).netloc.replace("www.", "").lower(), # Take domain only
                    'URL': response.url,
                    'Email': email.lower()
                    #In Future: phone, facebook, linkedin, instagram, twitter
                    }