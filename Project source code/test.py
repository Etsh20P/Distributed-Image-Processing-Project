from tkinter import PhotoImage, filedialog
import customtkinter
from PIL import Image
import os
from urllib.parse import urlparse
import webbrowser
# from ALB_API import send_image_processing_request
import time
from main_operations import get_unhealthy_instance_ids, add_instance_to_target, count_healthy_instances, get_number_of_instances_in_target_group, get_instances_health
import EC2_API
import ALB_API
import asyncio
import threading


# Define scaling parameters
MAX_REQUESTS_BEFORE_SCALING = 5
MAX_NUMBER_OF_INSTANCES = 8
DESIRED_INSTANCE_COUNT = 2
TARGET_GROUP_ARN ='arn:aws:elasticloadbalancing:eu-central-1:851725392781:targetgroup/Image-Processing-Frank-TG/4594d70e60686eda'
IMAGE_PROCESSING_SCRIPT_PATH = 'D:/Distributed Computing/Project/Project source code/image_processing_flask.py'
REMOTE_SCRIPT_PATH = '/home/ubuntu/image_processing_flask_script.py'

REQUESTS_PER_INSTANCE = 3
request_count = 0





customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk() 
app.title('Image Pro')
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}")
upload_icon = customtkinter.CTkImage(Image.open('GUI test/upload.png'), size=(35,35))
app_image = customtkinter.CTkImage(Image.open('GUI test/setting_1.png'), size=(70,70))
app_image_label = customtkinter.CTkLabel(master=app,image=app_image, text='')
app_image_label.place(x=80,y=10)
my_font = customtkinter.CTkFont(family='Helvetica',size=16, weight="bold")
imagePro_label = customtkinter.CTkLabel(master=app, text='Image Pro', font=my_font)
imagePro_label.place(x=160,y=40)


ALB_operations = {'Color Inversion':'color_inversion','Grayscale':'grayscale', 'Blur':'blur','Edge Detection':'edge_detection', 'Thresholding':'thresholding','Line Detection':'line_detection', 'Frame Contour Detection':'frame_contour_detection', 'Morphological operations':'morphological_operations'}
filenames=()
recent_images = {}
####################### RIGHT FRAME #########################
def upload_images():
    global filenames
    filenames = filedialog.askopenfilenames(multiple=True)
    if len(filenames) == 1:
        display_single_image(filenames[0])
        uplaod_frame.pack(expand=True)
        upload_btn.pack_forget()
        inner_frame2.pack_forget()
        inner_frame2.pack(expand=True)
    elif len(filenames) > 1:
        display_multiple_images(filenames)
        uplaod_frame.pack(expand=True)
        upload_btn.pack_forget()
        inner_frame2.pack_forget()
        inner_frame2.pack(expand=True)
        remaining_label.pack()


def display_single_image(filename):
  # Load the image and resize if needed
  image = customtkinter.CTkImage(Image.open(filename), size=(230,230))
  # Display image in the frame
  upload_label.configure(image=image,text='')
  upload_label.image = image  # Keep a reference to avoid garbage collection

def display_multiple_images(filenames):
  # Display first image and indicate remaining count
    image = customtkinter.CTkImage(Image.open(filenames[0]), size=(230,230)) 

    upload_label.configure(image=image,text='')
    upload_label.image = image
    remaining_count = len(filenames) - 1
    remaining_label.configure(text=f"+{remaining_count}",font=remaining_label_font)

def show_popup(message):
  # Create a popup window
  popup = customtkinter.CTkToplevel()
  popup.title("This is a Pop-up Window")
  popup.geometry("300x150")  # Set size

  # Label within the popup
  label = customtkinter.CTkLabel(popup, text=message)
  label.pack()

  # Button to close the popup
  close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
  close_button.pack()

async def Apply_operation(filenames,operation):
    
    global request_count
    
    if filenames == 0:
      show_popup('Please choose an image to upload.')
      return
    
    elif operation == '':
      show_popup("Please choose an operation.")
      return
    
    s3_bucket='dist-frank-proj'

    for file in filenames:
        image_url = urlparse(file)                   
        image_name = operation + '_' + os.path.basename(image_url.path)  
        download_link , instance_id = await ALB_API.send_image_processing_request(file, ALB_operations[operation], image_name, s3_bucket)
        recent_images[image_name]= download_link
        add_recent_images(image_name.split('_')[1], operation, download_link)
        request_count +=1
    
    print(request_count)
    filenames=()
    

    uplaod_frame.pack_forget()
    inner_frame2.pack_forget()
    upload_btn.pack(expand=True)
    inner_frame2.pack(expand=True)


