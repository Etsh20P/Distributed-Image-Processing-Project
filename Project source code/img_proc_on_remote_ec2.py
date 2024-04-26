import cv2
import boto3
import sys
import os

def color_inversion(input_image_path, output_image_path):
    # Read the image
    image = cv2.imread(input_image_path)

    # Perform color inversion
    inverted_image = cv2.bitwise_not(image)

    # Write the inverted image to disk
    cv2.imwrite(output_image_path, inverted_image)

def upload_to_s3(local_file_path, bucket_name, s3_key):
    # Upload the file to S3
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).upload_file(local_file_path, s3_key)

def get_s3_download_link(bucket_name, s3_file_path):
    # Create a presigned URL for the object
    s3 = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'))
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': s3_file_path},
        ExpiresIn=3600,  # Link expiration time (in seconds)
        HttpMethod='GET'
    )
    return url

# Paths
input_image_path = '/home/ubuntu/img2.jpg'
output_image_path = '/home/ubuntu/img6.jpg'
s3_bucket_name = 'dist-proj-buck-1'
s3_key = 'test/another_image6.jpg'

# Perform color inversion
color_inversion(input_image_path, output_image_path)

# Upload the processed image to S3
upload_to_s3(output_image_path, s3_bucket_name, s3_key)

# Get the download link for the processed image
download_link = get_s3_download_link(s3_bucket_name, 'test/another_image6.jpg')

# Print the download link
print("Download link for processed image:", download_link)
