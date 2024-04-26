import boto3

def rename_s3_file(bucket_name, old_key, new_key):
    """
    Rename a file in a specific S3 bucket.

    Args:
    - bucket_name (str): The name of the S3 bucket.
    - old_key (str): The old key (path + filename) of the file to be renamed.
    - new_key (str): The new key (path + filename) of the file after renaming.
    """
    # Create a session with specified AWS credentials
    # session = boto3.Session(
    #     aws_access_key_id='AKIA4MTWKDOG2CK35VIW',
    #     aws_secret_access_key='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',
    #     region_name='eu-north-1'
    # )

    # Create an S3 client using the session
    s3_client = boto3.client('s3')

    try:
        # Copy the file with the new key
        s3_client.copy(
            Bucket=bucket_name,
            CopySource={'Bucket': bucket_name, 'Key': old_key},
            Key=new_key
        )

        # Delete the old file
        s3_client.delete_object(Bucket=bucket_name, Key=old_key)

        print(f"File '{old_key}' renamed to '{new_key}' in bucket '{bucket_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    bucket_name = 'dist-proj-buck-1'
    old_key = 'test/mohamedhesham.jpg'  # Old file path + filename
    new_key = 'test/etsh.jpg'  # New file path + filename
    rename_s3_file(bucket_name, old_key, new_key)
    print(f"File '{old_key}' renamed to '{new_key}' in bucket '{bucket_name}'.")