frame1 = customtkinter.CTkFrame(master=app ,width=300,height=600,border_width=1,corner_radius=15,fg_color='#f2f2f2')
frame1.pack(side='right',padx=40)
frame1.pack_propagate(False)
upload_btn = customtkinter.CTkButton(master = frame1,text='Upload Image',image=upload_icon,compound='top' ,text_color='black' ,width=250, height=250,fg_color='#76BADC', corner_radius=15, command=upload_images)
uplaod_frame = customtkinter.CTkFrame(master = frame1, width=250, height=260,fg_color='#76BADC',corner_radius=15)
uplaod_frame.pack_propagate(False)
upload_label = customtkinter.CTkLabel(master=uplaod_frame,text='')
upload_label.pack(pady=10)
remaining_label = customtkinter.CTkLabel(master=uplaod_frame,text='')
remaining_label_font= customtkinter.CTkFont(family='Helvetica', weight='bold',size=14)
# remaining_label.pack()
inner_frame2 = customtkinter.CTkFrame(master = frame1, width=250, height=150,fg_color='#76BADC',corner_radius=15)

# **Centering the inner frames:**
# Use `pack` with `expand=True` for both frames
upload_btn.pack(expand=True)
inner_frame2.pack(expand=True)
inner_frame2.pack_propagate(False)

operation_label = customtkinter.CTkLabel(master=inner_frame2, text='Choose Operation')
operation_label.pack(anchor='nw',padx=5, pady=5)
operation_values = ['Color Inversion','Grayscale', 'Blur','Edge Detection', 'Thresholding','Line Detection', 'Frame Contour Detection', 'Morphological operations']
operations = customtkinter.CTkComboBox(master =inner_frame2, width = 200, height=35, values=operation_values,corner_radius=15, state='readonly' )
operations.pack(expand = True)
# inversion_button = customtkinter.CTkButton(master=inner_frame2,text='Color Inversion',width=200,height=35,corner_radius=20,fg_color='#134C9F')
# inversion_button.pack(expand=True)

# operatin2_button = customtkinter.CTkButton(master=inner_frame2,text='Operation 2',width=200,height=35,corner_radius=20,fg_color='#134C9F')
# operatin3_button = customtkinter.CTkButton(master=inner_frame2,text='Operation 3',width=200,height=35,corner_radius=20,fg_color='#134C9F')
# operatin4_button = customtkinter.CTkButton(master=inner_frame2,text='Operation 4',width=200,height=35,corner_radius=20,fg_color='#134C9F')
Apply_button = customtkinter.CTkButton(master=inner_frame2,text='Apply',width=200,height=35,corner_radius=20,fg_color='#2E3031', command=lambda: asyncio.run(Apply_operation(filenames, operations.get())))
# operatin2_button.pack(expand=True)
# operatin3_button.pack(expand=True)
# operatin4_button.pack(expand=True)
Apply_button.pack(expand=True)

# frame2 = customtkinter.CTkFrame(master=app ,width=900,height=600,border_width=1,corner_radius=15)
# frame2.pack(side='left', padx=100)
# frame2.pack_propagate(False)

############################ END OF RIGHT FRAME ##################################



########################## FRAME THAT HOLDS THE MACHINES STATUES ###########################
machines_frame = customtkinter.CTkScrollableFrame(master=app ,width=630,height=175,fg_color="#f2f2f2",border_width=1,corner_radius=15,orientation='horizontal')
machines_frame.place(x=245, y=100)




# cloud_icon1 = customtkinter.CTkImage(Image.open('cloud-server.png'), size=(100,100))
# cloud_label1 = customtkinter.CTkLabel(master=frame_state1,image=cloud_icon1, text='')
# cloud_label1.pack()
# state_label1 = customtkinter.CTkLabel(master=frame_state1, text='VM Name\nHealth: Status')
# state_label1.pack()

# cloud_label2 = customtkinter.CTkLabel(master=frame_state1,image=cloud_icon1, text='')
# cloud_label2.pack()
# state_label2 = customtkinter.CTkLabel(master=frame_state1, text='VM Name\nHealth: Status')
# state_label2.pack()

