import EC2_API
import S3_API
import time
import boto3
from datetime import datetime, timedelta  # Import datetime module

# not working needs permission to download
# S3_API.S3_download_file('dist-proj-buck-1', 'requested/sudoku.jpg', 'C:/Users/oem/Downloads')

# EC2_API.EC2_run_instance('i-0e38ba40ce0a1523b')

# ssh = EC2_API.initialize_ssh_connection('i-030f706b9e2ae625f')



 
# EC2_API.upload_python_script('D:/Distributed Computing/Project/Project source code/python_script.py', '/home/ubuntu/test3.py')
# EC2_API.execute_python_script('/home/ubuntu/test3.py')
# EC2_API.run_ec2_instance('i-07d897d2eecfda382')
# EC2_API.run_ec2_instance('i-030f706b9e2ae625f')
# ssh = EC2_API.initialize_ssh_connection('i-030f706b9e2ae625f')
# # EC2_API.upload_file('C:/Users/oem/Downloads/processed_image.jpg', '/home/ubuntu/img1.jpg',ssh)
# EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing.py', '/home/ubuntu/img_proc5.py',ssh)
# output = EC2_API.execute_remote_script('/home/ubuntu/img_proc5.py',ssh)
# print(output)


# EC2_API.stop_ec2_instance('i-0d2b2c20a04ea8073')

# EC2_API.assign_iam_role_to_instance('i-0d2b2c20a04ea8073', 'S3-Access')


# EC2_API.run_ec2_instance('i-030f706b9e2ae625f')


# install_command = 'sudo pip3 install sys'
# stdin, stdout, stderr = ssh.exec_command(install_command)
# print(stderr.read().decode('utf-8'))

# EC2_API.upload_file('C:/Users/oem/Downloads/sudoku.jpg', '/home/ubuntu/image_sud.jpg',ssh)

# ssh = EC2_API.initialize_ssh_connection('i-030f706b9e2ae625f')

# EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing.py', '/home/ubuntu/image_processing_script.py',ssh)

# output = EC2_API.execute_remote_script_with_args('/home/ubuntu/image_processing_script.py', ssh, '/home/ubuntu/image_sud.jpg', 'blur', 'image_proc_blured.jpg' )

# print(output)


# EC2_API.stop_ec2_instance('i-030f706b9e2ae625f')


# ssh = EC2_API.initialize_ssh_connection('i-0929e679594ee795a')
# EC2_API.execute_ssh_commands(ssh)

# ssh1 = EC2_API.initialize_ssh_connection('i-030f706b9e2ae625f')
# install_command = 'sudo pip3 install flask'
# stdin, stdout, stderr = ssh.exec_command(install_command)

# EC2_API.run_ec2_instance('i-030f706b9e2ae625f')
# EC2_API.run_ec2_instance('i-0929e679594ee795a')

# ssh = EC2_API.initialize_ssh_connection('i-030f706b9e2ae625f')
# EC2_API.execute_ssh_commands(ssh)
# ssh1 = EC2_API.initialize_ssh_connection('i-0929e679594ee795a')
# EC2_API.execute_ssh_commands(ssh1)
# install_command = 'sudo pip3 install flask'
# stdin, stdout, stderr = ssh1.exec_command(install_command)
# stdin, stdout, stderr = ssh1.exec_command(install_command)

# EC2_API.upload_file('image_processing_flask.py','/home/ubuntu/image_processing_flask1.py',ssh1)
# EC2_API.upload_file('flask_app.py','/home/ubuntu/flask_app1.py',ssh1)

# EC2_API.execute_remote_script('/home/ubuntu/image_processing_flask1.py',ssh1)
# EC2_API.execute_remote_script('/home/ubuntu/flask_app1.py',ssh1)
# EC2_API.upload_file('/home/ubuntu/health.html',ssh1)

# ssh1 = EC2_API.initialize_ssh_connection('i-02963630086cecad9')


# EC2_API.add_instance_to_target_group('i-02963630086cecad9', 'arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62')
# EC2_API.add_instance_to_target_group('i-08b55b11cd902449b', 'arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62')
# EC2_API.execute_ssh_commands(ssh1)

