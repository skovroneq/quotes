from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.authors_and_quotes import AuthorsAndQuotesSpider
from .upload_data_to_db import upload_authors_to_db, upload_quotes_to_db, upload_tags_to_db
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'spiders'))


def run_scraper():

    process = CrawlerProcess(get_project_settings())
    process.crawl(AuthorsAndQuotesSpider)
    process.start()

    upload_authors_to_db()
    upload_quotes_to_db()
    upload_tags_to_db()


if __name__ == '__main__':
    run_scraper()
