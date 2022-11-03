import os

from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

from common.playwright_settings import playwright_settings

from common_base.arg_env_parser import parse_args_env


source = {
    "url": "https://www.larepublica.co/indicadores-economicos/movimiento-accionario",
    "css_selector": "a.nameAction::text",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
    },
}

# https://www.investing.com/equities/colombia
# document.querySelectorAll('#cross_rate_markets_stocks_1 td.plusIconTd')
# COLCAP are only up to date

class BvcStocksSpider(scrapy.Spider):
    name = 'bvc_stocks_spider'

    def start_requests(self):
        yield scrapy.Request(
            url=source["url"],
            headers=source["headers"],
            meta={ "playwright": True, }
        )

    async def parse(self, response):
        stocks = response.css(source["css_selector"]).extract()
        for s in stocks:
            yield {"stock_ticker": s}


def extract_stocks_bvc(output_dest=None):
    assert output_dest != None, "missing output_dest"

    file_name = f"{datetime.today().strftime('%Y-%m-%d')}_stocks_bvc.csv"
    output_file = os.path.join(output_dest, file_name)
    feeds = {
        output_file: {
            "format": "csv",
            "fields": ["stock_ticker"],
        },
    }

    p = CrawlerProcess(settings={"FEEDS": feeds, **playwright_settings})
    p.crawl(BvcStocksSpider)
    p.start()


if __name__ == "__main__":
    kwargs = parse_args_env({
        "output_dest": {
            "args": ["--output-dest", "-o"],
            "env": "OUTPUT_DEST"
        },
    })
    extract_stocks_bvc(**kwargs)
