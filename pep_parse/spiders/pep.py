import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    """Паук собирает список PEP и их текущий статус
    в формате:
    Номер документа, Название, Статус

    Возврат осуществляется в виде pep_date.csv
    по пути /results/pep_date.csv
    """
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        section = response.css('section[id^="numerical-index"]')
        all_peps = section.css('a[href^="pep-"]')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.css('dt:contains("PEP")+dd::text').get()
        name = response.css('dt:contains("Title")+dd::text').get()
        status = response.css('dt:contains("Status")+dd::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
