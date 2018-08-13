# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from utils import pgs
from utils import rds
from .util import imjad
from music163 import items
from datetime import datetime


class Music163Pipeline(object):

    def __init__(self):
        # PostgreSQL
        host = 'localhost'
        port = 12432
        db_name = 'scrapy'
        username = db_name
        password = db_name
        self.postgres = pgs.Pgs(host=host, port=port, db_name=db_name, user=username, password=password)
        # Redis
        self.redis = rds.Rds(host=host, port=12379, db=2, password='redis6379').redis_cli

    def process_item(self, item, spider):
        if isinstance(item, items.Music163Item):
            music_id = item['music_id']
            music_name = item['music_name']
            music_url = item['music_url']
            music_lyric = imjad.get_lyric(music_id)
            now = datetime.now()

            key = 'music:163:{0}'.format(music_id)
            if not self.redis.exists(key):
                params = (music_id, music_name, music_url, music_lyric, 0, now)
                self.postgres.handler(add_music(), params)
        return item


def add_music():
    sql = 'insert into tb_music_163 values(music_id,music_name,music_url,music_lyric,"count",create_time)' \
          'values(%s,%s,%s,%s,%s,%s)'
    return sql