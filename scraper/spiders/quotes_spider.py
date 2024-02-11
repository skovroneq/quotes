from scraper.items import QuoteItem
from quoteapp.models import Tag, Author
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.comm"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author_name = quote.xpath("span/small/text()").extract_first()
            text = quote.xpath("span[@class='text']/text()").get()

            quote_author = Author.objects.filter(fullname=author_name)
            if quote_author.exists():
                author = quote_author.first()

            quote_item = QuoteItem()
            quote_item["author"] = author
            quote_item["text"] = text
            quote_item["tags"] = set()

            for tag in tags:
                quote_tags, created = Tag.objects.get_or_create(name=tag)
                quote_item["tags"].add(quote_tags)

            yield quote_item

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link, callback=self.parse)
