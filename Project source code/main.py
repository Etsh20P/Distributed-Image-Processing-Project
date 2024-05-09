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


ssh = EC2_API.initialize_ssh_connection('i-08b55b11cd902449b')
EC2_API.upload_file('D:/Distributed Computing/Project/Project source code/image_processing_flask.py', '/home/ubuntu/image_processing_script2.py', ssh)
EC2_API.execute_remote_script('/home/ubuntu/image_processing_script2.py', ssh)

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

