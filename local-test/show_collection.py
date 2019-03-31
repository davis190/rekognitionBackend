#!/Users/kevin/.virtualenvs/RekognitionBackend/bin/python

import json
import boto3
import os

rekognition = boto3.client("rekognition", 'us-east-1')
faces = rekognition.list_faces(CollectionId=os.environ['collectionId'])

for face in faces["Faces"]:
  print face
  print "\n"

print len(faces["Faces"])