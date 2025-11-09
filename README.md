# Project README

## Overview

This project is written in **Python** with **pytest** framework and uses **pip** for dependency management.

It interacts with AWS S3 service and performs automated tests.

## Setup

### 1. Set AWS Credentials as Environment Variables

Before running the project or tests, set your AWS credentials in your environment:

```
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=eu-central-1
```

Replace `your_access_key_id` and `your_secret_access_key` with your actual AWS credentials.

### 2. Run Tests

To run the tests, use:

```sh
pytest -v
```

Make sure you have installed all dependencies with:

```
pip install -r requirements.txt
```

There are custom markers used in the tests. To run tests with specific markers, use:

```
- default: to run tests from initial tasks
- extra: to run tests from extra tasks
```

### 3. AWS Region

Any AWS region can be used for this project.

AWS region  `eu-central-1`was used during tests.

## Limitations

- If your code creates S3 buckets, bucket names must be globally unique across all AWS accounts.
- Ensure your AWS credentials have the necessary permissions for the services used in this project.