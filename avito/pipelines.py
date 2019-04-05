# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import tablib
import tempfile
import json

class AvitoPipeline(object):
    def open_spider(self, spider):
        self.tempfile = tempfile.TemporaryFile('w+')
        self.keys = set()

    def close_spider(self, spider):
        ds = tablib.Dataset(headers=self.keys)

        self.tempfile.seek(0)
        for line in self.tempfile.readlines():
            row = []
            line_dict = json.loads(line)
            for key in self.keys:
                row.append(line_dict.get(key, ''))
            ds.append(row)

        self.tempfile.close()

        with open('result.xlsx', 'wb') as f:
            f.write(ds.xlsx)

    def process_item(self, item, spider):
        self.keys.update(dict(item).keys())
        self.tempfile.write(json.dumps(dict(item)) + "\n")
        return item
