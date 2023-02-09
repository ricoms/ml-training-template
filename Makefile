## The Makefile includes instructions on environment setup and lint tests
# Create and activate a virtual environment
# Install dependencies in requirements.txt
# Dockerfile should pass hadolint
# app.py should pass pylint
# (Optional) Build a simple integration test

project-name=ml-training-template
DOCKER_IMAGE_NAME=workshop-ml-training-template

hyperparameters_file=ml/input/config/hyperparameters.json
hyperparameters=`cat ${hyperparameters_file}`

CURRENT_UID := $(shell id -u)
time-stamp=$(shell date "+%Y-%m-%d-%H%M%S")

install:
	poetry install --no-dev

dev: install
	poetry install

data:
	wget https://archive.ics.uci.edu/ml/machine-learning-databases/00497/divorce.rar -P ml/input/data/training/
	cd ml/input/data/training/ && unrar e divorce.rar
	cd ml/input/data/training/ && rm divorce.rar && rm divorce.xlsx

train: build-image ml/input/data/training/divorce.csv
	docker run --rm \
		-u ${CURRENT_UID}:${CURRENT_UID} \
		-v ${PWD}/ml:/opt/ml \
		${DOCKER_IMAGE_NAME} python ml_training_template/train \
			--project_name ${project-name} \
			--input_dir /opt/ml/input/data/training/divorce.csv

clean:
	rm -r ml/output/divorce
	rm ml/output/model.tar.gz

# CICD commands

lint-docker:
	docker run --rm -i hadolint/hadolint:v1.17.6-3-g8da4f4e-alpine < Dockerfile

lint-python:
	pipenv run flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	pipenv run flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

lint: lint-docker lint-python

test:
	# Additional, optional, tests could go here
	pipenv run pytest -v
	
coverage:
	pipenv run pytest --cov-report=term-missing --cov=src --cov-fail-under=0.6
	pipenv run pytest --cov-report=html --cov=src

build-image:
	docker build -f Dockerfile -t ${DOCKER_IMAGE_NAME} .
