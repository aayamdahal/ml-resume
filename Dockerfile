# AWS Lambda Docker Image for Resume Ranking API
FROM public.ecr.aws/lambda/python:3.13

# Install system dependencies for building Python packages
RUN dnf install -y gcc gcc-c++ make && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copy application code
COPY app.py ${LAMBDA_TASK_ROOT}/
COPY config.py ${LAMBDA_TASK_ROOT}/
COPY extractor.py ${LAMBDA_TASK_ROOT}/
COPY parser.py ${LAMBDA_TASK_ROOT}/
COPY ranker.py ${LAMBDA_TASK_ROOT}/
COPY utils.py ${LAMBDA_TASK_ROOT}/
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/

# Set the Lambda handler
CMD ["lambda_handler.lambda_handler"]
