from django.core.management.base import BaseCommand
from scamp.spiders.quotes_spider import QuotesSpider
from scamp.spiders.authors_spider import AuthorsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(AuthorsSpider)
        process.crawl(QuotesSpider)
        process.start()


