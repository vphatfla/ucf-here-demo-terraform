#! /usr/bin/env python3
import logging
import json
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
def handler(event, context):
    mainFolder = 'face-reko/'
    try:
        LOGGER.info('SQS EVENT: %s', event)
        for sqs_rec in event['Records']:
            s3_event = json.loads(sqs_rec['body'])
            #LOGGER.info('S3 EVENT : %s', s3_event)
            # Skipping S3 test event
            if 'Event' in s3_event.keys() and s3_event['Event'] == 's3:TestEvent':
                break
            for s3_rec in s3_event['Records']:
                bucket_name = s3_rec['s3']['bucket']['name']
                object_key = s3_rec['s3']['object']['key']
                parts = object_key.split('/')
                object_folder = parts[0]   
                 
                LOGGER.info('Bucket name: %s', bucket_name)
                LOGGER.info('Object key: %s', object_key)
                LOGGER.info('Object folder: %s', object_folder)
                
                if (parts[1] == 'init.png'):
                    LOGGER.info('THIS IS INIT IMAGE')
                else:
                    LOGGER.info('This is NOT init, comparing face')
                    init_image = object_folder + '/init.png'
                    LOGGER.info('init image key = ' + init_image)
                    resp = compareFace(bucket_name, init_image, object_key)
                    LOGGER.info('Compare result :%s', str(resp))
                    
    except Exception as exception:
        LOGGER.error('Exception: %s', exception)
        raise


def compareFace(bucket_name, init_image, target_image):
    reko=boto3.client('rekognition')
    LOGGER.info('Inside compareFace bucketname = %s     init image = %s   and target image = %s', bucket_name, init_image, target_image)
    try:
        resp = reko.compare_faces(
            SourceImage={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': init_image,
            }},
            TargetImage={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': target_image,
            }}
        )
        return resp
    
    except Exception as exception:
        LOGGER.error('Exception: %s', exception)
        raise