import pickle
import boto3
import os
from botocore.exceptions import NoCredentialsError
import s3.json


class Serialization:
    
    def AWSupload(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def AWSdownload():
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY , aws_secret_access_key=SECRET_KEY)
    try:
        s3.download_file(bucket,'dogs', 'C:\\Users\\fhm\\Desktop\\dogs')
        print("Download Successful")
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
        else:
            raise

    
    




