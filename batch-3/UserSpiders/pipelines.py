# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface 下载
from pymongo import MongoClient

from .utile import sqlite_to_excel

client = MongoClient(username="admin", password="123456")

# collection = client["user-info"]["user"]
collection = client["huoxing"]["user"]


class UserspidersPipeline:

    def process_item(self, item, spider):

        sec_type = {"1": "男", "0": "女"}

        # 将字典数据录入数据库
        if spider.name == "a_stranger":
            item["sex"] = item["sex"]
            collection.insert_one(dict(item))
        elif spider.name == "huoxing":
            item["sex"] = sec_type.get(str(item["sex"]))
            collection.insert_one(dict(item))

        return item


class DownloadImagesPipeline:

    # def open_spider(self, spider):

    def process_item(self, item, spider):

        # 将图片下载到本地
        if spider.name == "download_user_images":
            imgpath = '/home/sdjuser/Desktop/images/'
            filepath = imgpath + item["userid"] + '_' + str(item["avatar_no"]) + '.jpeg'
            with open(filepath, 'wb') as f:
                f.write(item["content"])
        return item

    def close_spider(self, spider):
        # 输出excel
        # 下载完图片后,输出excel文件
        if spider.name == "download_user_images":
            sqlite_to_excel("user_info", "user.xls")
