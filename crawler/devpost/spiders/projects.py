# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.markup import remove_tags
from scrapy.loader.processors import Join, MapCompose
from devpost.items import ProjectItem


class ProjectLoader(ItemLoader):
    default_output_processor = Join(' ')
    headline_in = MapCompose(str.strip)
    text_in = MapCompose(remove_tags)


class ProjectsSpider(CrawlSpider):
    name = 'projects'
    allowed_domains = ['devpost.com']
    start_urls = ['http://devpost.com/software/popular']

    rules = (
        Rule(
            LinkExtractor(allow=('\?page=[0-9]+', )),
            callback='parse_project_page',
            follow=True
        ),
    )

    def parse_project_page(self, response):
        for url in response.xpath(
                '//a[contains(@class, "link-to-software")]/@href'
        ).extract():
            yield Request(url, callback=self.parse_project)

    def parse_project(self, response):
        hxs = HtmlXPathSelector(response)
        loader = ProjectLoader(ProjectItem(), hxs)

        loader.add_value('url', str(response.url))
        loader.add_xpath('title', '//h1[@id="app-title"]/text()')
        loader.add_xpath(
            'headline',
            '//header[@id="software-header"]//p[@class="large"]/text()'
        )
        loader.add_xpath('hackathon', '//div[@id="submissions"]//p/a/text()')
        loader.add_xpath(
            'text',
            '//div[@id="app-details-left"]'
            '/div[not(@id)]//*[text()]'
        )
        loader.add_xpath(
            'builtwith',
            '//div[@id="built-with"]//a/text()'
        )
        loader.add_xpath(
            'likes',
            '//header[@id="software-header"]//div[@class="software-likes"]'
            '//span[@class="side-count"]/text()'
        )
        # loader.add_xpath('developers', '//h1[@id="app-title"]/text()')
        # loader.add_xpath('developers', '//h1[@id="app-title"]/text()')
        loader.add_xpath('winner', '//span[contains(@class, "winner")]/text()')

        return loader.load_item()
