#! /usr/bin/env python3
import logging
import json
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
def handler(event, context):
    mainFolder = 'face-reko/'
    try:
        LOGGER.info('SQS EVENT: %s', event)
        for sqs_rec in event['Records']:
            s3_event = json.loads(sqs_rec['body'])
            LOGGER.info('S3 EVENT : %s', s3_event)
            # Skipping S3 test event
            if 'Event' in s3_event.keys() and s3_event['Event'] == 's3:TestEvent':
                break
            for s3_rec in s3_event['Record']:
                bucket_name = s3_rec['s3']['bucket']['name']
                object_key = s3_rec['s3']['object']['key']
                parts = object_key.split('/')
                object_folder = parts[1]
                LOGGER.info('Bucket name: %s', bucket_name)
                LOGGER.info('Object key: %s', object_key)
                LOGGER.info('Object folder: %s', object_folder)
                if (parts[2] == 'init.png'):
                    LOGGER.info('THIS IS INIT IMAGE')
    except Exception as exception:
        LOGGER.error('Exception: %s', exception)
        raise