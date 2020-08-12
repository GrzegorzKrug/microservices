from scrapy.crawler import CrawlerProcess
from .scrap_images.spiders.image_spider import ImageSpider
from .celery import app

from scrapy.cmdline import execute

import sys
import os


@app.task
def start_spider(url):
    """Task for crawling web"""
    os.system(f"python -m scrapy crawl image_spider -a url={url}")


if __name__ == "__main__":
    url = r'https://www.wykop.pl/'
    start_spider(url)
