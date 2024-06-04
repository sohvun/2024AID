import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = '2024-capstone-metadata-bucket'

def load_json_from_s3(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)

def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S')

def lambda_handler(event, context):
    try:
        # Load existing JSON files from S3
        json_keys = [content['Key'] for content in s3.list_objects_v2(Bucket=BUCKET_NAME)['Contents']]
    except KeyError:
        # No objects in the bucket
        json_keys = []
    
    json_data = []
    for key in json_keys:
        if key.endswith('.json'):
            data = load_json_from_s3(BUCKET_NAME, key)
            json_data.append(data)

    for i in range(len(json_data)):
        for j in range(i + 1, len(json_data)):
            data1, data2 = json_data[i], json_data[j]
            
            if ('Date' in data1 and 'Date' in data2 and
                'HostComputer' in data1 and 'HostComputer' in data2 and
                'GpsLatitude' in data1 and 'GpsLatitude' in data2 and
                'GpsLongitude' in data1 and 'GpsLongitude' in data2 and
                data1['Date'] == data2['Date'] and
                data1['HostComputer'] == data2['HostComputer'] and
                round(data1['GpsLatitude'], 3) == round(data2['GpsLatitude'], 3) and
                round(data1['GpsLongitude'], 3) == round(data2['GpsLongitude'], 3)):
                
                time1 = parse_time(data1['Time'])
                time2 = parse_time(data2['Time'])
                time_diff = abs((time2 - time1).total_seconds())
                
                if time_diff >= 60:
                    print("Report log updated: ", {
                        '날짜': data1['Date'],
                        '신고자': data1['HostComputer'],
                        '위치': (round(data1['GpsLatitude'], 3), round(data1['GpsLongitude'], 3)),
                        '최초신고시각': data1['Time']
                    })

    return {
        'statusCode': 200,
        'body': json.dumps('Report log updated.')
    }
