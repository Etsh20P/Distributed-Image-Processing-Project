import EC2_API
import S3_API
import time
import boto3
import threading
from datetime import datetime, timedelta  # Import datetime module


# Initialize AWS clients
ec2_client = boto3.client('ec2')
elbv2_client = boto3.client('elbv2')

# Define scaling parameters
MAX_REQUESTS_BEFORE_SCALING = 5
MAX_NUMBER_OF_INSTANCES = 8
DESIRED_INSTANCE_COUNT = 2
TARGET_GROUP_ARN ='arn:aws:elasticloadbalancing:eu-central-1:851725392781:targetgroup/Image-Processing-Frank-TG/4594d70e60686eda'
IMAGE_PROCESSING_SCRIPT_PATH = 'D:/Distributed Computing/Project/Project source code/image_processing_flask.py'
REMOTE_SCRIPT_PATH = '/home/ubuntu/image_processing_flask_script.py'

REQUESTS_PER_INSTANCE = 5
request_count = 0






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





def count_healthy_instances(instance_status_dict):
    # Initialize count
    healthy_count = 0
    
    # Iterate over dictionary values
    for status in instance_status_dict.values():
        # Check if status is 'healthy'
        if status == 'healthy':
            healthy_count += 1
    
    return healthy_count




def add_instance_to_target():
    new_instance_id = EC2_API.create_ec2_instance()  # Create new instances
    EC2_API.assign_iam_role_to_instance(new_instance_id, 'S3-Access')
    ssh = EC2_API.initialize_ssh_connection(new_instance_id)
    EC2_API.execute_ssh_commands(ssh)
    # EC2_API.modify_instance_metadata_options(new_instance_id)
    EC2_API.add_instance_to_target_group(new_instance_id, TARGET_GROUP_ARN)
    EC2_API.upload_file(IMAGE_PROCESSING_SCRIPT_PATH, REMOTE_SCRIPT_PATH, ssh)
    EC2_API.execute_remote_script(REMOTE_SCRIPT_PATH, ssh)





def auto_scaling_and_Fault_tolerance():


    while True:
        # Get monitoring metrics

        # request_count = get_request_count()
        healthy_instances = get_instances_health(TARGET_GROUP_ARN)
        existing_instances = get_number_of_instances_in_target_group(TARGET_GROUP_ARN)

        healthy_instances_count = count_healthy_instances(healthy_instances)
        print(f"healthy_instances_count = {healthy_instances_count}")


        ###################################################### scaling ##################################################################
        # calculate the required instances based on request count
        if request_count % 5 == 0:
            Needed_Vms = request_count // REQUESTS_PER_INSTANCE
        
        else:
            Needed_Vms = (request_count // REQUESTS_PER_INSTANCE) +1
        
        desired_instances = Needed_Vms - existing_instances

        # Check if scaling up is needed based on the calculated required instances
        print(f"desired_instances = {desired_instances}, Needed_Vms= {Needed_Vms} , existing_instances= {existing_instances} , request_count= {request_count} ")
        if desired_instances < 0:
            desired_instances = desired_instances * -1

            for i in range(desired_instances):

                if existing_instances <= DESIRED_INSTANCE_COUNT:
                    break
                EC2_API.terminate_ec2_instance(list(healthy_instances.keys())[i])
                existing_instances = existing_instances -1
                
        elif (desired_instances + existing_instances) <= MAX_NUMBER_OF_INSTANCES:
            for _ in range(desired_instances):
                instance_scale_thread = threading.Thread(target=add_instance_to_target)
                instance_scale_thread.start()
        
        

        ####################################################### Fault Tolerance #########################################################

        # Check if scaling up is needed based on healthy instance count
        # existing_instances instead of 2
        if (healthy_instances_count < DESIRED_INSTANCE_COUNT) and (existing_instances < MAX_NUMBER_OF_INSTANCES):

            instances_needed = max(0, DESIRED_INSTANCE_COUNT - healthy_instances_count)
            print(f"instance needed in fault tolerance = {instances_needed}")
            for _ in range(instances_needed):
                instance_fault_thread = threading.Thread(target=add_instance_to_target)
                instance_fault_thread.start()
                
                           
                

        time.sleep(400)  # wait until instances created, add to target group and become healthy



def main():
    global request_count
    
    ## run el awl el 2 vms ely 3ndk w khlehom healthy 
    ## then test Scale_and_fault again
    ## then test the modify IMDSv2 
    ## then test sending requests to the load balancer
    ## try to test the get_req_count
    ## try to link the requests count with the request of the ALB file
    ## link with gui

    ## EC2_API.run_ec2_instance('i-01d25c4b7a43d1a81')
    ## ssh = EC2_API.initialize_ssh_connection('i-01d25c4b7a43d1a81')
    ## EC2_API.execute_remote_script(REMOTE_SCRIPT_PATH,ssh)

    ## EC2_API.run_ec2_instance('i-0a13038954d21710f')
    ## ssh = EC2_API.initialize_ssh_connection('i-0a13038954d21710f')
    ## EC2_API.execute_remote_script(REMOTE_SCRIPT_PATH,ssh)

    # print(get_instances_health(TARGET_GROUP_ARN))

    Scale_and_fault_thread = threading.Thread(target=auto_scaling_and_Fault_tolerance)
    Scale_and_fault_thread.start()

    time.sleep(300)

    request_count = 40

    time.sleep(450)

    request_count = 5
    Scale_and_fault_thread.join()
    
    

if __name__ == "__main__":
    main()
