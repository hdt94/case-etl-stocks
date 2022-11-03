from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


@dag(
    start_date=datetime(2010, 1, 1),
    catchup=False,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=10),
)
def etl_stocks():
    @task.virtualenv(
        task_id="extract",
        requirements=["Scrapy==2.6.2", "pyopenssl==22.0.0",],
        system_site_packages=True,
    )
    def extract(output_dest):
        from extract_metrics import extract_metrics

        output_file = extract_metrics(output_dest=output_dest, stocks_demo=True)

        return output_file


    stocks_csv_file = extract("{{ var.value.get('extract_output_dest') }}")
    SparkSubmitOperator(
        task_id="transform",
        conn_id="spark_local",
        application="{{ var.value.get('transform_spark_app') }}",
        application_args=[
            "--input-csv", stocks_csv_file,
            "--output-dest", "{{ var.value.get('transform_output_dest') }}"
            # "--output-dest", "/home/vagrant/etl-stocks/output-airflow"
        ],
    )


# TaskFlow API v2.3.X requires creating and assigning a DAG instance
dag = etl_stocks()
