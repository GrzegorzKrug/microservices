import scrapy
from ..items import ImageItem
from ..custom_loger import define_logger


class ImageSpider(scrapy.Spider):
    name = 'image_spider'
    my_logger = define_logger("spider")

    # allowed_domains = ['www.wikipedia.pl']

    def start_requests(self):
        url = getattr(self, "url")

        if url:
            self.my_logger.debug(f"Starting image parsing at: {url}")
            yield scrapy.Request(url=url, callback=self.find_images)
        else:
            self.my_logger.error(f"URL is empty")
            yield None

    def parse(self, response):
        print(f"Parsing: {self.url}")

    def find_images(self, response):
        images = response.css("img::attr(src)").extract()
        item = ImageItem()
        item['image_urls'] = []
        item['title'] = response.css("title::text").extract()[0]
        item['title'] = response.xpath("//title/text()").extract()[0]

        self.my_logger.info(f"Found :{len(images)} images")
        for img in images:
            img = str(img)
            im_url = img if img.startswith("http") else "http:" + img

            item['image_urls'].append(im_url)
            self.my_logger.info(f"Got image: {im_url}")

        yield item

    # def save_images(self, response):
    #     image = ImageItem()
    #     self.my_logger.info(f"Got image: {response.url}")

    def err_hanlder(self, failure):
        url = failure.request.url
        callback = failure.request.callback
        errback = failure.request.errback  # should work same way as callback... ?
        # status = failure.value.response.status
        self.my_logger.error(f"Fail request: @: {url}")
