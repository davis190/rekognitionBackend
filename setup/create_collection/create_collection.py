import boto3
import json
from botocore.exceptions import ClientError
import requests

client = boto3.client('rekognition')

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
        try:
            response = client.create_collection(
                CollectionId=event['ResourceProperties']['collection_id']
            )

            print(response)

            responseData = {'collection_arn': response['CollectionArn']}
            cfn_response(event, context, 'SUCCESS', responseData)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                print("ResourceAlreadyExistsException Failure")
                responseData = {'Error': 'ResourceAlreadyExistsException'}
            else:
                print("Unexpected error: %s" % e)
                responseData = {}
            cfn_response(event, context, 'FAILED', responseData)

    elif event['RequestType'] == "Delete":
        response = client.delete_collection(
            CollectionId=event['ResourceProperties']['collection_id']
        )
        print(response)

        cfn_response(event, context, 'SUCCESS', responseData)
    else:
        responseData = {}
        cfn_response(event, context, 'SUCCESS', responseData)