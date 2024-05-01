from flask import Flask, request, jsonify
import cv2
import boto3
import numpy as np
import os


app = Flask(__name__)


@app.route('/health')
def health_check():
    # Perform any necessary health checks here
    # Return a successful response if the application is healthy
    return 'OK', 200


@app.route('/process_image', methods=['POST'])
def process_image():
    # Check if the request contains a file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    # Get the image file from the request
    image_file = request.files['image']

    # Read the image file using OpenCV
    image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Get other request parameters
    operation = request.form['operation']
    output_image_name = request.form['output_name']
    s3_bucket_name = request.form['s3_bucket']

    # Perform image processing
    output_image_path = f'/home/ubuntu/{output_image_name}'
    image_processing(image, output_image_path, operation)

    # Upload processed image to S3
    s3_key = f'test/{output_image_name}'
    upload_to_s3(output_image_path, s3_bucket_name, s3_key)

    # Get download link for processed image
    download_link = get_s3_download_link(s3_bucket_name, s3_key)

    
    return jsonify({'download_link': download_link, 'Instance_ID': instance_id})

def image_processing(image, output_image_path, operation):
    # Perform the specified operation
    if operation == 'color_inversion':
        processed_image = cv2.bitwise_not(image)
    elif operation == 'grayscale':
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif operation == 'blur':
        processed_image = cv2.GaussianBlur(image, (15, 15), 0)
    elif operation == 'edge_detection':
        processed_image = cv2.Canny(image, 100, 200)  # Perform edge detection
    elif operation == 'thresholding':
        _, processed_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    else:
        raise ValueError("Invalid operation specified.")

    # Write the processed image to disk
    cv2.imwrite(output_image_path, processed_image)

def upload_to_s3(local_file_path, bucket_name, s3_key):
    # Upload the file to S3
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).upload_file(local_file_path, s3_key)

def get_s3_download_link(bucket_name, s3_file_path):
    return f'https://{bucket_name}.s3.amazonaws.com/{s3_file_path}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
