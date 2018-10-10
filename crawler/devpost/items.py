# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    headline = scrapy.Field()
    hackathon = scrapy.Field()
    text = scrapy.Field()
    builtwith = scrapy.Field()
    likes = scrapy.Field()
    developers = scrapy.Field()
    created_by = scrapy.Field()
    winner = scrapy.Field()

