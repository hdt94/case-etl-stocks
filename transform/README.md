# Transform stocks data

TODO: drop `source_id`?

## Up and running for development

Create virtual environment:
- Skip following and use root repo virtual environment if created
- Using `pip`:
    ```bash
    python3.8 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r ${REPO_ROOT}/common/requirements.common_base.txt
    ```
- Using `conda`:
    ```bash
    conda create -n etl-stocks python=3.8
    conda activate etl-stocks
    conda install --file ${REPO_ROOT}/common/requirements.common_base.txt
    ```

Install either `pandas` or `pyspark`:
- Using `pip`:
    ```bash
    pip install -r requirements.pandas.txt
    pip install -r requirements.spark.txt
    ```
- Using `conda`:
    ```bash
    conda install --file requirements.pandas.txt
    conda install --file requirements.spark.txt
    ```

Running scripts:
- Add `common_base` to `PYTHONPATH` environment variable as described in [project root README](/README.md)
```bash
# Using arguments
INPUT_CSV_TRANSFORM=
OUTPUT_DEST_TRANSFORM=
python ${REPO_ROOT}/transform/transform_investing_spark.py \
    --input-csv $INPUT_CSV_TRANSFORM \
    --output-dest $OUTPUT_DEST_TRANSFORM

# Using environment variables
INPUT_CSV_TRANSFORM= \
OUTPUT_DEST_TRANSFORM= \
python ${REPO_ROOT}/transform/transform_investing_spark.py
```

Copy `common_base` directory:
```bash
cp -r "$REPO_ROOT/common_base" "$REPO_ROOT/transform/common_base"
```

Running notebooks:
- Copy `common_base` directory:
    ```bash
    cp -r "$REPO_ROOT/common_base" "$REPO_ROOT/transform/common_base"
    ```
- Create `.env` file defining `INPUT_CSV_TRANSFORM`:
    ```
    INPUT_CSV_TRANSFORM=
    ```
- Use Jupyter or VSCode Notebooks
