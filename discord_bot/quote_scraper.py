# Vincent Vu
# Sept 2026
# This module will handle the quote scraper utilizing Scrapy, a third-party Python Library
# that abtracts many of the processes of basic scraping away for this project
import scrapy
from scrapy.crawler import CrawlerProcess


def get_quotes():
    """This is the main function to return a AsyncCrawlerProcess for QuotesSpider in a Python script.
    If the object is run, the spider will run, get quotes, and write them into a .json file named
    'quotes.json'."""

    # Writing down the settings for the spider. Any need to change settings must be
    # done here to only change this spider
    settings = {
                "FEEDS": {
                            "discord_bot\\quotes.json": {"format": "json"},
                          },
                }

    # To run the spider, I will use AsyncCrawlerProcess and return it for other parts of a program to use it
    process = CrawlerProcess(settings=settings)
    process.crawl(QuotesSpider)
    process.start()


def _get_tags(type: str, from_item: object):
    """Helper function to specifically get tags from a quote from the website"""
    for type in from_item:
        yield from type.css("a::text").getall()


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                    "quote": quote.css("span::text").get(),
                    "author": quote.css("small::text").get(),
                    "tags": [i for i in _get_tags("a::text", quote.css("div.tags"))]
            }


__all__ = ["get_quotes"]


if __name__ == "__main__":
    print(get_quotes())