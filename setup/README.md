# Requirements
1. Create bucket in the destination account
2. CLI access to the account

# Deploy Template
1. Install requests
```
cd encrypt_key
pip install requests -t .
```

2. Use the `cloudformation package` command to package up the lambda function and send it to S3. This command will output the update cloudformation template to deploy.
```
aws cloudformation package --s3-bucket northern-wisconsin-meetup-bucket --template-file cloudformation.template.yml --output-template-file cloudformation.yml --region us-east-1
```

3. Use the `cloudformation deploy` command to deploy the template output by the above command.
```
aws cloudformation deploy --template-file cloudformation.yml --stack-name Rekognition-Meetup --capabilities CAPABILITY_IAM --parameter-overrides MeetupApiKey=<API_KEY> --region us-east-1
```