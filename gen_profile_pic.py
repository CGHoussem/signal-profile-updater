import requests
import os
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageStat
from io import BytesIO
import datetime
import random 

WORD_LIST = ("Love", "Allah", "Alhamdulillah", "Islam", "Peace", "Fake World", "AI", "Automation", "Houssem",
             "Rym", "Chastity", "Respect", "Clarity", "Achieve", "Persistence", "Truth", "Family",
             "Determination", "Passion", "Positivity", "Patience", "Strength", "Dare", "Confidence", "Wealth",
             "Heaven", "Honor", "Hell", "Intelligence", "Creativity", "Righteousness", "Knowledge", "Wisdom",
             "Majesty", "Mindfulness", "Resilience", "Raspberry PI", "Sincerity", "Enemy", "Friend", 
             "Timeless", "The End", "Endless", "Darkness", "Children")
chosen_word = random.choice(WORD_LIST)

## get an image from unsplash
UNSPLASH_API_BASE_ENDPOINT = "https://api.unsplash.com"
url = UNSPLASH_API_BASE_ENDPOINT+"/photos/random?"
headers = {
    "Accept-Version": "v1",
    "Authorization": "Client-ID " + os.environ.get("UNSPLASH_ACCESS_KEY")
}
query = f"{chosen_word} wallpaper"
if chosen_word == "Rym":
    query = "travel wallpaper"
params = {
    "query": query,
}
# request to get a random photo
req_res = requests.get(url, params=params, headers=headers)
print(f"Request a random photo status code : {req_res.status_code}")
if req_res.status_code != 200:
    print(req_res.reason)
    exit(1)

result = req_res.json()
image_url = result['urls']['small']
print(f"Image URL: {image_url}")

## crop image
req_res = requests.get(image_url)
print(f"Get image request status code : {req_res.status_code}")
if req_res.status_code != 200:
    print(req_res.reason)
    exit(1)

img_bytes = BytesIO(req_res.content)
original_img = Image.open(img_bytes)
w, h = original_img.size
size = min(w, h)
left = (w - size) / 2
top = (h - size) / 2
right = (w + size) / 2
bottom = (h + size) / 2
cropped_img = original_img.crop((left, top, right, bottom))
cropped_img = cropped_img.resize(size=(500, 500), resample=Image.Resampling.BICUBIC)

## blur image
blurred_image = cropped_img.filter(ImageFilter.GaussianBlur(radius=3))

# Check if the image is too bright
brightness_threshold = 50
brightness = ImageStat.Stat(blurred_image.convert("L")).mean[0]
if brightness > brightness_threshold:
    # If the image is too bright, darken it
    enhancer = ImageEnhance.Brightness(blurred_image)
    factor = brightness_threshold / brightness
    blurred_image = enhancer.enhance(factor)

## generate text
today = datetime.datetime.today()
date_string = today.strftime('%Y-%m-%d %H:%M:%S')
print(today)
print(date_string)
nb_days = (today - datetime.datetime(2023, 5, 7)).days + 1

## draw texts into image
draw = ImageDraw.Draw(blurred_image)
color = (255, 255, 255)
outline_color = (0, 0, 0)
padding = 10

# Define fonts
font = ImageFont.truetype("./fonts/American Captain.ttf", size=52)
small_font = ImageFont.truetype("./fonts/American Captain.ttf", size=32)
signature_font = ImageFont.truetype("./fonts/Sunday April.ttf", size=42)

# Draw the text with an outline
text = chosen_word
text_bbox = draw.textbbox((0, 0), text, font=font)
x = (blurred_image.width - text_bbox[2]) / 2
y = (blurred_image.height - text_bbox[3]) / 2 - 16
outline_thickness = 2
for x_offset in range(-outline_thickness, outline_thickness + 1):
    for y_offset in range(-outline_thickness, outline_thickness + 1):
        if x_offset != 0 or y_offset != 0:
            draw.text((x + x_offset, y + y_offset), text, font=font, fill=outline_color)
draw.text((x, y), text, fill=color, font=font)

# Draw day index text
text = f"Day #{nb_days}"
text_bbox = draw.textbbox((0, 0), text, font=small_font)
x = (blurred_image.width - text_bbox[2]) / 2
y = text_bbox[3] - padding
draw.text((x, y), text, fill=color, font=small_font)

# Draw last update text
text = f"Last Update: {date_string}"
text_bbox = draw.textbbox((0, 0), text, font=small_font)
x = (blurred_image.width - text_bbox[2]) / 2
y = (blurred_image.height - text_bbox[3]) / 2 + 50 - 16
draw.text((x, y), text, fill=color, font=small_font)

# Draw signature text
text = "PxHoussem"
text_bbox = draw.textbbox((0, 0), text, font=signature_font)

x = (blurred_image.width - text_bbox[2]) - padding
y = (blurred_image.height - text_bbox[3]) - padding
draw.text((x, y), text, fill=color, font=signature_font)

## save image
blurred_image.save("final_image.jpg")
