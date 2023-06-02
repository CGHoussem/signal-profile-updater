import requests
import os
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageStat
from io import BytesIO
import datetime
import random 
import logging

logging.basicConfig(filename='data/log.txt')

FILENAME = f"data/{datetime.date.today()}.jpg"
WORD_LIST = ("Love", "Allah", "Alhamdulillah", "Islam", "Peace", "Fake World", "AI", "Deception", "Houssem",
             "Rym", "Chastity", "Respect", "Clarity", "Achieve", "Persistence", "Truth", "Family",
             "Determination", "Passion", "Positivity", "Patience", "Strength", "Confidence", "Wealth",
             "Heaven", "Honor", "Hell", "Intelligence", "Creativity", "Righteousness", "Knowledge", "Wisdom",
             "Majesty", "Mindfulness", "Resilience", "Sincerity", "Culture", "Death", "Destiny",
             "Timeless", "The End", "Endless", "Darkness", "Children", "Mystery", "Battlefield")
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
	query = "Travel wallpaper"
elif chosen_word == "Houssem":
	query = "Nebula wallpaper"
elif chosen_word == "Alhamdulillah":
	query = "Allah wallpaper"
params = {
    "query": query,
}
# request to get a random photo
req_res = requests.get(url, params=params, headers=headers)
if req_res.status_code != 200:
    logging.error(f'Error making GET request to get random image: {req_res.reason}')
    exit(1)

result = req_res.json()
image_url = result['urls']['small']
logging.info(f"Chosen image URL: {image_url}")

## crop image
req_res = requests.get(image_url)
if req_res.status_code != 200:
    logging.error(f'Error making GET request to download image: {req_res.reason}')
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

# crop a section from the image where to place text
text_crop_img = cropped_img.crop((50, 150, 450, 350))
# blur the cropped section
text_crop_img = text_crop_img.filter(ImageFilter.GaussianBlur(radius=4))
# darken the cropped section
brightness = ImageStat.Stat(text_crop_img.convert("L")).mean[0]
enhancer = ImageEnhance.Brightness(text_crop_img)
factor = 75 / brightness
text_crop_img = enhancer.enhance(factor)

# draw text on the cropped section
## generate text
today = datetime.datetime.today()
date_string = today.strftime('%Y-%m-%d %H:%M:%S')
logging.info(date_string)
nb_days = (today - datetime.datetime(2023, 5, 7)).days + 1

draw_on_image = text_crop_img

## draw texts into image
draw = ImageDraw.Draw(draw_on_image)
draw_extra = ImageDraw.Draw(cropped_img)
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
x = (draw_on_image.width - text_bbox[2]) / 2
y = (draw_on_image.height - text_bbox[3]) / 2 - 16
outline_thickness = 2
for x_offset in range(-outline_thickness, outline_thickness + 1):
    for y_offset in range(-outline_thickness, outline_thickness + 1):
        if x_offset != 0 or y_offset != 0:
            draw.text((x + x_offset, y + y_offset), text, font=font, fill=outline_color)
draw.text((x, y), text, fill=color, font=font)

# Draw last update text
text = f"Last Update: {date_string}"
text_bbox = draw.textbbox((0, 0), text, font=small_font)
x = (draw_on_image.width - text_bbox[2]) / 2
y = (draw_on_image.height - text_bbox[3]) / 2 + 50 - 16
draw.text((x, y), text, fill=color, font=small_font)

# Draw day index text
text = f"Day #{nb_days}"
text_bbox = draw.textbbox((0, 0), text, font=small_font)
x =  padding
y = (cropped_img.height - text_bbox[3]) - padding
outline_thickness = 1
for x_offset in range(-outline_thickness, outline_thickness + 1):
    for y_offset in range(-outline_thickness, outline_thickness + 1):
        if x_offset != 0 or y_offset != 0:
            draw_extra.text((x + x_offset, y + y_offset), text, font=small_font, fill=outline_color)
draw_extra.text((x, y), text, fill=color, font=small_font)

# Draw signature text
text = "PxHoussem"
text_bbox = draw.textbbox((0, 0), text, font=signature_font)
x = (cropped_img.width - text_bbox[2]) - padding
y = (cropped_img.height - text_bbox[3]) - padding
outline_thickness = 1
for x_offset in range(-outline_thickness, outline_thickness + 1):
    for y_offset in range(-outline_thickness, outline_thickness + 1):
        if x_offset != 0 or y_offset != 0:
            draw_extra.text((x + x_offset, y + y_offset), text, font=signature_font, fill=outline_color)
draw_extra.text((x, y), text, fill=color, font=signature_font)

# place back the cropped section into theimage
cropped_img.paste(draw_on_image, (50, 150))

## save image
cropped_img.save(FILENAME)
