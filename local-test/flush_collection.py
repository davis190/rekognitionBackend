#!/Users/kevin/.virtualenvs/RekognitionBackend/bin/python

import json
import requests
import boto3
from base64 import b64decode
import urllib
import os

rekognition = boto3.client("rekognition", 'us-east-1')
faces = rekognition.list_faces(CollectionId=os.environ['collectionId'])

for face in faces["Faces"]:
  response = rekognition.delete_faces(CollectionId=os.environ['collectionId'], FaceIds=[face["FaceId"]])
