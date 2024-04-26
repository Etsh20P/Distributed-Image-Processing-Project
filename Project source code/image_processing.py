import cv2
import boto3
import sys
import os


def image_processing(input_image_path, output_image_path, operation):
    # Read the image
    image = cv2.imread(input_image_path)

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
        print("Invalid operation specified.")
        return

    # Write the processed image to disk
    cv2.imwrite(output_image_path, processed_image)





def upload_to_s3(local_file_path, bucket_name, s3_key):
    # Upload the file to S3
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).upload_file(local_file_path, s3_key)




def get_s3_download_link(bucket_name, s3_file_path):

    url = f'https://{bucket_name}.s3.amazonaws.com/{s3_file_path}' 


    return url


if __name__ == "__main__":
    # Check if correct number of arguments provided
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_image_path> <operation> <output_image_name>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    operation = sys.argv[2]
    output_image_name = sys.argv[3]

    # Determine the output image path
    output_image_path = f'/home/ubuntu/{output_image_name}'

    # Perform image processing
    image_processing(input_image_path, output_image_path, operation)

    # Upload the processed image to S3
    s3_bucket_name = 'dist-proj-buck-1'
    s3_key = f'test/{output_image_name}'
    upload_to_s3(output_image_path, s3_bucket_name, s3_key)

    # Get the download link for the processed image
    download_link = get_s3_download_link(s3_bucket_name, s3_key)

    # Print the download link
    print("Download link for processed image:", download_link)
