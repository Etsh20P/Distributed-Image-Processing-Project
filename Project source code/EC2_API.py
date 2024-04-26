import boto3
import paramiko


ssh = None
username = 'ubuntu'  
# Frankfurt -> "D:/Distributed Computing/Project/AWS key/Project-Frankfurt.pem"
private_key_path = "D:/Distributed Computing/Project/AWS key/Project-Test-01.pem"  # stockholm -> D:/Distributed Computing/Project/AWS key/Project-Test-01.pem
public_ip = None  # Define a global variable for storing public DNS

 # Create EC2 client  Frankfurt -> region_name='eu-central-1
ec2 = boto3.resource('ec2', region_name='eu-north-1') # stockholm



def initialize_ssh_connection(instance_id):

    instance = ec2.Instance(instance_id)

    public_ip = instance.public_ip_address

    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
    ssh.connect(hostname=public_ip, username=username, pkey=private_key)

    return ssh
    



def execute_ssh_commands(ssh_connection):

    # Commands to install Python and required libraries
    # 'sudo apt install -y python3-pyopencl',
    # 'sudo apt install -y python3-mpi4py',
    install_commands = [
        'sudo apt update',
        'sudo apt install -y python3 python3-pip python3-dev',
        'sudo apt install -y python3-opencv',
        'sudo apt install -y python3-boto3'
    ]

    # Execute commands
    for command in install_commands:
        print(f"Executing: {command}")
        stdin, stdout, stderr = ssh_connection.exec_command(command)

        # # Print command output
        # print(stdout.read().decode())

        # Print any errors
        print(stderr.read().decode('utf-8'))



def upload_file(local_file_path, remote_file_path, ssh_connection):
    """
    Uploads a file from the local machine to the specified path on the remote machine using SSH.

    Args:
    - local_file_path (str): Path to the local file to be uploaded.
    - remote_file_path (str): Path on the remote machine where the file will be uploaded.
    - ssh_connection (paramiko.SSHClient): Paramiko SSHClient instance representing the SSH connection.

    Returns:
    - bool: True if the upload was successful, False otherwise.
    """

    try:
        # Open an SFTP session
        sftp = ssh_connection.open_sftp()

        # Upload the file
        sftp.put(local_file_path, remote_file_path)

        # Close the SFTP session
        sftp.close()

        print(f"File '{local_file_path}' uploaded to '{remote_file_path}' successfully.")
        return True
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False



def execute_remote_script_with_args(remote_script_path, ssh_connection, image_path, operation, image_output_name):
    """
    Executes a Python script on the remote machine using SSH.

    Args:
    - remote_script_path (str): Path to the Python script on the remote machine.
    - ssh_connection (paramiko.SSHClient): Paramiko SSHClient instance representing the SSH connection.

    Returns:
    - str: Output of the executed command.
    """

    try:
        # Make the script executable
        ssh_connection.exec_command(f"chmod +x {remote_script_path}")

        # Execute the Python script
        stdin, stdout, stderr = ssh_connection.exec_command(f"python3 {remote_script_path} {image_path} {operation} {image_output_name}")
        
        # Read the output
        output = stdout.read().decode('utf-8')

        # Check for errors
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error executing script: {error}")
        
        return output
    
    except Exception as e:
        print(f"Error executing script: {str(e)}")
        return None
    





def execute_remote_script(remote_script_path, ssh_connection):
    """
    Executes a Python script on the remote machine using SSH.

    Args:
    - remote_script_path (str): Path to the Python script on the remote machine.
    - ssh_connection (paramiko.SSHClient): Paramiko SSHClient instance representing the SSH connection.

    Returns:
    - str: Output of the executed command.
    """

    try:
        # Make the script executable
        ssh_connection.exec_command(f"chmod +x {remote_script_path}")

        # Execute the Python script
        stdin, stdout, stderr = ssh_connection.exec_command(f"python3 {remote_script_path}")
        
        # Read the output
        output = stdout.read().decode('utf-8')

        # Check for errors
        error = stderr.read().decode('utf-8')
        if error:
            print(f"Error executing script: {error}")
        
        return output
    

    except Exception as e:
        print(f"Error executing script: {str(e)}")
        return None


