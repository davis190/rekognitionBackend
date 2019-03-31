import boto3
import os
import requests
import json
import base64

client = boto3.client('kms')

def cfn_response(event, context, status, responseData):
    responseBody = {'Status': status,
                    'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': responseData}
    print('RESPONSE BODY:n' + json.dumps(responseBody))

    req = requests.put(event['ResponseURL'], data=json.dumps(responseBody))
    print("Status Code: " + str(req.status_code))

def handler(event, context):
    print(event)
    if event['RequestType'] == "Create":
        responseData = {}

        plain_text_string=event['ResourceProperties']['plain_text_string']
        response = client.encrypt(
            KeyId=os.environ['KMS_KEY'],
            Plaintext=plain_text_string
        )
        print(response)
        encrypted_string=str(base64.b64encode(response['CiphertextBlob']), 'utf-8')

        responseData = {'encrypted_string': encrypted_string}
        cfn_response(event, context, 'SUCCESS', responseData)
    else:
        responseData = {}
        cfn_response(event, context, 'SUCCESS', responseData)

