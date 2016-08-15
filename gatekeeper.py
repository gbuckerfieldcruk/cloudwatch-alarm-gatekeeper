from __future__ import print_function
from datetime import datetime, time
# A Lambda function designed to control how Cloudwatch alarms are sent out.
# i.e. don't send alerts out-of-hours, unless the subject contains 'prod'.
import boto3
import json
 
print('Loading function')
 
 
def lambda_handler(event, context):
    
    # The SNS topic to forward alerts to:
    sns_alert_topic = 'arn:aws:sns:us-east-1:444455556666:MyTopic'
    
    sns_message = event['Records'][0]['Sns']['Message']
    sns_subject = event['Records'][0]['Sns']['Subject']
 
    sns_raw_timestamp = event['Records'][0]['Sns']['Timestamp']
   
    sns_nice_timestamp = datetime.strptime(sns_raw_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')   
    sns_time = sns_nice_timestamp.time()
 
    try:
        if "prod" not in sns_subject:
            if sns_time > time(8,00) and sns_time < time(18,00):
                print('In working hours, send an alert!')
                sns = boto3.client('sns')
                sns.publish(TopicArn=sns_alert_topic,Message=sns_message,Subject=sns_subject)
            else:
                print('Out-of-hours, suppress the alert!')
        else:
            print('Prod in the subject - send the alert regardless of time')
            sns = boto3.client('sns')
            sns.publish(TopicArn=sns_alert_topic,Message=sns_message,Subject=sns_subject)
    except Exception as e:
        raise e
