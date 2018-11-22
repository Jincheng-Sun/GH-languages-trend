# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import json
import os
import datetime
filepath=os.path.abspath('../trendModel/datas/iterm.jl')

class StatlangPipeline(object):


    def open_spider(self,spider):
        self.file = open(filepath,'a+')
    def close_spider(self,spider):
        self.file.close()
    def process_item(self, item, spider):
        line=json.dumps(dict(item))+"\n"
        # time_new=line[3]
        # time_new=datetime.datetime.strptime(time_new,['%Y-%m-%dT%H:%M:%S'])
        # self.file[-1]['timestamp']
        self.file.write(line)
        return item
