
# Name the lambda will be known as in AWS. If you change it then
# change the lambda function file to match
PROJECT = lambda_function
#  If changing this handler name then change the handler
# function name to match. You shouldn't need to though.
FUNCTION = lambda_handler
# Set the runtime
RUNTIME = 'python3.7'

# ------------- ARN of execution role -------------
LAMBDA_ROLE = arn:aws:iam::nnnnnnnnnnnnn:role/lambda-role

# ------------- Basic settings -------------
# Description as appears in AWS
DESCRIPTION = "My Demo Description"
# Region to deploy lambda
AWS_REGION = eu-west-2
# Memory to allocate to lambda
MEMORY = 128
# Timeout in seconds
TIMEOUT = 15

# ------------- Local directories for development -------------
NONPROD = ../../nonprod
PACKAGE = ./package
PACKAGE_TMP = ./package/tmp
PROD = ../../prod


# Tasks
build: clean build_package_tmp zip

build_package_tmp:
	mkdir -p $(PACKAGE_TMP)
	pip freeze > requirements.txt
	pip install -r requirements.txt -t $(PACKAGE_TMP)
	cp -a ./src/* $(PACKAGE_TMP)

clean:
	rm -rf ./package/*

# Copy the lambda handler and zip archive to our non prod directory
deliver_nonprod:
	cp $(PACKAGE_TMP)/$(PROJECT).py $(NONPROD)
	cp $(PACKAGE)/$(PROJECT).zip $(NONPROD)

# Copy the lambda handler and zip archive to our prod directory
deliver_prod:
	cp $(PACKAGE_TMP)/$(PROJECT).py $(PROD)
	cp $(PACKAGE)/$(PROJECT).zip $(PROD)

# Delete the Lambda from the AWS account
lambda_delete:
	aws lambda delete-function \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION)

# Deploy the Lambda to the AWS account
lambda_deploy:
	aws lambda create-function \
	    --description $(DESCRIPTION) \
		--region $(AWS_REGION) \
		--function-name $(FUNCTION) \
		--zip-file fileb://./package/$(PROJECT).zip \
		--role $(LAMBDA_ROLE) \
		--handler $(PROJECT).$(FUNCTION) \
		--runtime $(RUNTIME) \
		--timeout $(TIMEOUT) \
		--memory-size $(MEMORY)

# Retrieve the configuration from AWS
lambda_get_function_configuration:
	aws lambda get-function-configuration \
		--function-name $(FUNCTION)

# Update just the code on AWS, not the configuration
lambda_update_function_code:
	aws lambda update-function-code \
		--function-name $(FUNCTION) \
		--zip-file fileb://./package/$(PROJECT).zip

tasks:
	@echo "	---------------------------------------"
	@echo "	Lambda Template Default Make Task List:"
	@echo "	---------------------------------------"
	@echo "	build: Delete existing local Lambda package and build new one."
	@echo "	clean: Delete existing local Lambda package."
	@echo "	deliver_nonprod: Deliver the lambda handler and zip to ../nonprod dir"
	@echo "	deliver_prod: Deliver the lambda handler and zip to ../prod dir"
	@echo "	lambda_delete: Delete the Lambda from the AWS account."
	@echo "	lambda_deploy: Deploy the Lambda to the AWS account."
	@echo "	lambda_get_function_configuration: Retrieve the configuration from AWS."
	@echo "	lambda_update_function_code: Update just the code on AWS, not the configuration."
	@echo "	tasks: Display this list of tasks."
	@echo "	test: Run the unit tests"
	@echo "	---------------------------------------"

test:
	python src/test_lambda.py

zip:
	cd $(PACKAGE_TMP) && zip -r ../$(PROJECT).zip .
