from datetime import datetime
from quoteapp.models import Quote, Author, Tag
from scamp.items import QuoteItem, AuthorItem


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
            date_of_birth = datetime.strptime(
                item["born_date"], '%B %d, %Y').date()
            Author.objects.get_or_create(fullname=item['fullname'], born_date=date_of_birth,
                                         born_location=item["born_location"], description=item["description"])
        return item
