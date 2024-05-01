import aiohttp
import asyncio
import os
import json

async def send_image_processing_request(image_path, operation, output_name, s3_bucket):
    # Load balancer URL
    load_balancer_url = 'http://img-proc-test-1-1208126696.eu-north-1.elb.amazonaws.com/process_image' 

    # Read the image file
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Request data
    request_data = aiohttp.FormData()
    request_data.add_field('image', image_data, filename = os.path.basename(image_path))
    request_data.add_field('operation', operation)
    request_data.add_field('output_name', output_name)
    request_data.add_field('s3_bucket', s3_bucket)

    async with aiohttp.ClientSession() as session:
        async with session.post(load_balancer_url, data=request_data) as response:
            if response.status == 200:
                print("Image processing request sent successfully to the load balancer.")
                
                response_json = await response.json()  # Parse JSON response
                download_link = response_json.get('download_link')  # Extract download link
                if download_link:
                    print(f"Image processing request sent successfully to the load balancer. Download link: {download_link}")
                else:
                    print("Failed to get download link from the response.")
                
            else:
                error_message = await response.text()
                print(f"Failed to send image processing request to the load balancer. Error: {error_message}")


async def main():
    await send_image_processing_request(
        image_path='C:/Users/oem/Downloads/area-graph.png',
        operation='color_inversion',
        output_name='inverted.png',
        s3_bucket='dist-proj-buck-1'
    )

    await send_image_processing_request(
        image_path='C:/Users/oem/Downloads/bug (1).png',
        operation='thresholding',
        output_name='threshold.png',
        s3_bucket='dist-proj-buck-1'
    )
    
    await send_image_processing_request(
        image_path='C:/Users/oem/Downloads/debugging (1).png',
        operation='grayscale',
        output_name='grayscaled.png',
        s3_bucket='dist-proj-buck-1'
    )

# Run the asynchronous function
asyncio.run(main())