# EC2_API.assign_iam_role_to_instance('i-08b55b11cd902449b', 'S3-Access')
# EC2_API.assign_iam_role_to_instance('i-02963630086cecad9', 'S3-Access')


### ssh = EC2_API.initialize_ssh_connection('i-08b55b11cd902449b')
### EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing_flask.py', '/home/ubuntu/image_processing_script2.py', ssh)
### EC2_API.execute_remote_script('/home/ubuntu/image_processing_script2.py', ssh)

# ssh1 = EC2_API.initialize_ssh_connection('i-02963630086cecad9')
# EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing_flask.py', '/home/ubuntu/image_processing_script2.py', ssh1)
# EC2_API.execute_remote_script('/home/ubuntu/image_processing_script2.py', ssh1)
# while True:
    # if requests > 4:
    #     for i in range(request/2):
    #         id = EC2_API.create_ec2_instance()
    #         EC2_API.initialize_ssh_connection()
    #         EC2_API.execute_ssh_commands()
    #         add_instance_to_target_group(id)

    # elif get_healthy_instances < 2:
    #     for i in range(2-get_healthy_instances):
    #         EC2_API.create_ec2_instance()
    #         EC2_API.initialize_ssh_connection()
    #         EC2_API.execute_ssh_commands()



# Initialize AWS clients
ec2_client = boto3.client('ec2')
elbv2_client = boto3.client('elbv2')

# Define scaling parameters
MAX_REQUESTS_BEFORE_SCALING = 100
DESIRED_INSTANCE_COUNT = 3



def get_request_count(load_balancer_name):
    # Initialize the CloudWatch client
    cloudwatch_client = boto3.client('cloudwatch')

    # Define the metric dimensions
    dimensions = [
        {
            'Name': 'LoadBalancer',
            'Value': load_balancer_name
        }
    ]

    # Get the request count metric
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/ApplicationELB',
        MetricName='RequestCount',
        Dimensions=dimensions,
        StartTime=datetime.utcnow() - timedelta(minutes=5),  # Adjust the time window as needed
        EndTime=datetime.utcnow(),
        Period=300,  # 5-minute period (300 seconds)
        Statistics=['Sum']
    )

    # Extract the request count from the response
    if 'Datapoints' in response and len(response['Datapoints']) > 0:
        request_count = response['Datapoints'][-1]['Sum']
    else:
        request_count = 0

    return request_count



def get_instances_health(target_group_arn):
    # Initialize the ELBv2 client
    elbv2_client = boto3.client('elbv2')

    # Get target health descriptions for the specified target group
    response = elbv2_client.describe_target_health(TargetGroupArn=target_group_arn)

    # Extract instance IDs and health statuses from the response
    instances_health = {}
    for target_health in response['TargetHealthDescriptions']:
        instance_id = target_health['Target']['Id']
        health_status = target_health['TargetHealth']['State']
        instances_health[instance_id] = health_status

    return instances_health


def get_number_of_instances_in_target_group(target_group_arn):
    # Initialize the ELBv2 client
    elbv2_client = boto3.client('elbv2')

    try:
        # Describe target health to get information about targets in the target group
        response = elbv2_client.describe_target_health(TargetGroupArn=target_group_arn)
        
        # Count the number of instances in the target group
        instance_count = len(response['TargetHealthDescriptions'])
        
        return instance_count
    except Exception as e:
        print(f"Error: {e}")
        return None


########### EC2_API.create_ec2_instance()
def create_instance():
    # Placeholder function to create a new EC2 instance
    # In a real-world scenario, you would create an EC2 instance using boto3 or AWS SDK
    print("Creating a new EC2 instance...")
    # Code to create a new EC2 instance
    # Example: response = ec2_client.run_instances(ImageId='ami-12345678', MinCount=1, MaxCount=1)
    # Extract instance ID from response and return it
    return 'NEW_INSTANCE_ID'


########### EC2_API.add_instance_to_target_group()
def add_instance_to_target_group(instance_id, target_group_arn):
    # Placeholder function to add an EC2 instance to the target group
    # In a real-world scenario, you would use boto3 or AWS SDK to register the instance with the target group
    print(f"Adding instance {instance_id} to the target group...")
    # Code to add instance to target group
    # Example: elbv2_client.register_targets(TargetGroupArn=target_group_arn, Targets=[{'Id': instance_id}])

