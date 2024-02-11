from urllib.parse import urljoin
from scraper.items import AuthorItem
import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        author_links = response.xpath(
            "//span[@class='text']/following-sibling::span/small[@class='author']/following-sibling::a[@href]/@href").getall()

        for author_link in author_links:
            if author_link:
                full_url = f"{self.start_urls[0]}{author_link}/"
                yield scrapy.Request(url=full_url, callback=self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            full_next_url = urljoin(self.start_urls[0], next_link)
            yield scrapy.Request(url=full_next_url, callback=self.parse)

    def parse_author(self, response: scrapy.http.Response):
        author_item = AuthorItem()

        fullname = response.xpath(
            "//h3[@class='author-title']/text()").extract_first()
        born_date = response.xpath(
            "//span[@class='author-born-date']/text()").extract_first()
        born_location = response.xpath(
            "//span[@class='author-born-location']/text()").extract_first()
        description = response.xpath(
            "//div[@class='author-description']/text()").get()

        author_item["fullname"] = fullname
        author_item["born_date"] = born_date
        author_item["born_location"] = born_location[3:] if born_location else None
        author_item["description"] = description.strip(
        ) if description else None

        yield author_item
