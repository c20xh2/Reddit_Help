# email_scraper/spiders/email_spider.py

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class EmailSpider(CrawlSpider):
    name = 'email_spider'
    allowed_domains = []  # You can leave this empty for now
    start_urls = []  # This will be filled dynamically

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1,  # Delay between requests to avoid overloading the server
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'FEED_FORMAT': 'json',
    }

    # Define rules for following links
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')  # Get the domain from arguments
        if domain:
            self.allowed_domains = [domain]

            
            self.start_urls = [f'http://{domain}', f'https://{domain}']
        super(EmailSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        # Extract emails using a regular expression
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
        if emails:
            yield {'emails': emails, 'url': response.url}
