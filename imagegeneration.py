import asyncio
from random import randint  # Fixed typo: trandom → random
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open generated images
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            img.show()  # Actually opens the image
            print(f"Opening image: {image_path}")
        except Exception as e:
            print(f"Error opening image {image_path}: {e}")

# Async function to query Hugging Face API
async def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIkey')}"}
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Main image generation logic
async def generate_image(prompt: str):
    tasks = []
    for i in range(4):  # Fixed: `for in range(4)` → `for i in range(4)`
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        filename = f"Data/{prompt.replace(' ', '_')}{i + 1}.jpg"
        with open(filename, "wb") as f:
            f.write(image_bytes)  # Fixed typo: wite → write

# Helper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)

# File polling logic
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            data: str = f.read()
            Prompt, Status = data.split(",")

        if Status.strip() == "True":  # Fixed: `=` → `==`
            print("GenerateImages...")
            GenerateImages(prompt=Prompt.strip())

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)

    except :
        pass
