all: clean lint test

MAJOR_VERSION := 1
MINOR_VERSION := 0
BUILD_VERSION ?= $(USER)
VERSION := $(MAJOR_VERSION).$(MINOR_VERSION).$(BUILD_VERSION)

ORGANIZATION := clickandobey
SERVICE_NAME := python-dockerized-webservice
PACKAGE_NAME := python-helloworld-webservice

PACKAGE_IMAGE_NAME := ${ORGANIZATION}-${SERVICE_NAME}-package

APP_IMAGE_NAME := ${ORGANIZATION}-${SERVICE_NAME}-app
GITHUB_REPO := "docker.pkg.github.com"
APP_REPO_IMAGE_NAME := ${GITHUB_REPO}/${ORGANIZATION}/${SERVICE_NAME}/${PACKAGE_NAME}:${VERSION}
APP_PORT := 9001
APP_CONTAINER_NAME := ${APP_IMAGE_NAME}

TEST_IMAGE_NAME := ${ORGANIZATION}-${SERVICE_NAME}-test

TEST_CONTAINER_NAME := ${TEST_IMAGE_NAME}
ROOT_DIRECTORY := `pwd`
PYTHON_PATH := ${ROOT_DIRECTORY}/src/main/python
SCRIPTS_PATH := ${ROOT_DIRECTORY}/src/main/scripts
TEST_DIRECTORY := ${ROOT_DIRECTORY}/src/test
TEST_PYTHON_PATH := $(PYTHON_PATH):$(TEST_DIRECTORY)/python

ifneq ($(DEBUG),)
  INTERACTIVE=--interactive
  PDB=--pdb
  DETACH=--env "DETACH=None"
else
  INTERACTIVE=--env "INTERACTIVE=None"
  PDB=
  DETACH=--detach
endif

ifneq (${LOUD_TESTS},)
  TEST_OUTPUT_FLAG=-s
else
  TEST_OUTPUT_FLAG=
endif

ifeq (${TEST_SPECIFIER},)
  TEST_STRING=
else
  TEST_STRING= and ${TEST_SPECIFIER}
endif

FAIL_FAST ?=
ifneq (${FAIL_FAST},)
	FAILURE_FLAG := -x
else
	FAILURE_FLAG :=
endif

# Code Packaging Targets

package: $(shell find src/main/python -name "*") docker/Dockerfile.package
	@docker build \
		-t ${PACKAGE_IMAGE_NAME} \
		-f docker/Dockerfile.package \
		.
	@docker run \
		--rm \
		--env VERSION=$(VERSION) \
		-v ${ROOT_DIRECTORY}/dist:/python/dist \
		${PACKAGE_IMAGE_NAME}
	@touch package

# Local App Targets

run-webservice:
	@export PYTHONPATH=${PYTHON_PATH}; \
	export VERSION=${VERSION}; \
	export ENVIRONMENT=localhost; \
	export CONFIGURATION_DIRECTORY=`pwd`/configuration; \
	cd ${PYTHON_PATH}; \
	pipenv run python ../scripts/run_webservice --debug

# Docker App Targets

docker-build-app: package docker/app/Dockerfile.app docker/app/run_webservice.sh
	@docker build \
		-t ${APP_IMAGE_NAME} \
		-f docker/app/Dockerfile.app \
		--build-arg VERSION=${VERSION} \
		.
	@touch docker-build-app

docker-run-webservice: docker-build-app stop-webservice
	@docker run \
		--rm \
		${DETACH} \
		${INTERACTIVE} \
		--env VERSION=${VERSION} \
		--env ENVIRONMENT=docker \
		--env EXPORT_AWS=${EXPORT_AWS} \
		--name ${APP_CONTAINER_NAME} \
		-p ${APP_PORT}:9001 \
		${APP_IMAGE_NAME}
	@`pwd`/src/test/scripts/wait_for_webapp ${APP_PORT}

stop-webservice:
	@docker kill ${APP_CONTAINER_NAME} || true

# Testing

build-test-docker: package docker/Dockerfile.test $(shell find src/test -name "*")
	@docker build \
		-t $(TEST_IMAGE_NAME) \
		-f docker/Dockerfile.test \
		--build-arg VERSION=${VERSION} \
		.
	@touch build-test-docker

test: unit-test integration-test
test-docker: unit-test-docker integration-test-docker

unit-test:
	@export PYTHONPATH=$(TEST_PYTHON_PATH); \
	cd $(PYTHON_PATH); \
	pipenv run pip install pytest; \
	pipenv run python -m pytest \
		--durations=10 \
		${TEST_OUTPUT_FLAG} \
		${FAILURE_FLAG} \
		-m 'unit ${TEST_STRING}' \
		../../test/python

unit-test-docker: build-test-docker
	@docker run \
		--rm \
		${INTERACTIVE} \
		--env VERSION=${VERSION} \
		--name ${TEST_CONTAINER_NAME} \
		${TEST_IMAGE_NAME} \
			--durations=10 \
			-x \
			-n 4 \
			-s \
			-m 'unit ${TEST_STRING}' \
			${PDB} \
			/test/python

integration-test: docker-run-webservice
	@export PYTHONPATH=$(TEST_PYTHON_PATH); \
	cd $(PYTHON_PATH); \
	pipenv run pip install pytest; \
	pipenv run python -m pytest \
		--durations=10 \
		${TEST_OUTPUT_FLAG} \
		${FAILURE_FLAG} \
		-m 'integration ${TEST_STRING}' \
		../../test/python

integration-test-docker: build-test-docker docker-run-webservice
	docker run \
		--rm \
		${INTERACTIVE} \
		--env "VERSION=${VERSION}" \
		--env "ENVIRONMENT=docker" \
		--name ${TEST_CONTAINER_NAME} \
		--link ${APP_CONTAINER_NAME} \
		${TEST_IMAGE_NAME} \
			--durations=10 \
			-x \
			-s \
			-m 'integration ${TEST_STRING}' \
			${PDB} \
			/test/python

# Release

release: docker-build-app github-docker-login
	@echo Tagging webservice image to ${APP_REPO_IMAGE_NAME}...
	@docker tag ${APP_IMAGE_NAME} ${APP_REPO_IMAGE_NAME}
	@echo Pushing webservice docker image to ${APP_REPO_IMAGE_NAME}...
	@docker push ${APP_REPO_IMAGE_NAME}

# Linting

lint: lint-markdown lint-python

lint-markdown:
	@echo Linting markdown files...
	@docker run \
		--rm \
		-v `pwd`:/workspace \
		wpengine/mdl \
			/workspace
	@echo Markdown linting complete.

lint-python:
	@echo Linting Python files...
	@docker build \
		-t ${SERVICE_NAME}/pylint \
		-f docker/Dockerfile.pylint \
		.
	@docker run --rm \
		${SERVICE_NAME}/pylint \
			pylint \
				--rcfile /workspace/.pylintrc \
				/src_workspace
	@echo Python linting complete

# Utilities

clean:
	@echo Cleaning Make Targets...
	@rm -f package
	@rm -f docker-build-app
	@rm -f build-test-docker
	@echo Cleaned Make Targets.
	@echo Removing Build Targets...
	@rm -rf ${ROOT_DIRECTORY}/dist
	@echo Removed Build Targets.

setup-env:
	@cd ${PYTHON_PATH}; \
	pipenv install --dev

update-dependencies:
	@cd ${PYTHON_PATH}; \
	pipenv lock

github-docker-login:
	@echo ${GITHUB_TOKEN} | docker login https://docker.pkg.github.com -u ${GITHUB_USER} --password-stdin