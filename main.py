import boto3
from users import getuser, send_mail
import json
import pandas as pd
import datetime
# from datetime import datetime, timezone

iam = boto3.client('iam')

# List access keys through the pagination interface.
paginator = iam.get_paginator('list_access_keys')
keys = []
new_keys = []
usersdict = getuser()
# Creating the loop for iam keys to be deleted
# case 1 : user has single key which is deleted and new one is created
# case 2 : User has two keys 
# case 2 A: if key 1 is > 30 days it will be deleted and new one is created
# case 2 B: if key 2 is > 30 days it will be deleted and new one is creaated
# case 3 c: if both the keys are < 30 , compare and get the new one and delete the old one
for iamuser in usersdict:
    for response in paginator.paginate(UserName=iamuser):
        if len(response['AccessKeyMetadata']) == 1:
            old_key = response['AccessKeyMetadata'][0]
            new_key_response = iam.create_access_key(UserName=iamuser)
            iam.delete_access_key(
                AccessKeyId=old_key['AccessKeyId'],
                UserName=iamuser)
            new_keys.append((iamuser, new_key_response))
            
        elif len(response['AccessKeyMetadata']) == 2:
            key1 = response['AccessKeyMetadata'][0]
            key2 = response['AccessKeyMetadata'][1]
            flag=False
            if datetime.datetime.now() - datetime.timedelta(days=30) > key1['CreateDate'].replace(tzinfo=None):
                iam.delete_access_key(
                AccessKeyId=key1['AccessKeyId'],
                UserName=iamuser)
                flag=True
            if datetime.datetime.now() - datetime.timedelta(days=30) > key2['CreateDate'].replace(tzinfo=None):
                iam.delete_access_key(
                AccessKeyId=key2['AccessKeyId'],
                UserName=iamuser)
                flag=True
            if flag==False:
                if key1['CreateDate'] < key2['CreateDate']: 
                    key_to_del = key1
                    print('delete key1', key1['AccessKeyId'])
                else:
                    key_to_del = key2
                    print('delete key2', key2['AccessKeyId'])
                iam.delete_access_key(
                AccessKeyId=key_to_del['AccessKeyId'],
                UserName=iamuser)
            
            new_key_response = iam.create_access_key(UserName=iamuser)
            new_keys.append((iamuser, new_key_response))
        else:
            print("More than 2 keys")
        print(iamuser)
# sending email with secret key and access key for the respective users
        send_mail(iamuser,new_key_response,usersdict[iamuser])
        # for x in response['AccessKeyMetadata']:
        #     keys.append((x['UserName'], x['AccessKeyId']))


new_keys_df = pd.DataFrame(new_keys)
new_keys_df.columns = ['IAM_USER', 'KEY']
new_keys_df.to_csv('new_iam_file.csv', index=False)
