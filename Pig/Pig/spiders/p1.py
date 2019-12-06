# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy

class P1Spider(scrapy.Spider):
    name = 'p1'
    allowed_domains = ['zhuwang.cc']
    start_urls = ['https://hangqing.zhuwang.cc/zhurou/list-65-1.html',]

    def parse(self, response):
        date_list = response.xpath("//div[@class='main']/div/div/ul/li")
        for li in date_list:
            item = {}
            item['publish_date'] = li.xpath("./p[2]/text()").extract()[-1].strip()
            detail_url = li.xpath("./p[1]/a/@href").extract_first()
            print(item)
            if detail_url is not None:
                yield scrapy.Request(
                    detail_url,
                    callback=self.parse_detail,
                    meta={'item':deepcopy(item)}
                )
        next_page = response.xpath("//a[text()='下一页']/@href").extract_first()
        current_page = response.xpath("//div[@class='zxpage']/span/text()").extract()[0]
        # print("*"*20)
        # print(current_page)
        if next_page is not None:
            next_page = 'https://hangqing.zhuwang.cc/zhurou/' + next_page
            if int(current_page) < 7:
                yield scrapy.Request(
                    next_page,
                    callback=self.parse
                )
            else:
                yield scrapy.Request(
                    next_page,
                    callback=self.parse2
                )

    def parse_detail(self,response):
        item = response.meta['item']
        price_list = response.xpath("//div[@class='zxxw']/div[2]/text()").extract()
        for price in price_list:
            if '白条肉' in price:
                info_list = price.split('\xa0\xa0')
                if len(info_list) >= 4:
                    item['province'] = info_list[0].rstrip('\xa0')
                    item['city'] = info_list[1].rstrip('\xa0')
                    item['price'] = info_list[3].rstrip('\xa0')
                    yield item

    def parse2(self,response):
        date_list = response.xpath("//div[@class='main']/div/div/ul/li")
        for li in date_list:
            item = {}
            item['publish_date'] = li.xpath("./p[2]/text()").extract()[-1].strip()
            detail_url = li.xpath("./p[1]/a/@href").extract_first()
            print(item)
            if detail_url is not None:
                yield scrapy.Request(
                    detail_url,
                    callback=self.parse_detail2,
                    meta={'item': deepcopy(item)}
                )
        next_page = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_page is not None:
            next_page = 'https://hangqing.zhuwang.cc/zhurou/' + next_page
            yield scrapy.Request(
                next_page,
                callback=self.parse2
            )
    def parse_detail2(self,response):
        item = response.meta['item']
        price_list = response.xpath("//div[@class='zxxw']/div[2]/p")[1:]
        for price in price_list:
            price_info = price.xpath("./span/span/text()").extract_first().strip().split(' ')
            if len(price_info) == 4:
                item['province'] = price_info[0]
                item['city'] = price_info[1]
                item['price'] = price_info[3]
                yield item

