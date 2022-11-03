import json
import os

from datetime import datetime
from urllib.parse import urljoin, quote, unquote

import scrapy
from scrapy.crawler import CrawlerProcess

from common_base.arg_env_parser import parse_args_env


def get_url_google(source, page, stock):
    url = unquote(urljoin(
        source["base_url"],
        quote(stock["id"])
    ))

    return url


def get_url_investing(source, page, stock):
    url = urljoin(
        source["base_url"],
        f'{stock["name_url"]}{page["end_url"]}',
    )

    return url


class MetricsSpider(scrapy.Spider):
    name = 'metrics_spider'

    def __init__(self, sources, stocks=None, *args, **kwargs):
        super(MetricsSpider, self).__init__(*args, **kwargs)
        self.sources = sources
        self.stocks = stocks

    def start_requests(self):
        url_getters = {
            "google": get_url_google,
            "investing": get_url_investing
        }

        for (source_id, source) in self.sources.items():
            if source_id not in self.stocks:
                continue
            if source_id not in url_getters:
                raise ValueError("Unknown url getter source", source_id)

            get_url = url_getters[source_id]
            headers = source["headers"]
            for stock in self.stocks[source_id]:
                stock_id = stock["id"]

                for (page_name, page) in source["pages"].items():
                    yield scrapy.Request(
                        url=get_url(source, page, stock),
                        headers=headers,
                        callback=self.extract_from_html,
                        cb_kwargs=dict(
                            source_id=source_id,
                            page_name=page_name,
                            stock_id=stock_id,
                        )
                    )

    def extract_from_html(self, response, **kwargs):
        source_id = kwargs["source_id"]
        page_name = kwargs["page_name"]
        stock_id = kwargs["stock_id"]

        extraction_time = datetime.now().isoformat()
        metrics = self.sources[source_id]["pages"][page_name]["metrics"]
        for (metric, m) in metrics.items():
            if "xpath" in m:
                selector = response.xpath(m["xpath"])
            else:
                raise ValueError("Unsupported metric extraction", m)

            if m["output_type"] == "scalar":
                value = selector.get()
            elif m["output_type"] == "array":
                value = selector.extract()
            else:
                raise ValueError("Unsupported metric output type", m)

            if value == None:
                value = "null"

            yield {
                "stock_id": stock_id,
                "source_id": source_id,
                "page_name": page_name,
                "extraction_time": extraction_time,
                "metric": metric,
                "value": value
            }


def extract_metrics(output_dest=None, stocks_demo=False, stocks_file=None):
    assert output_dest != None, "missing output_dest"

    # feeds - output file
    file_name = f"{datetime.today().strftime('%Y-%m-%d')}_metrics.csv"
    output_file = os.path.join(output_dest, file_name)
    feeds = {
        output_file: {
            "format": "csv",
            "fields": [
                "stock_id",
                "source_id",
                "page_name",
                "extraction_time",
                "metric",
                "value",
            ],
        }
    }

    # stocks
    print(stocks_demo, stocks_file)
    if stocks_demo:
        stocks_file = os.path.join(
            os.path.dirname(__file__),
            "extract_metrics_stocks.json"
        )
    else:
        assert stocks_file != None, "missing stocks_file"

    with open(stocks_file, "r") as f:
        stocks = json.load(f)

    assert isinstance(stocks, dict), "stocks mismatches expected form"

    # metrics config
    metrics_config_file = os.path.join(
        os.path.dirname(__file__),
        "extract_metrics_config.json"
    )
    with open(metrics_config_file, 'r') as f:
        metrics_config = json.load(f)

    # crawling
    p = CrawlerProcess(settings={"FEEDS": feeds})
    p.crawl(MetricsSpider, sources=metrics_config["sources"], stocks=stocks)
    p.start()

    return output_file


if __name__ == "__main__":
    kwargs = parse_args_env({
        "output_dest": {
            "args": ["--output-dest", "-o"],
            "env": "OUTPUT_DEST"
        },
        "stocks_file": {
            "args": ["--stocks-file", "-s"],
            "env": "STOCKS_FILE"
        }
    })

    if (kwargs["stocks_file"] == None):
        kwargs["stocks_demo"] = True

    extract_metrics(**kwargs)
