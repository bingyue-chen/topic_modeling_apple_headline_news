# -*- coding: utf-8 -*-

import scrapy
import csv
import datetime
import pandas as pd
import time

class AppleNewSpider(scrapy.Spider):
    name = "apple_news_apider"
    writer = csv.writer(open("news.csv", 'w'))

    def start_requests(self):
        base_url = 'https://tw.appledaily.com/appledaily/archive/'

        for date in pd.date_range(datetime.date(2018, 1, 1), datetime.date(2018, 10, 20)):
            url = base_url+date.strftime('%Y%m%d')
            yield scrapy.Request(url=url, callback=self.parse_news_link)
            time.sleep(1)

    def parse_news_link(self, response):
        for url in response.css('.nclns a').xpath('@href').extract():
            if url.startswith("https://tw.news.appledaily.com/headline/daily/") or url.startswith("http://tw.news.appledaily.com/headline/daily/"):
                yield scrapy.Request(url, callback=self.parse_news)

    def parse_news(self, response):
        contents = ''
        for content in response.css('.ndArticle_content > .ndArticle_margin > p::text').extract():
            contents = contents+content.rstrip()
        if(len(contents) > 10):
            self.writer.writerow([response.url, contents])

