import pickle
import boto3
import os
import json
from botocore.exceptions import NoCredentialsError


class Serialization():
    
    def readCredentials(self):
        with open('s3.json') as f:
            data = json.load(f)
        aws_access_key_id = data['ACCESS_KEY']
        aws_secret_access_key = data['SECRET_KEY']
        bucket = data['bucket']
        return aws_access_key_id,aws_secret_access_key,bucket

    def __init__(self):
        self.ACCESS_KEY, self.SECRET_KEY, self.bucket = self.readCredentials()
        self.s3 = boto3.client('s3', aws_access_key_id=self.ACCESS_KEY , aws_secret_access_key=self.SECRET_KEY)

    def AWSupload(self, local_file, bucket, s3_file):
        try:
            self.s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def AWSdownload(self):
        try:
            self.s3.download_file(self.bucket,'dogs', 'C:\\Users\\fhm\\Desktop\\dogs')
            print("Download Successful")
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
            else:
                raise

    
    




