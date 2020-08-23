validate_cloudformation:
	aws cloudformation validate-template --template-body file://cloudformation.yml

deploy_cloudformation:
	aws cloudformation deploy --template-file cloudformation.yml --stack-name webdungeon --capabilities CAPABILITY_IAM