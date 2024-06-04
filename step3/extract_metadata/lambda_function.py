import json
import boto3
from PIL import Image
import piexif

s3 = boto3.client('s3')

def rational_to_float(rational):
    return rational[0] / rational[1]

def extract_jpeg_metadata(file_path):
    image = Image.open(file_path)
    exif_data = piexif.load(image.info['exif'])
    metadata = {}

    if piexif.ImageIFD.DateTime in exif_data['0th']:
        datetime_str = exif_data['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
        date, time = datetime_str.split(' ', 1)
        metadata['Date'] = date
        metadata['Time'] = time
    
    if piexif.ImageIFD.HostComputer in exif_data['0th']:
        metadata['HostComputer'] = exif_data['0th'][piexif.ImageIFD.HostComputer].decode('utf-8')
    
    if 'GPS' in exif_data:
        gps_info = exif_data['GPS']
        if piexif.GPSIFD.GPSLatitude in gps_info and piexif.GPSIFD.GPSLatitudeRef in gps_info:
            lat = gps_info[piexif.GPSIFD.GPSLatitude]
            metadata['GpsLatitude'] = round(sum([rational_to_float(val) / 60**i for i, val in enumerate(lat)]), 6)
        
        if piexif.GPSIFD.GPSLongitude in gps_info and piexif.GPSIFD.GPSLongitudeRef in gps_info:
            lon = gps_info[piexif.GPSIFD.GPSLongitude]
            metadata['GpsLongitude'] = round(sum([rational_to_float(val) / 60**i for i, val in enumerate(lon)]), 6)
    
    return metadata

def lambda_handler(event, context):
    read_bucket = '2024-capstone-image-bucket'
    
    write_bucket = '2024-capstone-metadata-bucket'
    
    key = event['Records'][0]['s3']['object']['key']
    download_path = f'/tmp/{key}'
    
    s3.download_file(read_bucket, key, download_path)
    metadata = extract_jpeg_metadata(download_path)
    
    metadata_key = key.replace('.jpg', '_metadata.json')
    metadata_json = json.dumps(metadata)
    
    s3.put_object(Bucket=write_bucket, Key=metadata_key, Body=metadata_json, ContentType='application/json')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Metadata extracted and saved to S3.')
    }
