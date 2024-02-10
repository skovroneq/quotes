import json
from quoteapp.models import Author, Quote, Tag
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


def upload_authors_to_db():
    with open('authors.json', 'r') as file:
        authors_data = json.load(file)

    for author_data in authors_data:
        author_name = author_data['fullname']
        try:
            existing_author = Author.objects.get(fullname=author_name)
        except ObjectDoesNotExist:
            with transaction.atomic():
                author = Author.objects.create(**author_data)
                author.save()


def upload_quotes_to_db():
    with open('quotes.json', 'r') as file:
        quotes_data = json.load(file)

    for quote_data in quotes_data:
        quote_content = quote_data.get('quote')
        try:
            existing_quote = Quote.objects.get(quote=quote_content)
        except ObjectDoesNotExist:
            with transaction.atomic():
                quote = Quote.objects.create(**quote_data)
                quote.save()


def upload_tags_to_db():
    existing_tags = set(Tag.objects.values_list('name', flat=True))

    for quote_data in Quote.objects.all().values('tags'):
        for tag_name in quote_data['tags']:
            if tag_name not in existing_tags:
                tag = Tag(name=tag_name)
                tag.save()
                existing_tags.add(tag_name)
