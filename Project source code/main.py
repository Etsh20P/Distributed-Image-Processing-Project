import EC2_API
import S3_API


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

ssh = EC2_API.initialize_ssh_connection('i-030f706b9e2ae625f')
# install_command = 'sudo pip3 install sys'
# stdin, stdout, stderr = ssh.exec_command(install_command)
# print(stderr.read().decode('utf-8'))

# EC2_API.upload_file('C:/Users/oem/Downloads/sudoku.jpg', '/home/ubuntu/image_sud.jpg',ssh)
EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing.py', '/home/ubuntu/image_processing_script.py',ssh)

output = EC2_API.execute_remote_script_with_args('/home/ubuntu/image_processing_script.py', ssh, '/home/ubuntu/image_sud.jpg', 'blur', 'image_proc_blured.jpg' )

print(output)

