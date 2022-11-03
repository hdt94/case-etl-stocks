# Extract stocks data

Extraction of stocks data by scraping both static HTML-only and dynamic JavaScript-based web pages.

## Setup

Create virtual environment:
- Skip following and use root repo virtual environment if created
```bash
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

Install dependencies for extraction:
```bash
pip install -r ${REPO_ROOT}/extract/requirements.txt
```

Add `common_base` to `PYTHONPATH` environment variable as described in [project root README](/README.md)

Installing `playwright`:
- Note that `playwright` is required only if using `extract_stocks_bvc.py`
```bash
pip install -r requirements.playwright.txt
```

Installing `chromium` for `playwright`:
- https://github.com/scrapy-plugins/scrapy-playwright
```bash
playwright install chromium
```

In case of required by playwright:
```bash
sudo apt-get install libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libwayland-client0
```

## Usage

Modules examples:
```python
from extract_metrics import extract_metrics
from extract_stocks_bvc import extract_stocks_bvc

extract_metrics(output_dest="/data/", stocks_demo=True)
extract_metrics(output_dest="/data/", stocks_file="/data/stocks-file.json")
extract_stocks_bvc(output_dest="/data/")
```

Shell examples:
```bash
# extracting metrics of demo stocks
python3 extract_metrics.py --output-dest /data/
python3 extract_metrics.py -o /data/
DEBUG=1 OUTPUT_DEST=/data/ python3 extract_metrics.py

# extracting metrics of custom stocks
python3 extract_metrics.py --output-dest /data/ --stocks-file /data/stocks-file.json
python3 extract_metrics.py -o /data/ -s /data/stocks-file.json
OUTPUT_DEST=/data/ STOCKS_FILE=/data/stocks-file.json python3 extract_metrics.py

# extracting stocks tickers from BVC
python3 extract_stocks_bvc.py --output-dest /data/
python3 extract_stocks_bvc.py -o /data/
OUTPUT_DEST=/data/ python3 extract_stocks_bvc.py
```

Notes:
- command line arguments take precedence over command line variables

Files `.env` or `envvars` with environment variables are also supported:
```
OUTPUT_DEST=/data/
STOCKS_FILE=/data/stocks-file.json
```

```bash
python3 extract_metrics.py
python3 extract_stocks_bvc.py
```
Notes:
- command line variables takes precedence over environment files
- `envvars` file takes precedence over `.env` file
- either environment file must be in current working directory
- VSCode debugger sets project workspace as current working directory

## Description

Sources:
- `google` - Google finance
- `investing` - https://www.investing.com/equities/
- `republica` - https://www.larepublica.co/indicadores-economicos/movimiento-accionario


Additional links:
- Colombian ADRs list: https://www.investing.com/equities/colombia-adrs
- Colombian BVC stocks list: https://www.investing.com/equities/colombia


Notes:
- Colombian stocks information is not available on Google Finance nor Yahoo Finance.

## Technical considerations

- `pyopenssl==22.0.0`:
    - https://stackoverflow.com/questions/73859249/attributeerror-module-openssl-ssl-has-no-attribute-sslv3-method
    - https://stackoverflow.com/questions/73861078/scrapy-attributeerror-module-openssl-ssl