def create_ec2_instance(instance_name):

    # Key pair name for (Frankfurt) -> Project-Frankfurt
    key_pair_name = "Project-Test-01" # stockholm

    # AMI ID for Ubuntu (Frankfurt)-> ami-023adaba598e661ac
    ubuntu_ami_id = 'ami-0914547665e6a707c' # stockholm


    # Security group id for Frankfurt -> sg-0734464f28a13491f
    security_group_id = "sg-05fb1384edf49343b" # stockholm

    # Instance type Frankfurt -> t2.micro
    instance_type = "t3.micro" # stockholm

    # Tag Specifications
    tags = [
        {
            'Key': 'Name',
            'Value': instance_name
        }
    ]

    # Create EC2 instance
    instance = ec2.create_instances(
        ImageId=ubuntu_ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=key_pair_name,
        SecurityGroupIds=[security_group_id],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': tags
            }
        ]
    )

    return instance[0].id  # Return the instance ID


def terminate_ec2_instance(instance_id):
    
    try:
        instance = ec2.Instance(instance_id)
        instance.terminate()
        print(f"Instance {instance_id} terminated successfully.")
    except Exception as e:
        print(f"Error terminating instance {instance_id}: {str(e)}")

def stop_ec2_instance(instance_id):
    
    try:
        instance = ec2.Instance(instance_id)
        instance.stop()
        print(f"Instance {instance_id} stopped successfully.")
    except Exception as e:
        print(f"Error stopping instance {instance_id}: {str(e)}")

def run_ec2_instance(instance_id):
    
    try:
        instance = ec2.Instance(instance_id)
        instance.start()
        print(f"Instance {instance_id} started successfully.")
    except Exception as e:
        print(f"Error starting instance {instance_id}: {str(e)}")





def assign_iam_role_to_instance(instance_id, iam_role_name):
    """
    Assigns an IAM role to an EC2 instance.

    Args:
    - instance_id (str): The ID of the EC2 instance.
    - iam_role_name (str): The name of the IAM role to be assigned.

    Returns:
    - bool: True if the operation was successful, False otherwise.
    """

    try:
        # Create EC2 client  Frankfurt -> region_name='eu-central-1
        ec2_client = boto3.client('ec2', region_name='eu-north-1') # stockholm

        # Associate IAM role with instance
        response = ec2_client.associate_iam_instance_profile(
            IamInstanceProfile={
                'Name': iam_role_name
            },
            InstanceId=instance_id
        )

        print(f"IAM role '{iam_role_name}' successfully assigned to instance '{instance_id}'.")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


# Example usage:
# Replace 'your_instance_id_here' and 'your_iam_role_name_here' with actual values
# assign_iam_role_to_instance('your_instance_id_here', 'your_iam_role_name_here')














# def create_ec2_instance(name):
#     # Set the parameters
#     instance_name = name
#     image_id = 'ami-0914547665e6a707c'  # Ubuntu 18.04 LTS in eu-north-1
#     instance_type = 't3.micro'
#     key_name = 'Project-Test-01'
#     security_group_name = 'Project-Test-SG'
#     security_group_description = 'Security group for Project-Test-1'
#     ssh_source_ip = '0.0.0.0/0'  # Assuming you want to allow SSH from any IP
    
#     # Connect to EC2
#     ec2_client = boto3.client('ec2', region_name='eu-north-1')
    
#     # Create a new security group
#     response = ec2_client.create_security_group(
#         GroupName=security_group_name,
#         Description=security_group_description
#     )
#     security_group_id = response['GroupId']
    
#     # Add SSH inbound rule to the security group
#     ec2_client.authorize_security_group_ingress(
#         GroupId=security_group_id,
#         IpProtocol='tcp',
#         FromPort=22,
#         ToPort=22,
#         CidrIp=ssh_source_ip
#     )
    
#     # Get the IAM role ARN
#     iam_role_arn = 'arn:aws:iam::851725392781:role/S3-Access'  # Provide the IAM role ARN
    
#     # Launch an EC2 instance
#     response = ec2_client.run_instances(
#         ImageId=image_id,
#         InstanceType=instance_type,
#         KeyName=key_name,
#         SecurityGroupIds=[security_group_id],
#         IamInstanceProfile={'Arn': iam_role_arn},
#         MinCount=1,
#         MaxCount=1,
#         TagSpecifications=[
#             {
#                 'ResourceType': 'instance',
#                 'Tags': [
#                     {'Key': 'Name', 'Value': instance_name}
#                 ]
#             }
#         ]
#     )
    
