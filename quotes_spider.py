import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            content = quote.css('span.text::text').extract_first()
            author = quote.css('small.author::text').extract_first()
            tags = ','.join(quote.css('.tags a::text').extract())
            yield {
                'content': content,
                'author': author,
                'tags': tags,
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
