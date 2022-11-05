#!/bin/bash

set -e

REPO_ROOT=$(realpath $(dirname $0))
SCRIPTS_DIR=${REPO_ROOT}/infrastructure/gcp/scripts


if [[ $RUN_ALL = true ]]; then
    APPLY_TERRAFORM=true
    UPLOAD_COMPOSER_DAGS=true
    UPDATE_COMPOSER_VARIABLES=true
    UPLOAD_SPARK_JOB=true
fi

if [[ $APPLY_TERRAFORM = true ]]; then
    GCP_PROJECT_ID=$GCP_PROJECT_ID \
    GCP_REGION=$GCP_REGION \
    REPO_ROOT="$REPO_ROOT" \
    ${SCRIPTS_DIR}/apply-terraform.sh
fi

TERRAFORM_DIR=${REPO_ROOT}/infrastructure/gcp/terraform
TERRAFORM_OUTPUT=$(terraform -chdir=$TERRAFORM_DIR output -json)

if [[ $TERRAFORM_OUTPUT == "{}" ]]; then
    echo "Terraform output is unexpectedly empty" >&2
    exit 1
fi

if [[ $UPLOAD_SPARK_JOB = true ]]; then
    REPO_ROOT="$REPO_ROOT" \
    SPARK_JOBS_DEST="$(echo "$TERRAFORM_OUTPUT" | jq -r .gs_spark_jobs.value)" \
    ${SCRIPTS_DIR}/upload-spark-job.sh
fi

if [[ $UPDATE_COMPOSER_VARIABLES = true || $UPLOAD_COMPOSER_DAGS = true ]]; then
    COMPOSER_OUTPUT="$(echo "$TERRAFORM_OUTPUT" | jq -c .composer_env.value)"

    COMPOSER_ENV_LOCATION="$(echo "$COMPOSER_OUTPUT" | jq -r .location)" \
    COMPOSER_ENV_NAME="$(echo "$COMPOSER_OUTPUT" | jq -r .name)" \
    REPO_ROOT="$REPO_ROOT" \
    UPLOAD_COMPOSER_DAGS="$UPLOAD_COMPOSER_DAGS" \
    UPDATE_COMPOSER_VARIABLES="$UPDATE_COMPOSER_VARIABLES" \
    ${SCRIPTS_DIR}/update-composer-env.sh
fi
