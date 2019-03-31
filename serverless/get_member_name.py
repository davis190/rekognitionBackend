#!/Users/kevin/.virtualenvs/RekognitionBackend/bin/python

import boto3
import os
from contextlib import closing
from botocore.client import Config
from botocore.exceptions import ClientError


def search_by_id(id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['dynamoDbTableName'])  # Change the DynamoDB table name
    response = table.get_item(
        Key={
            "memberId": id,
            # "meetupId": os.environ['eventId']
        }
    )
    print response
    item = response['Item']
    print(item["name"])
    return item["name"]

def handler(event, context):
    if 'AWS_LAMBDA_FUNCTION_VERSION' in os.environ:
        print(event)
        id = str(event['queryStringParameters']['id'])
    else:
        id = "000000000"  # Hard-coded id goes here for local testing.
    name = search_by_id(id)
    ## Use polly to craft greeting
    pollyClient = boto3.client('polly', region_name='us-east-1')
    response = pollyClient.synthesize_speech(
        OutputFormat='mp3',
        Text='Welcome '+name,
        VoiceId='Russell'
        #VoiceId='Geraint'|'Gwyneth'|'Mads'|'Naja'|'Hans'|'Marlene'|'Nicole'|'Russell'|'Amy'|'Brian'|'Emma'|'Raveena'|'Ivy'|'Joanna'|'Joey'|'Justin'|'Kendra'|'Kimberly'|'Matthew'|'Salli'|'Conchita'|'Enrique'|'Miguel'|'Penelope'|'Chantal'|'Celine'|'Mathieu'|'Dora'|'Karl'|'Carla'|'Giorgio'|'Mizuki'|'Liv'|'Lotte'|'Ruben'|'Ewa'|'Jacek'|'Jan'|'Maja'|'Ricardo'|'Vitoria'|'Cristiano'|'Ines'|'Carmen'|'Maxim'|'Tatyana'|'Astrid'|'Filiz'|'Vicki'|'Takumi'|'Seoyeon'|'Aditi'
    )
    print (response['AudioStream'])
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            try:
                # Open a file for writing the output as a binary stream
                print('reading stream')
                readStream = stream.read()
                s3 = boto3.resource('s3')
                faceFile = s3.Object(os.environ['s3Bucket'],'audio_files/'+name+".mp3")
                faceFile.put(ACL='public-read',Body=readStream)
                audioStringReturn="https://s3.amazonaws.com/"+os.environ['s3Bucket']+"/audio_files/"+name.replace(" ", "+")+".mp3"
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
    print {"statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS'
            },
            "body": "{\"name\": \"" + name + "\", \"audioFile\": \"" + audioStringReturn + "\"}"}

    return {"statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS'
            },
            "body": "{\"name\": \"" + name + "\", \"audioFile\": \"" + audioStringReturn + "\"}"}

if __name__ == '__main__':
    handler("event", "context")  # Allows for local execution / testing. This gets ignored by AWS Lambda.