########### EC2_API.execute_ssh_commands()
def install_dependencies(instance_id):
    # Placeholder function to install dependencies on the newly created instance
    print(f"Installing dependencies on instance {instance_id}...")
    # Code to install dependencies
    # Example: Use SSH to connect to the instance and execute commands to install dependencies


########### EC2_API.upload_file()
########### EC2_API.execute_remote_script()
def upload_and_execute_flask_file(instance_id):
    # Placeholder function to upload and execute the Flask file on the instance
    print(f"Uploading and executing Flask file on instance {instance_id}...")
    # Code to upload and execute Flask file
    # Example: Use SSH to transfer files to the instance and execute them


def count_healthy_instances(instance_status_dict):
    # Initialize count
    healthy_count = 0
    
    # Iterate over dictionary values
    for status in instance_status_dict.values():
        # Check if status is 'healthy'
        if status == 'healthy':
            healthy_count += 1
    
    return healthy_count


def main():


    new_instance_id = EC2_API.create_ec2_instance('Project4')  # Create new instances
    EC2_API.assign_iam_role_to_instance(new_instance_id, 'S3-Access')
    ssh = EC2_API.initialize_ssh_connection(new_instance_id)
    EC2_API.execute_ssh_commands(ssh)
    EC2_API.add_instance_to_target_group(new_instance_id, 'arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62')
    EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing_flask.py', '/home/ubuntu/image_processing_script33.py', ssh)
    EC2_API.execute_remote_script('/home/ubuntu/image_processing_script33.py', ssh)
    
    


    # EC2_API.create_ec2_instance('Project')

    # ssh = EC2_API.initialize_ssh_connection('i-02963630086cecad9')
    # EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing_flask.py', '/home/ubuntu/image_processing_script32.py', ssh)
    # EC2_API.execute_remote_script('/home/ubuntu/image_processing_script32.py', ssh)
    # print(get_instances_health('arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62'))
    # print(get_number_of_instances_in_target_group('arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62'))



    # while True:
        # Get monitoring metrics
        # request_count = get_request_count()
        # healthy_instances = get_instances_health('arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62')
        # existing_instances = get_number_of_instances_in_target_group('arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62')

        # # Check if scaling up is needed based on request count
        # # if request_count > MAX_REQUESTS_BEFORE_SCALING:
        # #     instances_needed = max(0, DESIRED_INSTANCE_COUNT - existing_instances)
        # #     for _ in range(instances_needed):
        # #         new_instance_id = create_instance()  # Create new instances
        # #         install_dependencies(new_instance_id)  # Install dependencies
        # #         upload_and_execute_flask_file(new_instance_id)  # Upload and execute Flask file
        # #         # Add new instances to the target group
        # #         add_instance_to_target_group(new_instance_id, 'YOUR_TARGET_GROUP_ARN')

        # # Check if scaling up is needed based on healthy instance count

        # healthy_instances_count = count_healthy_instances(healthy_instances)
        # print(healthy_instances_count)

        # # existing_instances
        # if healthy_instances_count < existing_instances:

        #     instances_needed = max(0, existing_instances - healthy_instances_count)
        #     print(instances_needed)
        #     for _ in range(instances_needed):
                
        #         new_instance_id = EC2_API.create_ec2_instance('Project')  # Create new instances
        #         EC2_API.assign_iam_role_to_instance(new_instance_id, 'S3-Access')
        #         EC2_API.add_instance_to_target_group(new_instance_id, 'arn:aws:elasticloadbalancing:eu-north-1:851725392781:targetgroup/test-img-proc-TG/cdfc847103e4fb62')
        #         # install_dependencies(new_instance_id)  # Install dependencies
        #         # upload_and_execute_flask_file(new_instance_id)  # Upload and execute Flask file
        #         # # Add new instances to the target group
        #         # add_instance_to_target_group(new_instance_id, 'YOUR_TARGET_GROUP_ARN')

        # time.sleep(60)  # Adjust the sleep duration as needed



if __name__ == "__main__":
    main()
