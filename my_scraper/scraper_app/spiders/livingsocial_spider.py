from scrapy.spider import BaseSpider

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from scraper_app.items import LivingSocialDeal


class LivingSocialSpider(BaseSpider):
	""" Spider for regularly updated Living Social Website"""
	name = 'livingsocial'
	allow_domains = ['livingsocial.com']
	start_urls = ['http://www.livingsocial.com/cities/4-los-angeles']
	deals_list_xpath = '//li[@dealid]'
	item_fields = {'title': './/a/div[@class="all-deals"]/h3[@itemprop]/text()',
                   'link': './/a/@href',
                   'description': './/a/div[@class="all-deals"]/p/text()',
                   'category': './/a/div[@class="all-deals"]/div[@class="deal-category"]/span/text()',
                   'location': './/a/div[@class="all-deals"]/ul[@class="unstyled deal-global"]/li/text()',
                   'original_price': './/a/div[@class="all-deals"]/ul[@class="unstyled deal-global"]/li[@class="deal-strikethrough-price"]/del/text()',
                   'price': './/a/div[@class="all-deals"]/ul[@class="unstyled deal-global"]/li[@class="deal-price"]/text()'}
	def parse(self, response):
	        """
	        Default callback used by Scrapy to process downloaded responses

	        Testing contracts:
	        @url http://www.livingsocial.com/cities/15-san-francisco
	        @returns items 1
	        @scrapes title link

	        """
	        selector = HtmlXPathSelector(response)

	        # iterate over deals
	        for deal in selector.select(self.deals_list_xpath):
	            loader = XPathItemLoader(LivingSocialDeal(), selector=deal)

	            # define processors
	            loader.default_input_processor = MapCompose(unicode.strip)
	            loader.default_output_processor = Join()

	            # iterate over fields and add xpaths to the loader
	            for field, xpath in self.item_fields.iteritems():
	                loader.add_xpath(field, xpath)
	            yield loader.load_item()