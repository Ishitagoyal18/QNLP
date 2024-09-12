# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
import os

class CustomFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        # Customize the file path using the organization name and URL
        filename = os.path.basename(urlparse(request.url).path)
        org_name = item.get('Orgname', 'default').replace(' ', '_')
        return f'{org_name}/{filename}'



class PdfscraperPipeline:
    def process_item(self, item, spider):
        return item
