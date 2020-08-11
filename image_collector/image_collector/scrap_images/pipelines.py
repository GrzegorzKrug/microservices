# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.files import FileException, FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
from contextlib import suppress
from .custom_loger import define_logger

from PIL import Image
from io import BytesIO

import requests
import hashlib
import os
import re


class ImageException(FileException):
    """General image error exception"""


class ImageSaver(ImagesPipeline):
    my_logger = define_logger("pipeline", mode='a')

    def get_images(self, response, request, info):
        name = self.file_name(request=request, response=response, info=info)
        orig_image = Image.open(BytesIO(response.body))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        area = width * height
        try:
            res = re.match(r"https?:\/\/(www\.)?([a-zA-Z\.\-]*)(\.\w+\/)", request.url)
            domain = res.group(2)  # Full, www, domain, first slash
            name = domain + '-' + name
        except AttributeError as e:
            self.my_logger.error(f"Could not read domain: {request.url} - {e}")
        except IndexError as e:
            self.my_logger.error(f"Could not read domain: {request.url} - {e}")

        if area <= 10_000:
            path = os.path.join("tiny", name)
        elif area <= 50_000:
            path = os.path.join("small", name)
        elif area <= 500_000:
            path = os.path.join("medium", name)
        else:
            path = os.path.join("big", name)

        image, buf = self.convert_image(orig_image)

        # path = str(self.title) + path
        self.my_logger.info(f"Saving: {path}")
        yield path, image, buf

        for thumb_id, size in self.thumbs.items():
            thumb_path = self.thumb_path(request, thumb_id, response=response, info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf

    def file_name(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{image_guid}.jpg"

    # def item_completed(self, results, item, info):
    #     with suppress(KeyError):
    #         ItemAdapter(item)[self.images_result_field] = [x for ok, x in results if ok]
    #     return item


class MyPipeline:
    my_logger = define_logger("my-pipeline", mode='a')

    def process_item(self, item, spider):
        self.my_logger.debug(f"Processing {len(ItemAdapter(item).get('image_urls'))} images")
        title = ItemAdapter(item).get('title')

        for url in ItemAdapter(item).get('image_urls'):
            name = str(hashlib.sha1(to_bytes(url))) + ".jpg"
            img = self.get_image(url)
            if img is None:
                continue
            self.save_image(name, title, img)

    def get_image(self, url):
        try:
            response = requests.get(url, stream=True)
            response.raw.decode_content = True
            image = Image.open(response.raw)
            self.my_logger.debug(f"Got image: {url}")
            return image
        except Exception as e:
            self.my_logger.error(f"{e}")
            return None

    def save_image(self, name, title, image):
        size = 'tiny'
        path = os.path.join("pictures", size, '-'.join([title, name]))

        image.save(path)
