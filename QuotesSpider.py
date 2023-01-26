import scrapy
import schedule
import time
from scrapy import cmdline

# This class is a spider for scraping data from quotes website
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # the starting url for the spider to crawl
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        
    ]
    # settings for the spider such as user agent, download delay, 
    # and number of concurrent requests
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'RETRY_TIMES': 3,
    'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
    'DOWNLOADER_MIDDLEWARES': {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    }
    }
    # parse method that is called when the spider is done crawling
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
    # check for next page and follow the link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# function to run the spider
def crawl_quotes():
    cmdline.execute("scrapy runspider QuotesSpider.py".split())

# schedule the spider to run every 30 seconds
schedule.every(30).seconds.do(crawl_quotes)

# infinite loop to run the scheduled spider
while True:
    schedule.run_pending()
    time.sleep(1)
