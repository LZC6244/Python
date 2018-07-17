# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from tencent.items import TencentItem


class TencentSpider(RedisCrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    # start_urls = ['http://hr.tencent.com/position.php?&start=0#a']
    redis_key = 'tencentspider:start_urls'

    # 多加后缀/@href将会报错：AttributeError: 'str' object has no attribute 'iter'
    # 原因是：restrict_xpaths应指向元素 - 直接链接或包含链接的容器，而不是属性
    # page_link = LinkExtractor(restrict_xpaths=(
    #   '//div[@class="pagenav"]/a[starts-with(@href,"position.php?&start=")]/@href'))

    # response中的提取规则
    # 使用xpath提取
    # restrict_xpaths表示使用xpath,allow表示使用正则
    # 返回的是符合匹配规则对象的列表（自动去重）
    page_link = LinkExtractor(restrict_xpaths=(
        '//div[@class="pagenav"]/a[starts-with(@href,"position.php?&start=")]'))

    # 使用正则表达式的提取
    # page_link = LinkExtractor(allow=("start=\d+"))

    rules = (
        Rule(page_link, callback='parse_item', follow=True),
    )

    # 回调函数
    def parse_item(self, response):
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()

        content_list = response.xpath('//tr[@class="even"]|//tr[@class="odd"]')
        # 初始化TencentItem对象
        item = TencentItem()

        for i in content_list:
            # 职位名称
            item['position_name'] = i.xpath('./td[1]/a/text()').extract()
            # 详情链接
            item['position_link'] = i.xpath('./td[1]/a/@href').extract()
            # 职位类别
            item['position_type'] = i.xpath('./td[2]/text()').extract()
            # 招聘人数
            item['num'] = i.xpath('./td[3]/text()').extract()
            # 工作地点
            item['location'] = i.xpath('./td[4]/text()').extract()
            # 发布时间
            item['time'] = i.xpath('./td[5]/text()').extract()

            # yield 是一个类似 return 的关键字，但这个函数返回的是个生成器
            yield item
