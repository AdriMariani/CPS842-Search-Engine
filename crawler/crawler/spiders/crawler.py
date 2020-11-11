import scrapy
from scrapy.exceptions import CloseSpider
from ..items import CrawlerItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor

class Crawler(scrapy.Spider):
    name = "Crawler"
    maxDocs = 500
    start_urls = [
        "https://www.uefa.com/uefachampionsleague/"
    ]
    linkExtractor = LinkExtractor()

    def __init__(self, *args, **kwargs):
        super(Crawler, self).__init__(*args, **kwargs)
        self.seenUrls = set()
        self.seenDocs = 0

    def parse(self, response):
        if self.seenDocs > Crawler.maxDocs:
            raise CloseSpider("Page Limit Reached.")

        loader = ItemLoader(item=CrawlerItem(), response=response)

        loader.add_value('url', response.url)
        loader.add_value('title', response.css('title::text').get())
        #loader.add_value('body', ''.join(response.xpath("//body//text()").extract()).strip().replace("\n", "").replace("\r", ""))

        self.seenDocs += 1
        self.seenUrls.add(response.url)
        outLinks = []
        links = Crawler.linkExtractor.extract_links(response)

        for link in links:
            url = link.url
            if url in self.seenUrls:
                outLinks.append(url)
                continue
            elif len(url) > 50 or '?' in url or '#' in url or '%' in url:
                continue

            self.seenUrls.add(url)
            outLinks.append(url)
            yield response.follow(url, callback=self.parse)

        loader.add_value('outLinks', outLinks)
        yield loader.load_item()
                