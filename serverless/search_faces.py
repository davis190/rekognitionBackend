#!/Users/kevin/.virtualenvs/RekognitionBackend/bin/python

import boto3
import os
import json
from datetime import date
import random
import string
import base64

def upload_to_s3(photo):
    s3 = boto3.resource('s3')

    today = date.today()
    stringDate=str(today.year)+'-'+str(today.month)+'-'+str(today.day)
    randomString=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))
    fileName=stringDate+'_'+randomString+'.png'
    
    photoParts = photo.split(",")
    faceFile = s3.Object(os.environ['s3Bucket'],fileName)
    faceFile.put(Body=base64.b64decode(photoParts[1]))

    return fileName

def search_by_face(photo):
    match_info = {}
    rekognition = boto3.client("rekognition", "us-east-1")

    fileName = upload_to_s3(photo)

    response = rekognition.search_faces_by_image(
        CollectionId=os.environ['collectionId'],
        FaceMatchThreshold=95,
        Image={
            'S3Object': {
                'Bucket': os.environ['s3Bucket'],
                'Name': fileName,
            },
        },
        MaxFaces=1,
    )
    # print response
    if len(response["FaceMatches"]) != 1:
        match_info.update({'matched': False})
        match_info.update({'ExternalImageId': ''})
        return match_info
    else:
        match_info.update({'matched': True})
        match_info.update({'ExternalImageId': response["FaceMatches"][0]["Face"]["ExternalImageId"]})
        match_info.update({'Confidence': response['FaceMatches'][0]['Face']['Confidence']})
        return match_info


def handler(event, context):
    print(event)
    if 'AWS_LAMBDA_FUNCTION_VERSION' in os.environ:
        try:
            photo = str(event['queryStringParameters']['photo'])
            checkBodyForPhoto = False
        except:
            print("no query parameter")
            checkBodyForPhoto = True
        ## Allow passing in body parameters for larger input
        if checkBodyForPhoto:
            try:
                jsonBody = json.loads(event['body'])
                photo = str(jsonBody['photo'])
            except:
                print("no body parameter")
    else:
        photo = "ke-1.JPG"
    result = search_by_face(photo)
    if result['matched']:
        print "not matched"
        return {"statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS'
                },
                "body": "{\"matched\": " + "true," +
                "\"confidence\": " + str(result["Confidence"]) + ","
                "\"externalid\": \"" + str(result["ExternalImageId"]) + "\"}"}
    else:
        print "matched!"
        return {"statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET,POST,DELETE,PUT,OPTIONS'
                },
                "body": "{\"matched\": " + "false}"}


if __name__ == '__main__':
    handler("event", "context")  # Allows for local execution / testing. This gets ignored by AWS Lambda.
