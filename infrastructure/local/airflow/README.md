# Setup

Install base local environment described in [repo root README](/README.md)

Using `pip`:
```bash
pip install -r ${REPO_ROOT}/infrastructure/local/airflow/requirements.txt
```

Using `conda`:
```bash
conda install -c conda-forge "$(sed 's|apache-airflow|airflow|' ${REPO_ROOT}/infrastructure/local/airflow/requirements.txt)"
```

If running Airflow locally in systems with SQLite system library < 3.15.0, then follow instructions at ["Troubleshooting old SQLite version"](#troubleshooting-old-sqlite-version).

If running `SparkSubmitOperator` install `apache-airflow-providers-apache-spark`:
- Using `pip`:
    - https://pypi.org/project/apache-airflow-providers-apache-spark/
    ```bash
    pip install apache-airflow-providers-apache-spark
    ```
- Using `conda`:
    - https://anaconda.org/conda-forge/apache-airflow-providers-apache-spark
    ```bash
    conda install -c conda-forge --file ${REPO_ROOT}/infrastructure/local/airflow/requirements.spark.txt
    ```

```bash
set -a; source envvars; set +a;
airflow info
```

Add Airflow connection to local Spark:
```
airflow connections add spark_local --conn-type spark --conn-host local
```

## Troubleshooting old SQLite version

Search and download up to date SQLite binary at [https://www.sqlite.org/download.html](https://www.sqlite.org/download.html):
```bash
curl -LO https://www.sqlite.org/2022/sqlite-tools-linux-x86-3390200.zip
unzip sqlite-tools-linux-x86-3390200.zip
```

Copy SQLite binary to `/bin` directory and add `/bin/` to `LD_LIBRARY_PATH` environment variable:
```bash
sudo cp sqlite-tools-linux-x86-3390200/sqlite3 /bin/
```
- If `LD_LIBRARY_PATH` is not defined:
    ```bash
        echo -e "\nLD_LIBRARY_PATH=/bin\n" >> /etc/environment
    ```
- If `LD_LIBRARY_PATH` is defined then edit `/etc/environment` manually.

Create Python environment using `conda`:
- Option 1: `venv` environment based on `conda` distribution
    ```bash
    conda create -n venv-conda python=3.8
    conda activate venv-conda
    python -m venv venv-conda
    conda deactivate
    source venv-conda/bin/activate
    pip install --upgrade pip
    ```
- Option 2: `conda` environment
    - note `conda` packager functionalities may be slow for low-memory systems
    ```bash
    conda create -n etl-stocks python=3.8
    conda activate etl-stocks
    ```

Test SQLite version:
```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"  # 3.39.4
```

Install Airflow:
- If choosed option 1:
    ```bash
    pip install -r ${REPO_ROOT}/infrastructure/local/airflow/requirements.airflow.txt
    ```
- If choosed option 2:
    ```bash
    conda install -c conda-forge "$(sed 's|apache-airflow|airflow|' ${REPO_ROOT}/infrastructure/local/airflow/requirements.airflow.txt)"
    ```

Test Airflow:
```bash
airflow info
```

Install all dependencies indicated in [root README](/README.md)


# References
- https://airflow.apache.org/docs/apache-airflow/stable/modules_management.html