# cloud_label3 = customtkinter.CTkLabel(master=frame_state1,image=cloud_icon1, text='')
# cloud_label3.pack()
# state_label3 = customtkinter.CTkLabel(master=frame_state1, text='VM Name\nHealth: Status')
# state_label3.pack()

########################## END OF FRAME THAT HOLDS THE MACHINES STATUES ###########################



######################### PROGRESS BAR ##############################
progress_bar = customtkinter.CTkProgressBar(master=app, width=650, height=10)
progress_label = customtkinter.CTkLabel(master=app,text="Progress 40%")
progress_bar.place(x=250,y=350)
progress_label.place(x=270,y=320)
inversion_progress = customtkinter.CTkLabel(master=app, text="Finished color inversion...")
inversion_progress.place(x=730,y=320)

my_font2 = customtkinter.CTkFont(family='Helvetica',size=18, weight="bold")
receent_label = customtkinter.CTkLabel(master=app, text="Recent Images",font=my_font2)
receent_label.place(x=250,y=380)
######################### END OF PROGRESS BAR ##############################



######################## FRAME THAT HOLDS THE RECENT IMAGES ##########################
recent_frame= customtkinter.CTkScrollableFrame(master=app, width=630,height=200,border_width=1,corner_radius=15, fg_color='#f2f2f2')
recent_frame.place(x=245,y=420)

gallery_image = customtkinter.CTkImage(Image.open('GUI test/image-gallery.png'), size=(32,32))
download_image = customtkinter.CTkImage(Image.open('GUI test/downloading.png'), size=(32,32))

def add_recent_images(image_name, operation, download_link):
  download_frame= customtkinter.CTkFrame(master=recent_frame ,width=590,height=50,corner_radius=15,border_width=1,fg_color='#f2f2f2')
  download_frame.pack(expand=True,pady=10)
  gallery_label = customtkinter.CTkLabel(master=download_frame,image=gallery_image, text="")
  gallery_label.place(x=7,y=7)
  imagenumber_label = customtkinter.CTkLabel(master=download_frame, text=image_name)
  imagenumber_label.place(x=50,y=10)
  operation_done_label = customtkinter.CTkLabel(master=download_frame, text=operation)
  operation_done_label.place(x=250,y=10)
  download_button = customtkinter.CTkButton(master = download_frame,text='',image=download_image,width=5,height=32,fg_color='#f2f2f2',border_spacing=0,hover=False , command=lambda: webbrowser.open(download_link))
  download_button.place(x= 530, y = 7)
######################## END OF FRAME THAT HOLDS THE RECENT IMAGES ##########################
  



def are_not_dicts_equal(dict1, dict2):
    """
    Check if two dictionaries are equal.

    Args:
    - dict1 (dict): First dictionary.
    - dict2 (dict): Second dictionary.

    Returns:
    - bool: True if dictionaries are equal, False otherwise.
    """
    if len(dict1) != len(dict2):
        return True

    for key, value in dict1.items():
        if key not in dict2 or dict2[key] != value:
            return True

    return False






def update_health_dictionary():

    global global_all_instances_health
    old_dict_instances = {}

    while True:
    
        global_all_instances_health = get_instances_health(TARGET_GROUP_ARN)
        print(global_all_instances_health)

        if are_not_dicts_equal(old_dict_instances,global_all_instances_health):
          i = 1

          for widget in machines_frame.winfo_children():

            try:
                widget.destroy()
            except Exception as e:
                print("error")
                print(e)

          for instance_id, health_status in global_all_instances_health.items():

            frame_state1 = customtkinter.CTkFrame(master=machines_frame ,width=150,height=150,fg_color="#f2f2f2")
            frame_state1.pack(side='right',padx=55)
            cloud_icon1 = customtkinter.CTkImage(Image.open('GUI test/cloud-server.png'), size=(100,100))
            cloud_label1 = customtkinter.CTkLabel(master=frame_state1,image=cloud_icon1, text='')
            cloud_label1.pack()

            # Create labels for instance ID and health status separately
            instance_name = customtkinter.CTkLabel(master=frame_state1, text=f'VM {i}')
            instance_id_label = customtkinter.CTkLabel(master=frame_state1, text=f'{instance_id}')
            health_status_label = customtkinter.CTkLabel(master=frame_state1, text=f'Status: {health_status}')

            
            instance_name.pack()
            instance_id_label.pack()
            health_status_label.pack()
            i +=1

            # if health_status == 'healthy':
            #   state_label1 = customtkinter.CTkLabel(master=frame_state1, text=f'{instance_id}\nStatus: {health_status}')
            # elif health_status == 'unhealthy':
            #   state_label1 = customtkinter.CTkLabel(master=frame_state1, text=f'{instance_id}\nStatus: {health_status}')
            # state_label1.pack()

        old_dict_instances = global_all_instances_health
        #GUI update status and machines
        time.sleep(15)





