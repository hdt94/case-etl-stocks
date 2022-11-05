from datetime import datetime, timedelta

from airflow.decorators import dag, task
# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateBatchOperator, DataprocDeleteBatchOperator, DataprocGetBatchOperator, DataprocListBatchesOperator
)

@dag(
    start_date=datetime(2010, 1, 1),
    catchup=False,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=10),
)
def etl_stocks():
    @task.virtualenv(
        task_id="extract",
        requirements=["Scrapy==2.6.2", "pyopenssl==22.0.0", "attrs==22.1.0"],
        system_site_packages=True,
    )
    def extract(output_dest):
        from extract.extract_metrics import extract_metrics

        output_file = extract_metrics(output_dest=output_dest, stocks_demo=True)

        return output_file


    stocks_csv_file = extract("{{ var.value.get('extract_output_dest') }}")

    # SparkSubmitOperator(
    #     task_id="transform",
    #     conn_id="spark_local",
    #     application="{{ var.value.get('transform_spark_app') }}",
    #     application_args=[
    #         "--input-csv", stocks_csv_file,
    #         "--output-dest", "{{ var.value.get('transform_output_dest') }}"
    #         # "--output-dest", "/home/vagrant/etl-stocks/output-airflow"
    #     ],
    # )

    # https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/operators/dataproc/index.html#airflow.providers.google.cloud.operators.dataproc.DataprocCreateBatchOperator
    # https://cloud.google.com/dataproc-serverless/docs/reference/rpc/google.cloud.dataproc.v1#google.cloud.dataproc.v1.PySparkBatch
    # https://cloud.google.com/dataproc-serverless/docs/reference/rest/v1/projects.locations.batches#PySparkBatch
    create_batch = DataprocCreateBatchOperator(
        task_id="batch_job_transform",
        region="{{ var.value.get('transform_dataproc_region', 'us-central1') }}",
        # batch_id="transform-{{ ts_nodash }}", # doesn't work as it contains uppercase T

        # Option 1
        # batch_id="transform-{{ macros.datetime.now().strftime('%Y%m%d%H%M%S') }}",

        # Option 2
        batch_id="transform-{{ macros.datetime.strptime(ts_nodash, '%Y%m%dT%H%M%S').strftime('%Y%m%d%H%M%S') }}",
        batch={
            "pyspark_batch": {
                "main_python_file_uri": "{{ var.value.get('transform_spark_app') }}",
                # "python_file_uris": "{{ var.value.get('transform_spark_pyfiles') }}", ERROR
                "python_file_uris": ["{{ var.value.get('transform_spark_pyfiles') }}"],
                # "file_uris": "{{ var.value.get('transform_spark_pyfiles') }}",
                "args": [
                    "--input-csv", stocks_csv_file,
                    "--output-dest", "{{ var.value.get('transform_output_dest') }}"
                ],
            },
            # "environment_config": {
            #     "peripherals_config": {
            #         "spark_history_server_config": {
            #             "dataproc_cluster": PHS_CLUSTER_PATH,
            #         },
            #     },
            # },
        },
    )


# TaskFlow API v2.3.X requires creating and assigning a DAG instance
dag = etl_stocks()
