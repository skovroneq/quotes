from urllib.parse import urljoin
from scamp.items import QuoteItem
from quoteapp.models import Tag, Author, Quote
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author_name = quote.xpath("span/small/text()").get()
            text = quote.xpath("span[@class='text']/text()").get()

            author, created = Author.objects.get_or_create(fullname=author_name)

            existing_quote = Quote.objects.filter(text=text, author=author)
            if existing_quote.exists():
                continue

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
            full_next_url = urljoin(self.start_urls[0], next_link)
            yield scrapy.Request(url=full_next_url, callback=self.parse)
