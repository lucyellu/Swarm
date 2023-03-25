import requests
import json
import argparse
import replicate
import openai
import os

"""
Example usage:
python3 dallephone.py nighthawks.jpeg 5

"""


# set the DALL-E API endpoint
dalle_api = "https://api.openai.com/v1/images/generations"

# set the API key
openai.api_key = os.environ("OPENAI_API_KEY")
REPLICATE_API_TOKEN=os.environ("REPLICATE_API_TOKEN")

def get_caption_for_image(image_path):
    model = replicate.models.get("salesforce/blip")
    version = model.versions.get("2e1dddc8621f72155f24cf2e0adbde548458d3cab9f00c0139eea840d0ac4746")
    inputs = {
        # Input image
        'image': open(image_path, "rb"),

        # Choose a task.
        'task': "image_captioning",
    }
    output = version.predict(**inputs)
    return output

def get_image_for_description(description, new_image_name):
    response = openai.Image.create(
        prompt=description,
        n=1,
        size="256x256",
    )
    new_image_url = response["data"][0]["url"]
    print(new_image_url)
    img_data = requests.get(new_image_url).content
    with open(new_image_name, 'wb') as handler:
        handler.write(img_data)

# parse the command line arguments
parser = argparse.ArgumentParser(description='Generate images with DALL-E.')
parser.add_argument('image_file', metavar='image_file', type=str, help='the file of the starting image')
parser.add_argument('n', metavar='n', type=int, help='the number of iterations to perform')

# get the command line arguments
args = parser.parse_args()

# set the initial image URL and number of iterations
image_file = args.image_file
image_name = image_file.split('.')[0]
n = args.n

# loop over the iterations
for i in range(n):
    # describe the image using DALL-E API
    # generate a new image based on the description
    caption = get_caption_for_image(image_file)
    print(caption)
    # extract the new image URL from the API response
    new_image_file_location = f"{image_name}-{i+1}.png"
    get_image_for_description(caption, new_image_file_location)
    print(new_image_file_location)
    # use the new image URL as the starting point for the next iteration
    image_file = new_image_file_location

    # print the iteration number and the new image URL
    print(f"Iteration {i+1}: {new_image_file_location}")
