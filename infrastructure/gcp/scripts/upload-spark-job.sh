#!/bin/bash

set -e

if [[ -z $REPO_ROOT ]]; then
    echo 'REPO_ROOT is undefined' >&2
    exit 1
fi
if [[ -z $SPARK_JOBS_DEST ]]; then
    echo "SPARK_JOBS_DEST is undefined" >&2
    exit 1
fi


echo "Uploading Spark job based on: ${REPO_ROOT}"

TMP_JOB_DIR=$(mktemp -d -t etl-stocks-spark-job-XXXXXXX)
PYFILES_OUTPUT="${TMP_JOB_DIR}/transform_investing_spark_pyfiles.zip"

cp "${REPO_ROOT}/transform/transform_investing_spark.py" "${TMP_JOB_DIR}"

# Copy only .py files and .json files, including subdirectories
# Note that trailing forward-slash in sources is omitted to copy each directory
# Note that parsing environment variables is not used in cloud, so, ignoring common_base/ requirements
rsync -rm --include="*.py" --include="*.json" --include="*/" --exclude="*" \
    "${REPO_ROOT}/common/common_base" \
    "${REPO_ROOT}/transform/common" \
    "${TMP_JOB_DIR}"

pushd "${TMP_JOB_DIR}" && zip "${PYFILES_OUTPUT}" -r common/ -r common_base/ && popd
rm -r "${TMP_JOB_DIR}/common" "${TMP_JOB_DIR}/common_base"

# Copy contents from TMP_JOB_DIR
gsutil -mq rsync -r "${TMP_JOB_DIR}/" "${SPARK_JOBS_DEST}/transform_investing"

rm -rf "${TMP_JOB_DIR}"

echo -e "PySpark app:\t${SPARK_JOBS_DEST}/transform_investing/transform_investing_spark.py"
echo -e "PyFiles:\t${SPARK_JOBS_DEST}/transform_investing/transform_investing_spark_pyfiles.zip"
