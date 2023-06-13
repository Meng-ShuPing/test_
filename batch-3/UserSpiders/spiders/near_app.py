"""
附近寻欢app
"""
import json

import scrapy
from scrapy import Request

from ..items import UserSpidersItem


class NearAppSpider(scrapy.Spider):
    name = 'near_app'
    allowed_domains = ['xxx']

    def query_urls(self):
        """从文件中查询请求url"""
        return ["https://api.iggqq.cn:443/api/feeds/recommend?page=1&net=4g&op=46002&sid=87507188szjrotw&verc=220409102&pf=android&pf_ver=10&man=Xiaomi&mod=MI+8&ver=2.5.1&fr=market_shl_xiaomi_01&an=2.0&code=haituan1&tv=0&p=0&tz=%2B8&lang=zh-CN&f=MainActivity&ts=1651908470&ckey=88e44ffb14bd08adf28bd3ab915c25aa&dno=e64725c0e0ada1b5e5948370ffa7d294cb&dno1=4e09a7652d8121a41fa5f90c5c9c5eae&h=21f22f72ae646adf45b9ffe04db58fe6"]

    def start_requests(self):
        """构建请求队列"""
        start_urls = self.query_urls()
        for url in start_urls:
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        """响应回调函数"""

        data = json.loads(response.text)
        for feed in data["feeds"]:
            item = UserSpidersItem()
            item["userid"] = feed["user"]["id"]
            item["nickname"] = feed["user"]["nickname"]
            item["sex"] = feed["user"]["sex"]
            item["avatar"] = feed["user"]["avatar_url"]
            item["city"] = feed["user"]["city_name"]
            item["sign"] = feed["content"]
            item["images"] = feed["file_urls"]
            yield item
