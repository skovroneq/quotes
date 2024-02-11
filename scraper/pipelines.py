# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from quoteapp.models import Quote, Author, Tag
from scraper.items import QuoteItem, AuthorItem


class ScraperPipeline:
    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            author = Author.objects.filter(fullname=item['author'])

            quote = Quote(text=item['text'], author=author.first())
            quote.save()

            tags = [Tag.objects.get_or_create(
                name=tag)[0] for tag in item['tags']]
            quote.tags.set(tags)
            quote.save()
        elif isinstance(item, AuthorItem):
            Author.objects.get_or_create(fullname=item['fullname'], born_date=item["born_date"],
                                         born_location=item["born_location"], description=item["description"])
        return item
