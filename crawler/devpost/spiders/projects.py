# -*- coding: utf-8 -*-
import scrapy


class ProjectsSpider(scrapy.Spider):
    name = 'projects'
    allowed_domains = ['devpost.com']
    start_urls = ['http://devpost.com/software']

    def parse(self, response):
        pass
