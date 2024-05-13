from tkinter import PhotoImage, filedialog
import customtkinter
from PIL import Image
import os
from urllib.parse import urlparse
import webbrowser
# from ALB_API import send_image_processing_request
import time
import main_operations
import ALB_API
import asyncio

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

TARGET_GROUP_ARN ='arn:aws:elasticloadbalancing:eu-central-1:851725392781:targetgroup/Image-Processing-Frank-TG/4594d70e60686eda'
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
  popup = customtkinter.Toplevel()
  popup.title("This is a Pop-up Window")
  popup.geometry("300x150")  # Set size

  # Label within the popup
  label = customtkinter.CTkLabel(popup, text=message)
  label.pack()

  # Button to close the popup
  close_button = customtkinter.CTkButton(popup, text="Close", command=popup.destroy)
  close_button.pack()

async def Apply_operation(filenames,operation):
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
machines_frame = customtkinter.CTkScrollableFrame(master=app ,width=630,height=150,fg_color="#f2f2f2",border_width=1,corner_radius=15,orientation='horizontal')
machines_frame.place(x=245, y=100)

for i in range (10):
  frame_state1 = customtkinter.CTkFrame(master=machines_frame ,width=150,height=150,fg_color="#f2f2f2")
  frame_state1.pack(side='right',padx=55)
  # frame_state1.pack_propagate(False)
  # frame_state2 = customtkinter.CTkFrame(master=machines_frame ,width=150,height=150,fg_color="#f2f2f2")
  # frame_state2.pack(side='right',padx=25)
  # frame_state2.pack_propagate(False)
  # frame_state3 = customtkinter.CTkFrame(master=machines_frame ,width=150,height=150,fg_color="#f2f2f2")
  # frame_state3.pack(side='right',padx=25)
  # frame_state3.pack_propagate(False)
  cloud_icon1 = customtkinter.CTkImage(Image.open('GUI test/cloud-server.png'), size=(100,100))
  cloud_label1 = customtkinter.CTkLabel(master=frame_state1,image=cloud_icon1, text='')
  cloud_label1.pack()
  state_label1 = customtkinter.CTkLabel(master=frame_state1, text='VM Name\nHealth: Status')
  state_label1.pack()


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
  





def update_health_dictionary():

    global global_all_instances_health

    while True:
    
        global_all_instances_health = main_operations.get_instances_health(TARGET_GROUP_ARN)
        #GUI update status and machines
        time.sleep(30)

        
app.mainloop()