#!/bin/bash

# TODO: Build doker images from array of Blender versions

REPO_ECR_NAME=$1
BLENDER_VERSIONS=$2
AWS_ACCOUNT_ID=$3
AWS_DEFAULT_REGION=$4

echo "Building docker images for Blender versions: $BLENDER_VERSIONS"
echo "AWS ECR Repository: $REPO_ECR_NAME"
echo "AWS Account ID: $AWS_ACCOUNT_ID"
echo "AWS Default Region: $AWS_DEFAULT_REGION"

get_major_version() {
    major_version=$1
    echo "$major_version"
}

get_full_version() {
    version=$1
    full_version="${version%.*}"  # Extraer la versión principal
    echo "$full_version"
}

image_exists_in_ecr() {
    major_version=$1
    # echo "Checking if image exists in ECR for major_version: $major_version"
    image_exists=$(docker manifest inspect $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$REPO_ECR_NAME:$major_version 2>&1)

    # echo "Image exists: $image_exists"
    
    if [[ $image_exists == *"no such manifest"* ]]; then
        echo "false"
    else
        echo "true"
    fi
}

IFS=',' read -ra VERSION_ARRAY <<< "$BLENDER_VERSIONS"

for VERSION in "${VERSION_ARRAY[@]}"; do 
    major_version=$(get_major_version $VERSION)
    full_version=$(get_full_version $VERSION)
    echo "Building docker image for Blender version: $full_version with major version: $major_version"
    exists=$(image_exists_in_ecr $major_version)
    echo "Image exists in ECR: $exists"
    if [[ $exists == "false" ]]; then
        echo "Image does not exist in ECR"
    else
        echo "Docker image for Blender version: $full_version already exists in ECR"
    fi

done