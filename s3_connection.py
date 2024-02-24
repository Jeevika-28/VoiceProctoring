import boto3
import logging
import os
import boto3

S3 = boto3.client(
    's3'
)

def list_bucket():
    
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        if response:
            print('Buckets exists..')
            for bucket in response['Buckets']:
                print(f'  {bucket["Name"]}')
    except Exception as e:
        logging.error(e)
        return False
    return True

def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except Exception as e:
        logging.error(e)
        return False
    return True

def upload_file(file_name, bucket, object_name=None):
    
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    try:
        response = S3.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True
upload_file('voicetotext.py','voiceproctor')
# upload_file('voiceproctor.py','voiceproctor')
def download_file(file_name, bucket, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

def delete_file(bucket, key_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=key_name)
        print('deleted')
    except Exception as e:
        logging.error(e)
        return False
    return True

def fetch_file_content_from_s3(bucket, object_name):

    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(Bucket=bucket, Key=object_name)
        file_content = response['Body'].read().decode('utf-8')
        return file_content
    except Exception as e:
        logging.error(e)
        return None

def update_file_on_s3(bucket, object_key, new_text):

    s3_client = boto3.client('s3')

    try:
        s3_client.put_object(Body=new_text, Bucket=bucket, Key=object_key)
        return True
    except Exception as e:
        print(f"Error updating file on S3: {e}")
        return False

# create_bucket('studentproctordata','eu-north-1')
# data=fetch_file_content_from_s3('assignmentcontent','content.txt')
# print(data)
# delete_file('voiceproctor','recorded_audio.wav')
# def get_file(bucket,key_name):
    

    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key_name)
    file_content = response['Body'].read().decode('utf-8')
    return file_content

def fetch_audio_from_s3(bucket_name, key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    audio_data = response['Body'].read()
    return audio_data