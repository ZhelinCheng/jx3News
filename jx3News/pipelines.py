# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import MySQLdb
from scrapy.exceptions import DropItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

INDEX = 0

class Jx3NewsPipeline(object):
    def __init__(self):
        try:
            self.db = MySQLdb.connect(host="192.168.84.128", user="root", passwd="root", port=3306, db="test", charset="utf8")
            self.cursor = self.db.cursor()
            print "数据库连接成功!"

        except:
            print "数据库连接失败!"

    def process_item(self, item, spider=None):
        global INDEX

        title = item['title']
        url = item['url']
        mydate = item['date']
        abstract = item['abstract']

        # print url
        # par = re.match(r'[^\.][0-9A-Za-z]+(?=\.com)', 'http://jx3.xoyo.com', re.I|re.M|re.S|re.IGNORECASE)
        # print par

        if mydate != '' and abstract != '':
            param = (mydate, url, title, abstract)

            sql = "insert into db_xoyo (update_date, url, title, abstract) values(%s, %s, %s, %s)"
            self.cursor.execute(sql, param)

            INDEX = INDEX + 1

            if INDEX % 10 == 0:
                print '提交数据库！'
                self.db.commit()

        else:
            raise DropItem(item)

        return item

    def close_spider(self, spider):
        print '提交数据库！'
        self.db.commit()
        self.db.close()
        print("Done")


if __name__ == '__main__':
    myClass = Jx3NewsPipeline()
    print myClass.process_item(item={
        'url': 'http://jx3.xoyo.com',
        'title': '测试',
        'date': '2017-10-31 09:28:57',
        'abstract': '测试'
    })