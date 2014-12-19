from scrapy.spider import BaseSpider

from scraper_app.items import LivingSocialDeal

class LivingSocialScraper(BaseSpider):
	""" Spider for regularly updated Living Social Website"""
	name = 'livingsocial'
	allow_domains = ['livingsocial.com']
	start_urls = ['http://www.livingsocial.com/cities/4-los-angeles']
	deals_list_xpath = '//li@dealid]'
	item_fields = {'title': './/a/div[@class="deal-bottom"]/h3[@itemprop]/text()',
                   'link': './/a/@href',
                   'description': './/a/div[@class="deal-bottom"]/p/text()',
                   'category': './/a/div[@class="deal-top"]/div[@class="deal-category"]/span/text()',
                   'location': './/a/div[@class="deal-top"]/ul[@class="unstyled deal-info"]/li/text()',
                   'original_price': './/a/div[@class="deal-bottom"]/ul[@class="unstyled deal-info"]/li[@class="deal-original"]/del/text()',
                   'price': './/a/div[@class="deal-bottom"]/ul[@class="unstyled deal-info"]/li[@class="deal-price"]/text()'}
