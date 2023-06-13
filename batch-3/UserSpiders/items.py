# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserSpidersItem(scrapy.Item):
    """用户信息模型"""
    # 用户id
    userid = scrapy.Field()
    # 昵称
    nickname = scrapy.Field()
    # 性别
    sex = scrapy.Field()
    # 头像
    avatar = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 签名
    sign = scrapy.Field()
    # 背景图
    background = scrapy.Field()
    # 图片
    images = scrapy.Field()

    # 功能字段
    # 朋友圈页数
    page = scrapy.Field()




