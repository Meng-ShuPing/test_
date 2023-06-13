"""
图片下载
"""
import json
from copy import deepcopy

import scrapy

from ..utile import sqlite_to_pandas


class DownloadUserImagesSpider(scrapy.Spider):
    name = 'download_user_images'

    def start_requests(self):
        """构建下载请求"""
        df = sqlite_to_pandas("user_info")
        for i in range(df.shape[0]):

            item = {
                "userid": df.iloc[i]["userid"]
            }
            # 最多要三张朋友圈图片
            images = json.loads(df.iloc[i]["images"])
            images = images if len(images) < 3 else images[:4]
            urls = [df.iloc[i]["avatar_url"], df.iloc[i]["background_url"]]
            urls = urls + images if images else urls
            for avatar_no, url in enumerate(urls):
                # 图片编号
                item["avatar_no"] = avatar_no
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, meta=deepcopy({"item": item}))

    def parse(self, response):
        """下载图片"""
        item = response.meta["item"]
        item["content"] = response.body
        yield item
