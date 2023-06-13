"""
火星app
"""
import json
import random
import time

import scrapy
from ..items import UserSpidersItem


class HuoxingSpider(scrapy.Spider):

    name = 'huoxing'
    list_base_url = "http://www.huoxingxin.com:80/app/poi/poiSign/listPoiSignSimple.do"
    detail_base_url = "http://www.huoxingxin.com:80/app/user/ucenter/getUserCenterPoiSign.do"
    queryType = "104"
    currentPage = 1
    showcount = "200"
    detail_type = "2"
    token = ("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJlMDJmNzMwNDIzMDg0NGY3YmQ1MjU2Njc5ZTM4MTJhYyIsInVzZXJJZCI6ImUwMmY3MzA0M"
             "jMwODQ0ZjdiZDUyNTY2NzllMzgxMmFjIiwiaWF0IjoxNjUyMTY4NTE5LCJqdGkiOiJiN2I2MGIzYS0zNDU3LTQ0NmMtYjZlYS03MmV"
             "hNTlhNzA4YTgifQ.DxNzupOLsQ9gFgUzoaZHSPem-x_RmAbrViAZ-ruykcQ")
    loginUserId = "e02f7304230844f7bd5256679e3812ac"

    def create_detail_url(self, userid):
        """构建详情页请求url"""

        return (f"{self.detail_base_url}?queryUserId={userid}&type={self.detail_type}&token={self.token}"
                f"&loginUserId={self.loginUserId}")

    def create_list_url(self, page):
        """构建详情页请求url"""
        currentPage = str(page)
        print(f"=============获取第 {page} 页数据=========================")
        return (f"{self.list_base_url}?queryType={self.queryType}&currentPage={currentPage}"
                f"&showcount={self.showcount}&token={self.token}&loginUserId={self.loginUserId}")

    def start_requests(self):
        """构建初始列表页请求"""

        start_list_url = self.create_list_url(self.currentPage)

        yield scrapy.Request(url=start_list_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """列表页响应解析"""
        list_data = json.loads(response.text).get("data")
        if list_data and isinstance(list_data, list):
            # 详情页请求
            for data in list_data:
                userid = data["poiSignBO"]["userid"]
                detail_url = self.create_detail_url(userid)
                yield scrapy.Request(url=detail_url, callback=self.detail_parse)
                # 休眠
                time.sleep(random.uniform(0.1, 0.3))

            # 翻页请求
            self.currentPage += 1
            list_url = self.create_list_url(self.currentPage)
            yield scrapy.Request(url=list_url, callback=self.parse)

    def detail_parse(self, response):
        """详情页响应解析"""

        detail_data_list = json.loads(response.text).get("data")

        def mp4_to_jpeg_format(path: str):
            """mp4格式获取封面图"""
            if path and path.endswith("mp4"):
                path = path.replace(".mp4", ".jpeg", 1)
            return path

        def get_images(data_list):
            """获取朋友圈图片列表"""
            images = []
            for data in data_list:
                image = mp4_to_jpeg_format(data["poiSignBO"]["hrefpath"])
                images.append(image)
            return images

        if detail_data_list:
            item = UserSpidersItem()
            item["userid"] = detail_data_list[0]["poiSignBO"]["userid"]
            item["nickname"] = detail_data_list[0]["poiSignBO"]["nickname"]
            item["sex"] = detail_data_list[0]["poiSignBO"]["sex"]
            item["avatar"] = detail_data_list[0]["poiSignBO"]["headimgPath"]
            item["background"] = mp4_to_jpeg_format(detail_data_list[0]["poiSignBO"]["hrefpath"])
            item["city"] = ""
            # 该app签名过于格式化, 改为取第一条动态的文本
            content = detail_data_list[0]["poiSignBO"].get("beizhu")
            item["sign"] = content if content else detail_data_list[0]["poiSignBO"].get("remark")
            item["images"] = get_images(detail_data_list)
            yield item