def auto_scaling_and_Fault_tolerance():

    global request_count
    Fault_Tolerance_flag = False
    Auto_Scaling_flag = False
    
    while True:
        # Get monitoring metrics

        # request_count = get_request_count()
        all_instances_health = get_instances_health(TARGET_GROUP_ARN)
        existing_instances_count = get_number_of_instances_in_target_group(TARGET_GROUP_ARN)

        healthy_instances_count = count_healthy_instances(all_instances_health)
        print(f"healthy_instances_count = {healthy_instances_count}")

        # each interation check on unhealthy and remove them
        unhealthy_instances = get_unhealthy_instance_ids(all_instances_health)

        for instance_id in unhealthy_instances:
            print(f"Terminating instance {instance_id}...")
            EC2_API.terminate_ec2_instance(instance_id)
            print(f"Instance {instance_id} terminated successfully.")
            all_instances_health.pop(instance_id, None)
            print("Terminated instances removed from instances_health dictionary.")
            existing_instances_count -= 1
            
        ###################################################### scaling ##################################################################
        # calculate the required instances based on request count
        if request_count % 3 == 0:
            Needed_Vms = request_count // REQUESTS_PER_INSTANCE
        
        else:
            Needed_Vms = (request_count // REQUESTS_PER_INSTANCE) +1
        
        desired_instances = Needed_Vms - existing_instances_count

        # Check if scaling up is needed based on the calculated required instances
        print(f"desired_instances = {desired_instances}, Needed_Vms= {Needed_Vms} , existing_instances= {existing_instances_count} , request_count= {request_count} ")
        if (desired_instances < 0) and (desired_instances != 0):
            desired_instances *= -1
            for i in range(desired_instances):

                if existing_instances_count <= DESIRED_INSTANCE_COUNT:
                    break
                EC2_API.terminate_ec2_instance(list(all_instances_health.keys())[i])
                existing_instances_count -= 1
                
        elif desired_instances != 0:

            if (desired_instances + existing_instances_count) >= MAX_NUMBER_OF_INSTANCES:
                desired_instances = MAX_NUMBER_OF_INSTANCES - existing_instances_count

            Auto_Scaling_flag = True
            for _ in range(desired_instances):
                instance_scale_thread = threading.Thread(target=add_instance_to_target)
                instance_scale_thread.start()
        
        

        ####################################################### Fault Tolerance #########################################################

        # Check if scaling up is needed based on healthy instance count
        # DESIRED_INSTANCE_COUNT instead of 2
        if not Auto_Scaling_flag:
            if (healthy_instances_count < DESIRED_INSTANCE_COUNT) and (existing_instances_count < MAX_NUMBER_OF_INSTANCES):
                
                instances_needed = max(0, DESIRED_INSTANCE_COUNT - healthy_instances_count)
                if instances_needed != 0:
                    Fault_Tolerance_flag = True

                print(f"instance needed in fault tolerance = {instances_needed}")
                for _ in range(instances_needed):

                    instance_fault_thread = threading.Thread(target=add_instance_to_target)
                    instance_fault_thread.start()
                    

            elif (healthy_instances_count < existing_instances_count) and (existing_instances_count < MAX_NUMBER_OF_INSTANCES):   
                instances_needed = max(0, existing_instances_count - healthy_instances_count)
                if instances_needed != 0:
                    Fault_Tolerance_flag = True

                print(f"instance needed in fault tolerance = {instances_needed}")
                for _ in range(instances_needed):

                    instance_fault_thread = threading.Thread(target=add_instance_to_target)
                    instance_fault_thread.start()


                
        if Fault_Tolerance_flag or Auto_Scaling_flag:
            request_count = 0
            Fault_Tolerance_flag = Auto_Scaling_flag = False
            time.sleep(400)  # wait until instances created, add to target group and become healthy
        
        else:
            request_count = 0
            time.sleep(60)






Health_thread = threading.Thread(target=update_health_dictionary)
Health_thread.start()

Scale_and_fault_thread = threading.Thread(target=auto_scaling_and_Fault_tolerance)
Scale_and_fault_thread.start()

app.mainloop()
