from scrapy.crawler import CrawlerProcess
from .scrap_images.spiders.image_spider import ImageSpider
from .celery import app

from scrapy.cmdline import execute

import sys
import os


@app.task
def start_spider(url):
    """Task for crawling web"""
    "1"
    # process = CrawlerProcess()
    # process.crawl(ImageSpider, url=url)
    # process.start()
    # process.join()
    "2"
    # cmd = f"bash 'scrapy crawl image_spider -a url={url}'"
    # print(f"Command '{cmd}'")
    # os.system(cmd)
    "3"
    # sys.argv = ['cd', 'image_collector', '&&', '/usr/local/bin/scrapy', 'crawl', 'image_spider', '-a', f"url={url}"]
    os.system(f"python -m scrapy crawl image_spider -a url={url}")
    # execute(['/usr/local/bin/scrapy', 'crawl', 'image_spider', '-a', f"url={url}"])


if __name__ == "__main__":
    url = r'https://www.wykop.pl/'
    start_spider(url)
