import logging

import scrapy
from fool.items import FoolItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from scrapy_splash import SplashRequest
# from scrapy_splash import SplashMiddleware
# script = """
# function main(splash, args)
#   splash.images_enabled = false
#   assert(splash:go(args.url))
#   assert(splash:wait(1))
#   js = string.format("document.querySelector('.load-more-button').click();", args.page)
#   splash:runjs(js)
#   assert(splash:wait(1))
#   return splash:html()
# end
# """



class FoolInvestingNewsSpider(CrawlSpider):
    name = "fool_investing_news"
    allowed_domains = ["www.fool.com"]
    row_count = 1
    start_urls = ['https://www.fool.com/investing-news/']
    rules = (
        Rule(
            LinkExtractor(allow=(r'https://www\.fool\.com/investing/\d{4}/\d{2}/\d{2}/.*',)),
            callback='parse_item',
            follow=False
        ),
    )

    # def start_requests(self):
    #     for url in self.start_urls:
    #         # endpoint其他教程都是写的render.html，但是模拟点击需要修改为 '/execute'
    #         yield SplashRequest(url=url, callback=self.parse_item, endpoint='execute', args={
    #             'wait': 10, 'images': 0, 'lua_source': script
    #         })

    def parse_item(self, response):
        logging.info(f"Parsing item URL: {response.url}")
        item = FoolItem()
        self.get_title(response, item)
        self.get_time(response, item)
        self.get_source(response, item)
        self.get_content(response, item)
        self.get_url(response, item)
        self.get_stock_symbol(response, item)

        self.row_count += 1
        if self.row_count >= 50:
            raise scrapy.exceptions.CloseSpider(reason="Reached maximum row count")
        yield item

    def get_url(self, response, item):
        url = response.url
        if url:
            item['url'] = url

    def get_content(self, response, item):
        content = response.xpath('//div[@class="max-w-full"]//text()').getall()
        if content:
            logging.info(f"text: {content}")
            result_with_spaces = ' '.join(content)
            item['content'] = result_with_spaces


    def get_source(self, response, item):
        author_content = response.css('meta[name="author"]::attr(content)').get()
        if author_content:
            logging.info(f"source: {author_content}")
            item['source'] = author_content

    def get_time(self, response, item):
        published_time = response.css('meta[property="article:published_time"]::attr(content)').get()
        if published_time:

            item['time'] = published_time

    def get_title(self, response, item, ):
        og_title_content = response.xpath('//meta[@property="og:title"]/@content').get()

        if og_title_content:
            cleaned_title = og_title_content.split('+')[0].strip()
            cleaned_title = cleaned_title.split('|')[0].strip()
            logging.info(f"title: {cleaned_title}")
            item['title'] = cleaned_title


    def get_stock_symbol(self, response, item):
        stock_symbol = response.xpath('//meta[@name="tickers"]/@content').get()
        if stock_symbol:

            logging.info(f"stock_symbol: {stock_symbol}")
            item['stock_symbol'] = stock_symbol



