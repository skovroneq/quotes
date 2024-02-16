from quoteapp.models import Tag, Author, Quote
from scrapy_djangoitem import DjangoItem
import scrapy


class TagItem(DjangoItem):
    django_model = Tag


class AuthorItem(DjangoItem):
    django_model = Author


class QuoteItem(DjangoItem):
    django_model = Quote
    tags = scrapy.Field()
