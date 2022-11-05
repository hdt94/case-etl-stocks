#!/bin/bash

set -e

if [[ -z $REPO_ROOT ]]; then
    echo 'REPO_ROOT is undefined' >&2
    exit 1
fi
if [[ -z $GCP_PROJECT_ID ]]; then
    if [[ $GOOGLE_CLOUD_SHELL = true || $CLOUD_SHELL = true ]]; then
        GCP_PROJECT_ID=$DEVSHELL_PROJECT_ID
    else
        echo 'GCP_PROJECT_ID is undefined' >&2
        exit 1
    fi
fi
if [[ -z $GCP_REGION ]]; then
    echo 'GCP_REGION is undefined' >&2
    exit 1
fi


TERRAFORM_DIR=$REPO_ROOT/infrastructure/gcp/terraform

terraform -chdir=$TERRAFORM_DIR init
terraform -chdir=$TERRAFORM_DIR apply \
    -var PROJECT_ID=${GCP_PROJECT_ID} \
    -var REGION=${GCP_REGION}

gcloud compute networks subnets update default \
    --region=${GCP_REGION} \
    --enable-private-ip-google-access
