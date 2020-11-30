import scrapy
from scrapy.exceptions import CloseSpider
from ..items import CrawlerItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from w3lib.html import replace_tags, remove_tags_with_content

class Crawler(scrapy.Spider):
    name = "Crawler"
    maxDocs = 100
    start_urls = [
        "https://www.uefa.com/uefachampionsleague/",
        "https://www.skysports.com/football",
        "https://www.bbc.com/sport/football",
        "https://www.mirror.co.uk/sport/football/",
        "https://www.mlssoccer.com/",
        "https://theathletic.co.uk/premier-league/",
        "https://theathletic.co.uk/serie-a/",
        "https://theathletic.co.uk/la-liga/",
        "https://theathletic.co.uk/bundesliga/",
        "https://theathletic.co.uk/champions-league/",
        "https://theathletic.co.uk/europa-league/",
        "https://www.tribalfootball.com/",
        "https://www.football365.com/",
        "https://www.whoscored.com/",
        "https://fbref.com/en/",
        "https://footystats.org/",
        "https://www.theguardian.com/football",
        "https://www.bundesliga.com/en/bundesliga",
        "http://www.legaseriea.it/en"
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
        body = ''.join(response.xpath("body").extract())
        loader.add_value('body', replace_tags(remove_tags_with_content(body, ('script', 'noscript', 'style',)), " ").strip().replace("\n", " ").replace("\r", " ").replace("\t"," "))


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

            inStartUrls = False
            for startUrl in self.start_urls:
                if url.find(startUrl) >= 0:
                    inStartUrls = True
                    break
            
            if inStartUrls:
                self.seenUrls.add(url)
                outLinks.append(url)
                yield response.follow(url, callback=self.parse)

        loader.add_value('outLinks', outLinks)
        yield loader.load_item()
                