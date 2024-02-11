from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.authors_spider import AuthorsSpider
from scraper.spiders.quotes_spider import QuotesSpider


@shared_task
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()
