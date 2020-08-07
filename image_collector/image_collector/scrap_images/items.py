# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ImageItem(scrapy.Item):
    # images = Field()
    title = Field()
    image_urls = Field()
