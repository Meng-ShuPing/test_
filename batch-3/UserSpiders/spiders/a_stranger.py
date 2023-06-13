"""
一个陌生人app
"""
import json
import random
import time
from copy import deepcopy

import scrapy

from ..items import UserSpidersItem


class AStrangerSpider(scrapy.Spider):
    name = 'a_stranger'
    # allowed_domains = ['xxx']
    token = "5e14553e51f047d1dc35-aeca09e41fe54b0149db1652061617468-1.3.35"
    ucode = "4756279d02b42ca3"
    list_url = "http://api.jianduixiang.com:80/TreeHole"
    detail_url = "http://api.jianduixiang.com:80/get_user"
    img_url = "http://api.jianduixiang.com:80"

    def start_requests(self):
        """构建列表页请求"""

        for i in range(1, 1082):
            body = {
                "token": self.token,
                "ucode": self.ucode,
                "page": str(i),
                "type": "0"
            }
            yield scrapy.FormRequest(url=self.list_url, formdata=body, callback=self.parse, dont_filter=True)
            time.sleep(random.uniform(0, 0.5))

    def parse(self, response):
        """列表页响应解析"""

        list_data = json.loads(response.text).get("data")

        # 构建详情页请求
        for data in list_data:
            uid = data.get("uid")
            body = {
                "token": self.token,
                "ucode": self.ucode,
                "uid": uid
            }
            yield scrapy.FormRequest(url=self.detail_url, formdata=body, callback=self.detail_parser)
            time.sleep(random.uniform(0, 0.5))

    def detail_parser(self, response):
        """详情页响应解析"""

        detail_data = json.loads(response.text).get("data")

        item = UserSpidersItem()
        item["userid"] = detail_data["uid"]
        item["nickname"] = detail_data["name"]
        item["sex"] = detail_data["sex"]
        item["avatar"] = self.img_url + detail_data["head_img"] if detail_data.get("head_img") else ""
        item["background"] = self.img_url + detail_data["head_img"] if detail_data.get("head_img") else ""
        item["city"] = detail_data["city"]
        moods = detail_data["mood"]
        images = []
        for mood in moods:
            image = mood.get("imgs", [])
            images = images + image if image[0] else images
        # 没有签名则用第一条动态的文本替代
        item["sign"] = detail_data["autograph"] if detail_data.get("autograph") else moods[0].get("title")
        item["images"] = images

        # 图片不够,且可能存在下一页动态, 请求翻页
        if len(item["images"]) < 4 and len(moods) == 3:
            item["page"] = "2"
            body = {
                "token": self.token,
                "ucode": self.ucode,
                "uid": detail_data["uid"],
                "page": item["page"]
            }
            yield scrapy.FormRequest(
                url=self.detail_url,
                formdata=body,
                callback=self.detail_turn_pages,
                meta=deepcopy({"item": item})
            )
        else:
            yield item

    def detail_turn_pages(self, response):
        """详情页翻页"""

        # 获取响应对象中的meta属性
        item = response.meta.get("item")
        detail_data = json.loads(response.text).get("data")
        moods = detail_data["mood"]
        for mood in moods:
            image = mood.get("imgs", [])
            item["images"] = item["images"] + image if image[0] else item["images"]

        # 图片不够,且可能存在下一页动态, 请求翻页
        if len(item["images"]) < 4 and len(moods) == 3:
            item["page"] = int(item["page"]) + 1
            body = {
                "token": self.token,
                "ucode": self.ucode,
                "uid": detail_data["uid"],
                "page": str(item["page"])
            }
            yield scrapy.FormRequest(
                url=self.detail_url,
                formdata=body,
                callback=self.detail_turn_pages,
                meta=deepcopy({"item": item})
            )
        else:
            item.pop("page", "")
            yield item