#     # Extract the instance ID
#     instance_id = response['Instances'][0]['InstanceId']
#     print(f"Instance {instance_id} created successfully.")




































# # Global variables for SSH connection
# ssh_client = None
# username = 'ubuntu'  
# private_key_path = "D:/Distributed Computing/Project/AWS key/Project-Test-01.pem"  
# public_ip = None  # Define a global variable for storing public DNS



# # Specify the bash script to run on the EC2 instance to setup and install python and some needed libraries
# bash_script = """#!/bin/bash
# apt update
# apt install -y python3 python3-pip
# pip3 install opencv-python-headless boto3
# apt install -y python3-pyopencl python3-mpi4py mpich
# """

# # bsh_script = """#!/bin/bash
# # apt update
# # apt install -y python3 python3-pip
# # pip3 install boto3
# # """

# # Create EC2 resource
# ec2_resource = boto3.resource('ec2')



# def initialize_ssh_connection(instance_id):

#     instance = ec2_resource.Instance(instance_id)

#     global ssh_client, public_ip
#     # Connect to the EC2 instance via SSH
#     ssh_client = paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#     # Load private key
#     private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

#     # Connect to the instance
#     public_ip = instance.public_ip_address
#     ssh_client.connect(hostname=public_ip, username=username, pkey=private_key)


# def upload_python_script(local_script_path, remote_script_path):
#     # Upload the Python file to the EC2 instance
#     sftp_client = ssh_client.open_sftp()
#     sftp_client.put(local_script_path, remote_script_path)
#     sftp_client.close()



# def execute_python_script(remote_script_path):

#     # Execute the Python script on the EC2 instance
#     stdin, stdout, stderr = ssh_client.exec_command(f'python3 {remote_script_path}')
#     for line in stdout:
#         print(line.strip())




# def EC2_create_instance(name):

#     # Specify the parameters for launching the instance
#     ami_id = 'ami-0914547665e6a707c'
#     instance_type = 't3.micro'
#     key_pair_name = 'Project-Test-01'
#     instance_name = name

#     # Launch a new EC2 instance
#     instance = ec2_resource.create_instances(
#         ImageId=ami_id,
#         InstanceType=instance_type,
#         KeyName=key_pair_name,
#         MinCount=1,
#         MaxCount=1,
#         TagSpecifications=[
#             {
#                 'ResourceType': 'instance',
#                 'Tags': [
#                     {'Key': 'Name', 'Value': instance_name}
#                 ]
#             }
#         ]
#     )[0]  # Get the first instance from the list of created instances

#     print(f'EC2 instance {instance.id} ({instance_name}) has been created.')

#     return instance.id


# def EC2_delete_instance(Ec2ID):

#     # Specify the instance ID to delete
#     instance_id = Ec2ID

#     # Get the instance object
#     instance = ec2_resource.Instance(instance_id)

#     # Terminate the instance
#     response = instance.terminate()

#     print(f'Instance {instance_id} has been terminated.')


# def EC2_run_instance(Ec2ID):

#     # Specify the instance ID of the instance to start
#     instance_id = Ec2ID

#     # Get the instance object
#     instance = ec2_resource.Instance(instance_id)

#     # Start the instance
#     response = instance.start()

#     print(f'Instance {instance_id} has been started.')


# def EC2_stop_instance(Ec2ID):

#     # Get the instance object
#     instance = ec2_resource.Instance(Ec2ID)

#     # Stop the instance
#     instance.stop()

#     print(f'Instance {Ec2ID} has been stopped.')



# def EC2_install_py_on_machine(Ec2ID):

#     # Read the contents of the bash script file
#     with open("bash_script.sh", "r") as file:
#         bash_script = file.read()
    
#     # Execute the bash script
#     stdin, stdout, stderr = ssh_client.exec_command(bash_script)
#     for line in stdout:
#         print(line.strip())

#     # Close the SSH connection
#     ssh_client.close()

#     print('Bash script executed successfully on the EC2 instance.')




